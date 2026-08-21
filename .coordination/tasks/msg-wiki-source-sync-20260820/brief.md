# Task brief: MSG Wiki source sync

## Objective

將使用者指定的 GitLab Wiki（`https://gitlab.etzone.net/OB/Message-Backend/wikis/home`）完整拉取為 rule-base 的 MSG 原始來源，保留可追溯的頁面、附件／圖片與來源資訊，並更新 MSG source manifest。

## Role and ownership

- Coordinator: current Codex pane (`w1:p1`)
- Unique writer: one visible Herdr worker in the assigned pane
- Reviewer: a separate visible Herdr worker after writer handoff
- Handoff: writer must write this task's `report.md`; reviewer must write this task's `review.md`

## Workspace-relative task path

`.coordination/tasks/msg-wiki-source-sync-20260820/`

## In scope

- Inspect the existing `data/sources/msg/` layout and source-manifest conventions.
- Fetch the specified GitLab Wiki using the least destructive read-only method available (prefer the wiki Git repository if accessible).
- Add the complete fetched Wiki content under `data/sources/msg/` in a clearly named directory or files; preserve page filenames, attachments and binary assets as applicable.
- Add a concise provenance/readme file if needed so the source URL, fetch timestamp, retrieval method and limitations are explicit.
- Update `data/sources/manifest.json` only for the new Wiki source entries and any directly required manifest metadata.
- Run scoped checks: source completeness/counts, file/hash or repository revision evidence, JSON validity, sensitive-data scan appropriate to source ingestion, `git diff --check`, and confirm no unrelated tracked/untracked files were modified.
- Write `.coordination/tasks/msg-wiki-source-sync-20260820/report.md` with exact files, evidence, checks, limitations, runtime/external-operation boundary, and a completion marker.

## Out of scope

- Do not edit existing MSG PDFs, Redmine snapshots, website menu data, requirements, operations or test documents.
- Do not reorganize, summarize, translate or interpret Wiki content beyond provenance metadata.
- Do not modify source code or the upstream GitLab Wiki.
- Do not commit, push, deploy, restart services, change secrets/credentials, or rewrite Git history.
- Do not delete or overwrite unrelated dirty/untracked work.

## Unique facts and constraints

- Target repository: `/home/art/openab-repos/rule-base`.
- Canonical source directory: `data/sources/msg/`.
- Existing worktree is intentionally dirty; preserve all pre-existing changes and scope the diff precisely.
- Treat Wiki content as source-only/historical unless runtime verification exists; do not claim current deployment state.
- Never include credentials, tokens, cookies or private keys in committed source/provenance files.
- If GitLab access is unavailable or the Wiki is not fetchable, stop safely and record the exact blocker in `report.md` instead of inventing content.

## Acceptance criteria

1. The requested Wiki is fetched successfully, or the report proves a concrete access blocker.
2. If fetched, all retrievable Wiki pages and associated assets are present under `data/sources/msg/` with no silent omissions; inaccessible/non-versioned items are listed explicitly.
3. Provenance identifies the source URL, retrieval URL/method, retrieval time, and revision or content hash where available.
4. `data/sources/manifest.json` remains valid and maps new source content to an appropriate provenance/readme entry without disturbing unrelated entries.
5. Scoped checks pass, and the report distinguishes source-only evidence from runtime/deployment evidence.
6. Writer's report has `Status: COMPLETE` only after the above are true; otherwise use `Status: BLOCKED` with evidence.

## Completion marker

End `report.md` with exactly one of:

- `Status: COMPLETE`
- `Status: BLOCKED`
