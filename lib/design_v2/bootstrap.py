from __future__ import annotations

import html
import json
import os
import re
import shutil
import stat
import subprocess
import tarfile
import tempfile
import zipfile
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urlencode, urlparse

from ..common import he_dir, home, repo_root, sha256_file, share_dir, write_json
from ..paths import tar_member_ok
from . import FTS_SCHEMA_VERSION, PACKAGE_DIR
from .bank import DesignV2Error, resolve_design_v2_root
from .commands import bank_health, doctor_rows
from .dedupe import dedupe
from .importers.bank_pointer import (
    POINTER_PREVIEW_SAMPLE,
    pointer_catalog_rows,
    preview_relative_path,
    resolve_catalog_file,
)
from .ingest import ingest_path
from .rebuild import rebuild
from .security import member_ok


SOURCE_CONFIG = PACKAGE_DIR / "bootstrap_sources.json"
SOURCE_NAME_RE = re.compile(r"^[a-z0-9][a-z0-9._-]{0,63}$")
DRIVE_FILE_ID_RE = re.compile(r"^[A-Za-z0-9_-]{10,128}$")
SHA256_HEX_RE = re.compile(r"^[0-9A-Fa-f]{64}$")
SHA256_RE = re.compile(r"^([0-9A-Fa-f]{64})[ \t]+\*?([^\r\n]+)$")
DRIVE_VIEW_RE = re.compile(r"https?://(?:drive|docs)\.google\.com/file/d/([A-Za-z0-9_-]{10,128})")
DRIVE_ID_QUERY_RE = re.compile(r"[?&]id=([A-Za-z0-9_-]{10,128})")
DRIVE_CONFIRM_RE = re.compile(r"[?&]confirm=([0-9A-Za-z_-]+)")
DRIVE_CONFIRM_INPUT_RE = re.compile(
    r'name=["\']confirm["\'][^>]*value=["\']([^"\']+)["\']|value=["\']([^"\']+)["\'][^>]*name=["\']confirm["\']',
    re.I,
)
ZIP_MAGIC = (b"PK\x03\x04", b"PK\x05\x06", b"PK\x07\x08")
GZIP_MAGIC = b"\x1f\x8b"
DRIVE_HOSTS = ("drive.google.com", "drive.usercontent.google.com", "docs.google.com")
BOOTSTRAP_ZIP_LIMITS = {
    "max_members": 150_000,
    "max_member_uncompressed": 1 << 30,
    "max_total_uncompressed": 8 << 30,
    "max_compression_ratio": 500.0,
    "max_path_depth": 24,
    "max_path_length": 512,
}
REQUIRED_CATALOGS = {
    "21st": Path("21st/library/catalog.json"),
    "aura": Path("aura/library/catalog.json"),
    "refero": Path("Refero/bank/catalog.json"),
    "motionsites": Path("motionsites/library/catalog.json"),
}

Downloader = Callable[[str, Path], None]
StageReporter = Callable[[str, str], None]


class BootstrapError(DesignV2Error):
    code = "BOOTSTRAP_FAILED"

    def __init__(self, stage: str, message: str, *, code: str = "BOOTSTRAP_FAILED") -> None:
        super().__init__(f"{stage}: {message}", code=code)
        self.stage = stage
        self.detail = message


@dataclass(frozen=True)
class BootstrapSource:
    name: str
    source_type: str
    bank_version: str
    archive_name: str
    archive_file_id: str
    checksum_file_id: str
    pinned_sha256: str | None = None


def _config_error(message: str) -> BootstrapError:
    return BootstrapError("SOURCE_RESOLVED", message, code="BOOTSTRAP_SOURCE_INVALID")


def load_bootstrap_sources(path: Path | None = None) -> tuple[str, dict[str, BootstrapSource]]:
    config_path = path or SOURCE_CONFIG
    try:
        payload = json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise _config_error("source configuration is unreadable") from exc
    if not isinstance(payload, dict) or set(payload) != {"schemaVersion", "default", "sources"}:
        raise _config_error("source configuration shape")
    if payload.get("schemaVersion") != 1:
        raise _config_error("source configuration schema")
    default = payload.get("default")
    raw_sources = payload.get("sources")
    if not isinstance(default, str) or not SOURCE_NAME_RE.fullmatch(default):
        raise _config_error("default source")
    if not isinstance(raw_sources, dict) or not raw_sources:
        raise _config_error("sources")

    sources: dict[str, BootstrapSource] = {}
    required = {
        "type",
        "bankVersion",
        "archiveName",
        "archiveFileId",
        "checksumFileId",
    }
    allowed = required | {"archiveSha256"}
    for name, raw in raw_sources.items():
        if not isinstance(name, str) or not SOURCE_NAME_RE.fullmatch(name) or not isinstance(raw, dict):
            raise _config_error("source entry")
        if not required.issubset(raw) or set(raw) - allowed:
            raise _config_error(f"source fields for {name}")
        source_type = raw.get("type")
        bank_version = raw.get("bankVersion")
        archive_name = raw.get("archiveName")
        archive_file_id = raw.get("archiveFileId")
        checksum_file_id = raw.get("checksumFileId")
        pinned = raw.get("archiveSha256")
        if source_type != "google-drive-public":
            raise _config_error(f"unsupported source type for {name}")
        if not isinstance(bank_version, str) or not bank_version or len(bank_version) > 32:
            raise _config_error(f"bank version for {name}")
        if (
            not isinstance(archive_name, str)
            or Path(archive_name).name != archive_name
            or not archive_name.endswith(".zip")
        ):
            raise _config_error(f"archive name for {name}")
        if not isinstance(archive_file_id, str) or not DRIVE_FILE_ID_RE.fullmatch(archive_file_id):
            raise _config_error(f"archive file ID for {name}")
        if not isinstance(checksum_file_id, str) or not DRIVE_FILE_ID_RE.fullmatch(checksum_file_id):
            raise _config_error(f"checksum file ID for {name}")
        if pinned is not None and (not isinstance(pinned, str) or not re.fullmatch(r"[0-9A-Fa-f]{64}", pinned)):
            raise _config_error(f"pinned checksum for {name}")
        sources[name] = BootstrapSource(
            name=name,
            source_type=source_type,
            bank_version=bank_version,
            archive_name=archive_name,
            archive_file_id=archive_file_id,
            checksum_file_id=checksum_file_id,
            pinned_sha256=pinned.lower() if isinstance(pinned, str) else None,
        )
    if default not in sources:
        raise _config_error("default source is missing")
    return default, sources


def resolve_bootstrap_source(name: str | None = None, *, config_path: Path | None = None) -> BootstrapSource:
    default, sources = load_bootstrap_sources(config_path)
    selected = name or default
    if selected not in sources:
        raise BootstrapError("SOURCE_RESOLVED", f"unknown source {selected}", code="BOOTSTRAP_SOURCE_UNKNOWN")
    return sources[selected]


def google_drive_public_url(file_id: str) -> str:
    if not DRIVE_FILE_ID_RE.fullmatch(file_id):
        raise _config_error("Google Drive file ID")
    query = urlencode({"id": file_id, "export": "download", "confirm": "t"})
    return f"https://drive.usercontent.google.com/download?{query}"


def resolve_operator_url(url: str) -> str:
    raw = (url or "").strip()
    if not raw.startswith("https://"):
        raise BootstrapError("SOURCE_RESOLVED", "URL must be https", code="DESIGN_BANK_URL_INVALID")
    view = DRIVE_VIEW_RE.search(raw)
    if view:
        return f"https://drive.google.com/uc?export=download&id={view.group(1)}"
    host = (urlparse(raw).hostname or "").lower()
    if host in DRIVE_HOSTS:
        found = DRIVE_ID_QUERY_RE.search(raw)
        if found:
            return f"https://drive.google.com/uc?export=download&id={found.group(1)}"
    return raw


def env_design_bank_override() -> tuple[str, str] | None:
    url = (os.environ.get("OPENCODE_DESIGN_BANK_URL") or "").strip()
    sha = (os.environ.get("OPENCODE_DESIGN_BANK_SHA256") or "").strip()
    if not url:
        return None
    if not SHA256_HEX_RE.fullmatch(sha):
        raise BootstrapError(
            "SOURCE_RESOLVED",
            "OPENCODE_DESIGN_BANK_SHA256 is required",
            code="SHA256_REQUIRED",
        )
    return url, sha.lower()


def _archive_name_from_url(url: str, default: str) -> str:
    host = (urlparse(url).hostname or "").lower()
    if host in DRIVE_HOSTS:
        return default
    name = Path(urlparse(url).path).name
    if not name or name in {".", "..", "uc", "download", "view"} or "/" in name or "\\" in name:
        return default
    return name


def operator_url_source(url: str, sha256: str) -> tuple[BootstrapSource, str]:
    resolved = resolve_operator_url(url)
    return (
        BootstrapSource(
            name="env-url",
            source_type="operator-url",
            bank_version="env",
            archive_name=_archive_name_from_url(resolved, "design-bank.bin"),
            archive_file_id="",
            checksum_file_id="",
            pinned_sha256=sha256.lower(),
        ),
        resolved,
    )


def github_fallback_source() -> tuple[BootstrapSource, str]:
    path = repo_root() / "vendor" / "sources.json"
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise BootstrapError("SOURCE_RESOLVED", "vendor sources unreadable", code="BOOTSTRAP_SOURCE_INVALID") from exc
    block = ((payload.get("sources") or {}) if isinstance(payload, dict) else {}).get("design-bank")
    if not isinstance(block, dict):
        raise BootstrapError("SOURCE_RESOLVED", "github fallback missing", code="BOOTSTRAP_SOURCE_INVALID")
    url = block.get("artifactUrl")
    sha = block.get("artifactSha256")
    if not isinstance(url, str) or not url.startswith("https://"):
        raise BootstrapError("SOURCE_RESOLVED", "github fallback URL", code="BOOTSTRAP_SOURCE_INVALID")
    if not isinstance(sha, str) or not SHA256_HEX_RE.fullmatch(sha):
        raise BootstrapError("SOURCE_RESOLVED", "github fallback SHA-256", code="BOOTSTRAP_SOURCE_INVALID")
    return (
        BootstrapSource(
            name="github-release-fallback",
            source_type="https-artifact",
            bank_version=str(block.get("version") or "fallback"),
            archive_name=_archive_name_from_url(url, "Design-bank.tgz"),
            archive_file_id="",
            checksum_file_id="",
            pinned_sha256=sha.lower(),
        ),
        url,
    )


def select_remote_source(
    source_name: str | None = None, *, config_path: Path | None = None
) -> tuple[BootstrapSource, str | None, str]:
    env = env_design_bank_override()
    if env:
        source, url = operator_url_source(env[0], env[1])
        return source, url, "curl-operator-url"
    try:
        source = resolve_bootstrap_source(source_name, config_path=config_path)
        return source, None, "curl-google-drive-public"
    except BootstrapError:
        if source_name:
            raise
        source, url = github_fallback_source()
        return source, url, "curl-github-release"


def _is_html_file(path: Path) -> bool:
    try:
        head = path.read_bytes()[:512].lstrip().lower()
    except OSError:
        return False
    return head.startswith(b"<!doctype html") or head.startswith(b"<html")


def drive_confirm_url(original_url: str, page: str) -> str | None:
    text = html.unescape(page)
    tokens = DRIVE_CONFIRM_RE.findall(text)
    for match in DRIVE_CONFIRM_INPUT_RE.findall(text):
        tokens.extend(part for part in match if part)
    confirm = next((token for token in tokens if token and token != "t"), tokens[0] if tokens else None)
    if not confirm:
        return None
    found = DRIVE_ID_QUERY_RE.search(original_url) or DRIVE_ID_QUERY_RE.search(text)
    file_id = found.group(1) if found else None
    if file_id and DRIVE_FILE_ID_RE.fullmatch(file_id):
        return f"https://drive.google.com/uc?export=download&id={file_id}&confirm={confirm}"
    sep = "&" if "?" in original_url else "?"
    return f"{original_url}{sep}confirm={confirm}"


def _is_drive_url(url: str) -> bool:
    host = (urlparse(url).hostname or "").lower()
    return host in DRIVE_HOSTS


def _run_curl(curl: str, url: str, destination: Path, cookie_jar: Path | None) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    partial = destination.with_name(destination.name + ".part")
    command = [
        curl,
        "--location",
        "--silent",
        "--show-error",
        "--retry",
        "4",
        "--retry-delay",
        "2",
        "--retry-all-errors",
        "--connect-timeout",
        "30",
        "--output",
        str(partial),
    ]
    if cookie_jar is not None:
        command.extend(["--cookie", str(cookie_jar), "--cookie-jar", str(cookie_jar)])
    command.append(url)
    try:
        result = subprocess.run(command, capture_output=True, text=True)
    except OSError as exc:
        partial.unlink(missing_ok=True)
        raise BootstrapError("ARCHIVE_DOWNLOADED", type(exc).__name__, code="DOWNLOAD_FAILED") from exc
    if result.returncode != 0:
        partial.unlink(missing_ok=True)
        detail = (result.stderr or "curl failed").strip().splitlines()[-1]
        raise BootstrapError("ARCHIVE_DOWNLOADED", detail, code="DOWNLOAD_FAILED")
    if partial.is_symlink() or not partial.is_file() or partial.stat().st_size == 0:
        partial.unlink(missing_ok=True)
        raise BootstrapError("ARCHIVE_DOWNLOADED", "empty download", code="DOWNLOAD_FAILED")
    os.replace(partial, destination)


def _curl_download(url: str, destination: Path) -> None:
    curl = shutil.which("curl")
    if not curl:
        raise BootstrapError("PREFLIGHT", "curl is required", code="CURL_MISSING")
    if not _is_drive_url(url):
        _run_curl(curl, url, destination, None)
        return
    with tempfile.TemporaryDirectory(prefix="opencode-he-drive-") as tmp:
        cookie_jar = Path(tmp) / "cookies"
        _run_curl(curl, url, destination, cookie_jar)
        if not _is_html_file(destination):
            return
        try:
            page = destination.read_text(encoding="utf-8", errors="ignore")
        except OSError as exc:
            destination.unlink(missing_ok=True)
            raise BootstrapError("ARCHIVE_DOWNLOADED", "unreadable download", code="DOWNLOAD_FAILED") from exc
        confirm = drive_confirm_url(url, page)
        destination.unlink(missing_ok=True)
        if not confirm:
            raise BootstrapError("ARCHIVE_DOWNLOADED", "Google Drive confirm page", code="DOWNLOAD_FAILED")
        _run_curl(curl, confirm, destination, cookie_jar)
        if _is_html_file(destination):
            destination.unlink(missing_ok=True)
            raise BootstrapError("ARCHIVE_DOWNLOADED", "Google Drive confirm page", code="DOWNLOAD_FAILED")


def download_public_file(url: str, destination: Path) -> None:
    _curl_download(url, destination)


def parse_checksum(text: str, archive_name: str) -> str:
    records: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        match = SHA256_RE.fullmatch(line)
        if not match:
            raise BootstrapError("CHECKSUM_FETCHED", "malformed SHA-256 file", code="CHECKSUM_INVALID")
        filename = match.group(2).strip()
        if filename != archive_name:
            raise BootstrapError("CHECKSUM_FETCHED", "checksum archive name mismatch", code="CHECKSUM_INVALID")
        records.append(match.group(1).lower())
    if not records or len(set(records)) != 1:
        raise BootstrapError("CHECKSUM_FETCHED", "missing or conflicting SHA-256", code="CHECKSUM_INVALID")
    return records[0]


def _zip_error(message: str, code: str = "ARCHIVE_UNSAFE") -> BootstrapError:
    return BootstrapError("ARCHIVE_INSPECTED", message, code=code)


def inspect_bootstrap_zip(path: Path) -> dict[str, int]:
    try:
        with path.open("rb") as handle:
            magic = handle.read(4)
    except OSError as exc:
        raise _zip_error("archive is unreadable", "ARCHIVE_INVALID") from exc
    if not any(magic.startswith(prefix) for prefix in ZIP_MAGIC):
        raise _zip_error("download is not a ZIP archive", "ARCHIVE_INVALID")
    try:
        with zipfile.ZipFile(path) as handle:
            infos = handle.infolist()
    except (OSError, zipfile.BadZipFile) as exc:
        raise _zip_error("invalid ZIP archive", "ARCHIVE_INVALID") from exc
    limits = BOOTSTRAP_ZIP_LIMITS
    if not infos or len(infos) > int(limits["max_members"]):
        raise _zip_error("ZIP member limit")
    seen: set[str] = set()
    total = 0
    files = 0
    for info in infos:
        name = info.filename.replace("\\", "/")
        if "\x00" in name or not member_ok(name):
            raise _zip_error(f"unsafe ZIP path {name}")
        if len(name) > int(limits["max_path_length"]) or len(Path(name).parts) > int(limits["max_path_depth"]):
            raise _zip_error("ZIP path limit")
        normalized = name.rstrip("/")
        if normalized in seen:
            raise _zip_error(f"duplicate ZIP path {normalized}")
        seen.add(normalized)
        mode = info.external_attr >> 16
        file_type = stat.S_IFMT(mode)
        if stat.S_ISLNK(mode) or file_type not in {0, stat.S_IFREG, stat.S_IFDIR}:
            raise _zip_error(f"special ZIP member {name}")
        if info.flag_bits & 0x1:
            raise _zip_error("encrypted ZIP member")
        if info.is_dir() or name.endswith("/"):
            continue
        files += 1
        uncompressed = int(info.file_size)
        compressed = max(int(info.compress_size), 1)
        if uncompressed > int(limits["max_member_uncompressed"]):
            raise _zip_error("ZIP member size limit")
        if uncompressed and uncompressed / compressed > float(limits["max_compression_ratio"]):
            raise _zip_error("ZIP compression ratio limit")
        total += uncompressed
        if total > int(limits["max_total_uncompressed"]):
            raise _zip_error("ZIP total size limit")
    return {"members": len(infos), "files": files, "uncompressed_bytes": total}


def safe_extract_bootstrap_zip(path: Path, destination: Path) -> dict[str, int]:
    stats = inspect_bootstrap_zip(path)
    destination.mkdir(parents=True, exist_ok=False)
    base = destination.resolve()
    try:
        with zipfile.ZipFile(path) as handle:
            for info in handle.infolist():
                name = info.filename.replace("\\", "/")
                target = destination / name.rstrip("/")
                try:
                    target.resolve(strict=False).relative_to(base)
                except (OSError, ValueError) as exc:
                    raise BootstrapError(
                        "EXTRACTED_TO_TEMP", f"unsafe ZIP path {name}", code="ARCHIVE_EXTRACTION_FAILED"
                    ) from exc
                if info.is_dir() or name.endswith("/"):
                    target.mkdir(parents=True, exist_ok=True)
                    continue
                target.parent.mkdir(parents=True, exist_ok=True)
                try:
                    with handle.open(info) as reader, target.open("xb") as writer:
                        shutil.copyfileobj(reader, writer, length=1 << 20)
                except (OSError, RuntimeError, zipfile.BadZipFile) as exc:
                    raise BootstrapError(
                        "EXTRACTED_TO_TEMP", f"failed to extract {name}", code="ARCHIVE_EXTRACTION_FAILED"
                    ) from exc
                st = target.lstat()
                if not stat.S_ISREG(st.st_mode) or st.st_nlink != 1 or st.st_size != info.file_size:
                    raise BootstrapError(
                        "EXTRACTED_TO_TEMP", f"unsafe extracted file {name}", code="ARCHIVE_EXTRACTION_FAILED"
                    )
    except BootstrapError:
        raise
    except (OSError, zipfile.BadZipFile) as exc:
        raise BootstrapError("EXTRACTED_TO_TEMP", "ZIP extraction failed", code="ARCHIVE_EXTRACTION_FAILED") from exc
    return stats


def inspect_bootstrap_tar(path: Path) -> dict[str, int]:
    try:
        handle = tarfile.open(path, mode="r:*")
    except (OSError, tarfile.TarError) as exc:
        raise BootstrapError("ARCHIVE_INSPECTED", "invalid tar archive", code="ARCHIVE_INVALID") from exc
    limits = BOOTSTRAP_ZIP_LIMITS
    try:
        members = handle.getmembers()
        if not members or len(members) > int(limits["max_members"]):
            raise BootstrapError("ARCHIVE_INSPECTED", "tar member limit", code="ARCHIVE_UNSAFE")
        seen: set[str] = set()
        total = 0
        files = 0
        for member in members:
            name = (member.name or "").replace("\\", "/")
            normalized = name.rstrip("/")
            if normalized in {"", "."}:
                continue
            if "\x00" in name or not member_ok(normalized) or ".." in Path(name).parts:
                raise BootstrapError("ARCHIVE_INSPECTED", f"unsafe tar path {name}", code="ARCHIVE_UNSAFE")
            if len(name) > int(limits["max_path_length"]) or len(Path(name).parts) > int(limits["max_path_depth"]):
                raise BootstrapError("ARCHIVE_INSPECTED", "tar path limit", code="ARCHIVE_UNSAFE")
            if normalized in seen:
                raise BootstrapError("ARCHIVE_INSPECTED", f"duplicate tar path {normalized}", code="ARCHIVE_UNSAFE")
            seen.add(normalized)
            if member.issym() or member.islnk() or not (member.isfile() or member.isdir()):
                raise BootstrapError("ARCHIVE_INSPECTED", f"special tar member {name}", code="ARCHIVE_UNSAFE")
            if member.isdir():
                continue
            files += 1
            uncompressed = int(member.size)
            if uncompressed > int(limits["max_member_uncompressed"]):
                raise BootstrapError("ARCHIVE_INSPECTED", "tar member size limit", code="ARCHIVE_UNSAFE")
            total += uncompressed
            if total > int(limits["max_total_uncompressed"]):
                raise BootstrapError("ARCHIVE_INSPECTED", "tar total size limit", code="ARCHIVE_UNSAFE")
        return {"members": len(members), "files": files, "uncompressed_bytes": total}
    finally:
        handle.close()


def safe_extract_bootstrap_tar(path: Path, destination: Path) -> dict[str, int]:
    stats = inspect_bootstrap_tar(path)
    destination.mkdir(parents=True, exist_ok=False)
    base = destination.resolve()
    try:
        with tarfile.open(path, mode="r:*") as handle:
            for member in handle.getmembers():
                name = (member.name or "").replace("\\", "/")
                if name.rstrip("/") in {"", "."}:
                    continue
                if not tar_member_ok(destination, name):
                    raise BootstrapError(
                        "EXTRACTED_TO_TEMP", f"unsafe tar path {name}", code="ARCHIVE_EXTRACTION_FAILED"
                    )
                target = destination / name.rstrip("/")
                try:
                    target.resolve(strict=False).relative_to(base)
                except (OSError, ValueError) as exc:
                    raise BootstrapError(
                        "EXTRACTED_TO_TEMP", f"unsafe tar path {name}", code="ARCHIVE_EXTRACTION_FAILED"
                    ) from exc
                if member.isdir():
                    target.mkdir(parents=True, exist_ok=True)
                    continue
                if not member.isfile():
                    raise BootstrapError(
                        "EXTRACTED_TO_TEMP", f"special tar member {name}", code="ARCHIVE_EXTRACTION_FAILED"
                    )
                target.parent.mkdir(parents=True, exist_ok=True)
                reader = handle.extractfile(member)
                if reader is None:
                    raise BootstrapError(
                        "EXTRACTED_TO_TEMP", f"failed to extract {name}", code="ARCHIVE_EXTRACTION_FAILED"
                    )
                try:
                    with reader, target.open("xb") as writer:
                        shutil.copyfileobj(reader, writer, length=1 << 20)
                except OSError as exc:
                    raise BootstrapError(
                        "EXTRACTED_TO_TEMP", f"failed to extract {name}", code="ARCHIVE_EXTRACTION_FAILED"
                    ) from exc
                st = target.lstat()
                if not stat.S_ISREG(st.st_mode) or st.st_nlink != 1 or st.st_size != member.size:
                    raise BootstrapError(
                        "EXTRACTED_TO_TEMP", f"unsafe extracted file {name}", code="ARCHIVE_EXTRACTION_FAILED"
                    )
    except BootstrapError:
        raise
    except (OSError, tarfile.TarError) as exc:
        raise BootstrapError("EXTRACTED_TO_TEMP", "tar extraction failed", code="ARCHIVE_EXTRACTION_FAILED") from exc
    return stats


def _archive_magic(path: Path) -> bytes:
    try:
        with path.open("rb") as handle:
            return handle.read(4)
    except OSError as exc:
        raise BootstrapError("ARCHIVE_INSPECTED", "archive is unreadable", code="ARCHIVE_INVALID") from exc


def inspect_bootstrap_archive(path: Path) -> dict[str, int]:
    magic = _archive_magic(path)
    if any(magic.startswith(prefix) for prefix in ZIP_MAGIC):
        return inspect_bootstrap_zip(path)
    if magic.startswith(GZIP_MAGIC):
        return inspect_bootstrap_tar(path)
    raise BootstrapError("ARCHIVE_INSPECTED", "download is not a ZIP or tar archive", code="ARCHIVE_INVALID")


def safe_extract_bootstrap_archive(path: Path, destination: Path) -> dict[str, int]:
    magic = _archive_magic(path)
    if any(magic.startswith(prefix) for prefix in ZIP_MAGIC):
        return safe_extract_bootstrap_zip(path, destination)
    if magic.startswith(GZIP_MAGIC):
        return safe_extract_bootstrap_tar(path, destination)
    raise BootstrapError("ARCHIVE_INSPECTED", "download is not a ZIP or tar archive", code="ARCHIVE_INVALID")


def validate_design_bank(root: Path) -> dict[str, Any]:
    check_root = root.resolve() if root.is_symlink() else root
    if not check_root.is_dir() or check_root.is_symlink():
        raise BootstrapError("BANK_VALIDATED", "Design Bank root is not a directory", code="DESIGN_BANK_INVALID")
    counts: dict[str, int] = {}
    sampled: dict[str, int] = {}
    for provider, relative in REQUIRED_CATALOGS.items():
        catalog = root / relative
        if catalog.is_symlink() or not catalog.is_file():
            raise BootstrapError("BANK_VALIDATED", f"missing {relative}", code="DESIGN_BANK_INVALID")
        try:
            payload = json.loads(catalog.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise BootstrapError(
                "BANK_VALIDATED", f"malformed {relative}", code="DESIGN_BANK_INVALID"
            ) from exc
        rows = pointer_catalog_rows(payload, provider)
        if rows is None:
            raise BootstrapError("BANK_VALIDATED", f"invalid {relative}", code="DESIGN_BANK_INVALID")
        counts[provider] = len(rows)
        sampled[provider] = 0
        if provider not in {"21st", "aura"}:
            continue
        provider_root = root / provider
        for row in rows:
            raw_preview = row.get("preview")
            if not isinstance(raw_preview, str) or not raw_preview.strip():
                continue
            preview = preview_relative_path(row)
            if not preview:
                raise BootstrapError(
                    "BANK_VALIDATED", f"invalid {provider} preview pointer", code="DESIGN_BANK_INVALID"
                )
            resolved = resolve_catalog_file(provider_root, preview)
            if resolved is None or resolved.is_symlink() or not resolved.is_file():
                raise BootstrapError(
                    "BANK_VALIDATED", f"missing {provider} preview {preview}", code="DESIGN_BANK_INVALID"
                )
            sampled[provider] += 1
            if sampled[provider] >= POINTER_PREVIEW_SAMPLE:
                break
    return {"counts": counts, "preview_samples": sampled}


def normalize_extracted_bank(extracted: Path) -> Path:
    nested = extracted / "Design"
    candidates = [nested, extracted] if nested.is_dir() else [extracted]
    last_error: BootstrapError | None = None
    for candidate in candidates:
        try:
            validate_design_bank(candidate)
            return candidate
        except BootstrapError as exc:
            last_error = exc
    assert last_error is not None
    raise last_error


def resolve_design_target(explicit: Path | None = None) -> Path:
    if explicit is not None:
        target = explicit.expanduser()
    else:
        canonical = os.environ.get("OPENCODE_DESIGN_BANK")
        if canonical:
            target = Path(canonical).expanduser()
        else:
            target = Path()
            pointer = he_dir() / "config" / "design-bank.json"
            if pointer.is_file() and not pointer.is_symlink():
                try:
                    payload = json.loads(pointer.read_text(encoding="utf-8"))
                except (OSError, UnicodeDecodeError, json.JSONDecodeError):
                    payload = None
                root = payload.get("root") if isinstance(payload, dict) else None
                if isinstance(root, str) and root:
                    target = Path(root).expanduser()
            if target == Path():
                target = home() / "Design"
    target = target.absolute()
    if target in {Path("/"), home().absolute()}:
        raise BootstrapError("PREFLIGHT", "unsafe Design Bank target", code="TARGET_UNSAFE")
    return target


def _write_design_bank_pointer(target: Path, source: BootstrapSource) -> None:
    write_json(
        he_dir() / "config" / "design-bank.json",
        {
            "root": str(target),
            "catalogs": [str(path) for path in REQUIRED_CATALOGS.values()],
            "source": source.name,
            "bankVersion": source.bank_version,
            "ownership": "user-data",
        },
    )


def _populate_design_v2(
    design_root: Path,
    design_v2_root: Path,
    *,
    skip_rebuild: bool,
    stage: StageReporter,
) -> dict[str, Any]:
    try:
        ingested = [
            ingest_path(design_root, design_v2_root, provider="bank-pointer"),
            ingest_path(design_root / "21st", design_v2_root, provider="21st"),
            ingest_path(design_root / "aura", design_v2_root, provider="aura"),
        ]
        if any(result.get("copied_media") is not False for result in ingested):
            raise BootstrapError("INGESTED", "pointer ingest copied media", code="MEDIA_COPY_DETECTED")
    except BootstrapError:
        raise
    except Exception as exc:
        code = exc.code if isinstance(exc, DesignV2Error) else "INGEST_FAILED"
        raise BootstrapError("INGESTED", str(exc) or type(exc).__name__, code=code) from exc
    ingested_count = sum(int(result.get("count") or 0) for result in ingested)
    stage("INGESTED", str(ingested_count))
    try:
        dedupe_result = dedupe(design_v2_root)
    except Exception as exc:
        code = exc.code if isinstance(exc, DesignV2Error) else "DEDUPE_FAILED"
        raise BootstrapError("DEDUPED", str(exc) or type(exc).__name__, code=code) from exc
    stage("DEDUPED", str(dedupe_result.get("marked", 0)))
    payload: dict[str, Any] = {
        "ingested": ingested,
        "ingested_count": ingested_count,
        "dedupe": dedupe_result,
        "media_copied": 0,
    }
    if skip_rebuild:
        payload["rebuild"] = {"status": "skipped"}
        payload["doctor"] = {"status": "skipped"}
        return payload
    try:
        rebuild_result = rebuild(design_v2_root)
    except Exception as exc:
        code = exc.code if isinstance(exc, DesignV2Error) else "REBUILD_FAILED"
        raise BootstrapError("REBUILT", str(exc) or type(exc).__name__, code=code) from exc
    stage("REBUILT", str(rebuild_result.get("item_count", 0)))
    try:
        rows = doctor_rows(design_v2_root)
        if any(status == "FAIL" for status, _label, _evidence in rows):
            raise BootstrapError("DOCTOR_PASS", "DesignV2 doctor failed", code="DESIGN_V2_DOCTOR_FAILED")
        health = bank_health(design_v2_root)
    except BootstrapError:
        raise
    except Exception as exc:
        code = exc.code if isinstance(exc, DesignV2Error) else "DESIGN_V2_DOCTOR_FAILED"
        raise BootstrapError("DOCTOR_PASS", str(exc) or type(exc).__name__, code=code) from exc
    stage("DOCTOR_PASS", str(health.get("broken_pointers")))
    fts = health.get("fts") if isinstance(health.get("fts"), dict) else {}
    payload.update(
        {
            "rebuild": rebuild_result,
            "doctor": {"status": "pass", "checks": rows},
            "cards": health.get("total_assets"),
            "fts": fts,
            "broken_pointers": health.get("broken_pointers"),
        }
    )
    return payload


def bootstrap_design_bank(
    *,
    source_name: str | None = None,
    target: Path | None = None,
    design_v2_root: Path | None = None,
    dry_run: bool = False,
    download_only: bool = False,
    skip_rebuild: bool = False,
    config_path: Path | None = None,
    cache_dir: Path | None = None,
    downloader: Downloader = download_public_file,
    report: StageReporter | None = None,
) -> dict[str, Any]:
    stages: list[dict[str, str]] = []

    def stage(name: str, evidence: str = "") -> None:
        stages.append({"stage": name, "evidence": evidence})
        if report:
            report(name, evidence)

    stage("PREFLIGHT")
    design_target = resolve_design_target(target)
    v2_root = design_v2_root or resolve_design_v2_root()
    existing = False
    validation: dict[str, Any] | None = None
    if (design_target.exists() or design_target.is_symlink()) and not download_only:
        try:
            validation = validate_design_bank(design_target)
        except BootstrapError as exc:
            raise BootstrapError(
                "PREFLIGHT", "target exists but is not a compatible Design Bank", code="TARGET_EXISTS"
            ) from exc
        existing = True
        stage("BANK_VALIDATED", "already-present")
        stage("BANK_COMMITTED", "already-present")

    if existing:
        source = resolve_bootstrap_source(source_name, config_path=config_path)
        archive_url: str | None = None
        download_method = "curl-google-drive-public"
    else:
        source, archive_url, download_method = select_remote_source(source_name, config_path=config_path)
    stage("SOURCE_RESOLVED", source.name)
    if dry_run:
        stage("COMPLETE", "dry-run")
        return {
            "schema_version": 1,
            "action": "bootstrap",
            "status": "dry_run",
            "source": source.name,
            "source_type": source.source_type,
            "target": str(design_target),
            "design_v2_root": str(v2_root),
            "download_method": download_method,
            "stages": stages,
        }

    cache = cache_dir or share_dir() / "cache" / "design-bootstrap" / source.name
    archive = cache / source.archive_name
    checksum_file = cache / f"{source.archive_name}.sha256"
    archive_stats: dict[str, int] | None = None
    expected: str | None = None
    if not existing or download_only:
        if cache.is_symlink() or (cache.exists() and not cache.is_dir()):
            raise BootstrapError("PREFLIGHT", "bootstrap cache is not a safe directory", code="CACHE_UNSAFE")
        cache.mkdir(parents=True, exist_ok=True)
        if source.checksum_file_id:
            if checksum_file.is_symlink():
                checksum_file.unlink()
            if not checksum_file.is_file():
                try:
                    downloader(google_drive_public_url(source.checksum_file_id), checksum_file)
                except BootstrapError as exc:
                    if exc.stage == "PREFLIGHT":
                        raise
                    raise BootstrapError("CHECKSUM_FETCHED", exc.detail, code=exc.code) from exc
                except Exception as exc:
                    raise BootstrapError("CHECKSUM_FETCHED", str(exc), code="DOWNLOAD_FAILED") from exc
            try:
                expected = parse_checksum(checksum_file.read_text(encoding="utf-8"), source.archive_name)
            except BootstrapError:
                checksum_file.unlink(missing_ok=True)
                raise
            except (OSError, UnicodeDecodeError) as exc:
                checksum_file.unlink(missing_ok=True)
                raise BootstrapError("CHECKSUM_FETCHED", "checksum is unreadable", code="CHECKSUM_INVALID") from exc
            if source.pinned_sha256 and expected != source.pinned_sha256:
                raise BootstrapError(
                    "CHECKSUM_FETCHED", "checksum does not match pinned digest", code="CHECKSUM_MISMATCH"
                )
        else:
            expected = source.pinned_sha256
            if not expected:
                raise BootstrapError("SOURCE_RESOLVED", "SHA-256 is required", code="SHA256_REQUIRED")
        stage("CHECKSUM_FETCHED", expected)

        cached_ok = archive.is_file() and not archive.is_symlink() and sha256_file(archive) == expected
        if not cached_ok:
            archive.unlink(missing_ok=True)
            fetch_url = archive_url or google_drive_public_url(source.archive_file_id)
            try:
                downloader(fetch_url, archive)
            except BootstrapError:
                raise
            except Exception as exc:
                raise BootstrapError("ARCHIVE_DOWNLOADED", str(exc), code="DOWNLOAD_FAILED") from exc
        stage("ARCHIVE_DOWNLOADED", "cache" if cached_ok else "network")
        actual = sha256_file(archive)
        if actual != expected:
            archive.unlink(missing_ok=True)
            raise BootstrapError("ARCHIVE_VERIFIED", "archive SHA-256 mismatch", code="CHECKSUM_MISMATCH")
        stage("ARCHIVE_VERIFIED", actual)
        try:
            archive_stats = inspect_bootstrap_archive(archive)
        except BootstrapError:
            archive.unlink(missing_ok=True)
            raise
        stage("ARCHIVE_INSPECTED", json.dumps(archive_stats, sort_keys=True, separators=(",", ":")))
        if download_only:
            stage("COMPLETE", "download-only")
            return {
                "schema_version": 1,
                "action": "bootstrap",
                "status": "downloaded",
                "source": source.name,
                "archive": str(archive),
                "sha256": actual,
                "archive_stats": archive_stats,
                "stages": stages,
            }

    if not existing:
        assert expected is not None
        design_target.parent.mkdir(parents=True, exist_ok=True)
        workspace = Path(tempfile.mkdtemp(prefix=".opencode-design-bootstrap-", dir=str(design_target.parent)))
        extracted = workspace / "extract"
        try:
            safe_extract_bootstrap_archive(archive, extracted)
            stage("EXTRACTED_TO_TEMP", str(extracted))
            normalized = normalize_extracted_bank(extracted)
            validation = validate_design_bank(normalized)
            stage("BANK_VALIDATED", json.dumps(validation["counts"], sort_keys=True, separators=(",", ":")))
            if design_target.exists() or design_target.is_symlink():
                raise BootstrapError("BANK_COMMITTED", "target appeared during bootstrap", code="TARGET_EXISTS")
            try:
                os.replace(normalized, design_target)
            except OSError as exc:
                raise BootstrapError("BANK_COMMITTED", type(exc).__name__, code="BANK_COMMIT_FAILED") from exc
            stage("BANK_COMMITTED", str(design_target))
        finally:
            shutil.rmtree(workspace, ignore_errors=True)
    assert validation is not None
    _write_design_bank_pointer(design_target, source)
    if not existing:
        archive.unlink(missing_ok=True)
        checksum_file.unlink(missing_ok=True)
        try:
            cache.rmdir()
        except OSError:
            pass

    population = _populate_design_v2(design_target, v2_root, skip_rebuild=skip_rebuild, stage=stage)
    if skip_rebuild:
        stage("COMPLETE", "skip-rebuild")
    else:
        stage("COMPLETE")
    return {
        "schema_version": 1,
        "action": "bootstrap",
        "status": "already_present" if existing else "ok",
        "source": source.name,
        "target": str(design_target),
        "design_v2_root": str(v2_root),
        "bank": validation,
        "archive_stats": archive_stats,
        "population": population,
        "fts_schema_expected": FTS_SCHEMA_VERSION,
        "stages": stages,
    }
