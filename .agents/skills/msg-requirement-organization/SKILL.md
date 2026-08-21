---
name: msg-requirement-organization
description: Organize MSG Redmine requirements by the actual MSG menu and cross-reference non-page/shared or unresolved tickets with MSG business flows. Use when rebuilding or reviewing the MSG requirement index; keep unresolved tickets flagged for manual confirmation.
---

# Msg Requirement Organization

Use this skill only for the MSG requirement documentation under
`/home/art/openab-repos/rule-base`.

## Workflow

1. Read the current Redmine snapshot at `data/sources/msg/redmine/issues_all.json`
   and the user-provided menu at `data/sources/msg/website-menus.json`.
2. Read the relevant MSG business-flow indexes under
   `/home/art/openab-repos/project-docs/projects/MSG/data/business-flows`.
   Start with `INDEX.md`, `B2E/L3/INDEX.md`, `special/INDEX.md`, then follow
   the L3/L1 documents needed by the ticket group.
3. Rebuild the menu classification with:

   ```bash
   python3 scripts/classify-msg-by-website-menu.py
   ```

   The classifier is the source of truth for menu-page assignment, menu sort
   order, and evidence. It compares the title before the description.
4. Rebuild the two cross-cutting documents with:

   ```bash
   python3 scripts/enrich-msg-cross-cutting-requirements.py
   ```

   This keeps `98-非頁面-共用功能.md` grouped by business flow and adds source
   documents. It keeps `99-待人工確認頁面.md` unresolved, adding only candidate
   flows, reasons, and references.
5. Do not force a ticket into a visible menu page merely because a keyword is
   similar. If the page cannot be established from the ticket and the MSG
   flow documents, leave it in 99.

## Required invariants

- Preserve every Redmine issue exactly once across the generated categories.
- Keep the original issue ID, title, project, tracker, status, assignee,
  created date, and classification evidence.
- Treat project-docs business flows as traceability references, not proof that
  a requirement is implemented or tested. Current code and environment
  behavior takes precedence.
- Do not call Redmine write APIs, edit Redmine issues, scrub user-approved
  test data, commit, or push unless the user separately requests it.
- Keep external project-docs references as readable links or paths; do not
  copy their full contents into rule-base.

For the routing table and conservative handling of ambiguous tickets, read
[MSG business-flow routing](references/msg-business-flow-routing.md).

## Validation

After regeneration, check the issue totals and uniqueness, then run:

```bash
python3 -m py_compile scripts/classify-msg-by-website-menu.py scripts/enrich-msg-cross-cutting-requirements.py
python3 scripts/check-source-status.py --all
git diff --check
```

Also verify that links in `docs/msg/requirements/` resolve and that 99 still
explicitly says “待人工確認” for every unresolved ticket.
