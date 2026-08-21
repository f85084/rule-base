# Task brief: MSG 一般人員操作手冊

## Objective

依 MSG Redmine 需求單整理結果與 `project-docs/projects/MSG/data/business-flows` 的 B2E L2／L3 業務流程，撰寫給一般 MSG 後台使用人員的繁體中文操作手冊，讓讀者能依工作任務找到入口、完成主要操作、判讀結果並知道異常時應先檢查什麼。

## Role and ownership

- Coordinator: current Codex pane (`w1:p1`)
- Unique writer: one visible interactive Codex worker in the existing shared `WORKERS` tab
- Reviewer: a different visible interactive Codex worker in the same shared `WORKERS` tab after writer handoff
- Handoff: writer writes `report.md`; reviewer writes `review.md`; coordinator performs final acceptance

## Workspace-relative task path

`.coordination/tasks/msg-general-user-manual-20260821/`

## Authorized scope

### Files the writer may create or edit

- `docs/msg/operations/一般人員操作手冊.md` — the canonical general-user manual.
- `docs/msg/README.md` — add the manual to the MSG navigation.
- `docs/README.md` — add or correct the top-level link if the current index exposes MSG operations.
- `.coordination/tasks/msg-general-user-manual-20260821/report.md` — writer evidence and handoff.

### Source of truth

- MSG Redmine snapshot and summary:
  - `data/sources/msg/redmine/issues_all.json`
  - `data/sources/msg/redmine/summary_all.md`
  - `docs/msg/requirements/README.md`
  - `docs/msg/requirements/page-classification-index.md`
  - `docs/msg/requirements/page-purpose-index.md`
  - `docs/msg/requirements/pages/*.md`
- MSG business-flow source:
  - `/home/art/openab-repos/project-docs/projects/MSG/data/business-flows/INDEX.md`
  - `B2E/L2/INDEX.md` and the linked B2E L2 page documents
  - `B2E/L3/INDEX.md` and all six linked B2E L3 solution documents
  - relevant B2E L1 files and `special/` files only when the L2/L3 source points to them
- Existing RuleBase navigation and operation documents:
  - `docs/msg/README.md`
  - `docs/msg/operations/message-operations.md`
  - `docs/msg/operations/check-in-stamp-setup.md`
  - `docs/msg/rules/README.md`
  - `docs/msg/troubleshooting/README.md`

## Content requirements

- Write for general B2E staff first; use task-oriented headings and plain language rather than controller/API terminology.
- Cover the ordinary work path for: sign-in and account readiness; customer conversation and assignment; customer lookup and tags; offline messages; message/template/media preparation; multicast or audience work; event/check-in operations; and reports or message query. Link to existing detailed pages when the source already has a dedicated document instead of copying unverified technical detail.
- Include a compact navigation table mapping each work task to the MSG page/route, relevant business-flow source, and related requirement classification. The table is an entry point, not a substitute for procedure details.
- For each covered task, state where to enter, the normal sequence, what success looks like, important prerequisites/permissions, side effects or irreversible-looking actions, and the first troubleshooting check.
- Distinguish source-backed current descriptions from historical, inferred, planned, or runtime-unknown behavior. Redmine status is a snapshot field, not proof that a feature is deployed or verified.
- Preserve the L3 business boundaries: login/security, real-time support and assignment, marketing content/broadcast, audience/tagging, interactive events/check-in, and streaming/statistics/cost monitoring.
- Explicitly identify administrative-only pages and technical-only flows that are not ordinary staff procedures, with links for escalation where appropriate.
- Do not reproduce credentials, tokens, private URLs, personal data, SQL initialization data, internal secrets, or full sensitive source contents. Refer to controlled environment information instead.
- Do not claim runtime behavior, permission matrices, retention periods, notifications, or successful deployment unless directly supported by the allowed sources; mark unknowns clearly.

## Out of scope

- Do not modify application source, project-docs, Redmine snapshots, source manifest, test files, requirement classification files, skills, or existing operation manuals other than the navigation links explicitly listed above.
- Do not rewrite or reorganize the six B2E L3 source documents.
- Do not create a separate API/developer manual, deployment guide, troubleshooting runbook, or B2C/WebAPI implementation guide.
- Do not commit, push, deploy, restart services, alter secrets, access private systems, or change external sources.
- Preserve all pre-existing dirty and untracked work in the repository; do not reset, checkout, clean, overwrite, or delete unrelated paths.

## Required checks

- Confirm every local Markdown link introduced or touched by this task resolves.
- Run `git diff --check`.
- Validate that the manual links to the canonical requirement/business-flow sources without hard-coded claims unsupported by them.
- Scan the new/edited files for credentials, tokens, private keys, and obvious personal-data leakage.
- Confirm the diff is limited to the authorized files plus this task's evidence files.

## Acceptance criteria

1. A readable general-user manual exists at `docs/msg/operations/一般人員操作手冊.md` and is navigable from the MSG index (and top-level index when applicable).
2. The manual covers the six B2E L3 work domains or clearly explains why a domain is administrative/technical and links the reader to the appropriate source.
3. Procedures are task-oriented, source-traceable, and distinguish current source descriptions from runtime-unknown or historical material.
4. The manual does not expose credentials, tokens, secrets, or unnecessary personal data.
5. Required checks pass and are recorded in `report.md`.
6. `report.md` lists exact files, evidence, checks, limitations, external operations not run, and ends with exactly one `Status: COMPLETE` or `Status: BLOCKED` marker.

## Reviewer handoff

After the writer submits `report.md`, an independent reviewer in another visible Panel must read this brief, the report, the full diff, the referenced manual sources, and the final files. The reviewer is read-only with respect to writer files and writes only this task's `review.md`, ending with exactly one `Status: PASS` or `Status: FINDINGS` marker.
