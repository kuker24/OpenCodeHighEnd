# Verification profiles

Read this file only after a verification profile is chosen. A missing command is `NOT_CONFIGURED`, not success. Required configured failures block a completion claim.

## FAST

Localized, low-risk edits.

When configured:

1. Project-native typecheck.
2. Tests targeted at the changed behavior.

## STANDARD

Normal feature work.

Run project-native typecheck, relevant unit or integration tests, and the build when it is materially affected. Run dependency or export checks only when the project already configures them. Add browser verification only for changed UI behavior.

## UI

Visual or interaction changes.

Run project-native typecheck and relevant tests, then the repository's configured browser or E2E workflow. Use `/playwright-qa` as the primary adapter for exploratory UI QA (or `/browser-act` when explicitly requested or configured for specific browser sessions). Use `/chrome-devtools-axi` only after an observed failure; DevTools attaches through background Chromium (`opencode-chromium-cdp` on `127.0.0.1:9223`). Playwright QA and BrowserAct manage their own isolated sessions. Run existing project test suites (Playwright Test, Cypress) for regression; do not initialize browser tooling or configs that the project does not already have.

## SECURITY

Auth, authorization, payments, uploads, webhooks, secrets, privileged routes, public APIs, or user-controlled external input.

Run relevant tests plus available deterministic scanners: `semgrep`, `osv-scanner`, `gitleaks`. Specialist reasoning produces hypotheses. Scanner and test output provide evidence. Do not print secret contents.

## PERFORMANCE

Use only for a measured performance concern.

1. Record a baseline metric.
2. Profile and identify the bottleneck.
3. Make the targeted change.
4. Measure the same metric again.
5. Run relevant regression tests.

Primary Core Web Vitals: LCP, INP, CLS. FID is legacy. Do not claim improvement without comparable before and after evidence.

## RELEASE

Run every configured release gate: typecheck, full tests, coverage, build, E2E, dependency or export checks, Semgrep, OSV-Scanner, Gitleaks, and pre-commit. Record unconfigured gates explicitly. Do not declare release success while a required configured gate fails.

## Mechanical completion & Done-gate

Before claiming "done", every required check appropriate to the chosen profile (FAST, STANDARD, UI, SECURITY, PERFORMANCE, RELEASE) must execute and pass.

Blocking evidence lives in a verifiable evidence ledger (concrete commands run, test exit codes, artifact paths, URLs inspected, or screenshots). When recording evidence rows (see `rules/decision-log-protocol.md`), results must strictly distinguish mechanical fact from advisory evaluation:
- `FACT: <outcome>` — blocking mechanical proof (e.g. `FACT: tests green`, `FACT: exit 0`, `FACT: build succeeded`). A done-gate cannot pass without verifiable FACT evidence.
- `JUDGMENT: <assessment>` — advisory model evaluation (e.g. `JUDGMENT: visual balance improved`). Advisory only; model judgment cannot override failed, missing, or inconclusive FACT evidence.

Do not claim done while a required configured gate is unrun. Missing project command = `NOT_CONFIGURED`, not PASS.

Distinguish mechanical facts (typecheck, tests, build actually ran) from reasoning quality (in-session review or `/matt-code-review`). Do not install Claude Code Stop hooks, learning-library mtime gates, or disk-space blockers. Those remain `FOREIGN_ON_DEMAND`.
