# Body Measurements – TODO

Purpose: Prioritized, actionable tasks to improve code quality, security, UX, and maintainability. Keep PRs small and focused. Reference AGENTS.MD for guidelines.

## Now (High Priority)
- [ ] Repo hygiene and secrets
  - [ ] Untrack built folders from git index: `node_modules/`, `staticfiles/`
  - [x] Untrack built folders from git index: `node_modules/`, `staticfiles/`

- [ ] Messages UX
  - [ ] Ensure consistent styling and timed auto-dismiss for non-error messages

- [ ] Clean up after removing CSV import/export
  

## Next (Medium Priority)
- [ ] Database integrity
  - [ ] Add unique constraint for `(user, date)` in `Measurement` (migration)
  - [ ] Handle `IntegrityError` on create/update and present friendly message

- [ ] List/chart consistency
  - [ ] Decide on canonical order (asc for charts) and keep templates/JS aligned
  - [ ] Consider pagination for measurements table if datasets are large

- [ ] Frontend stack decision
  - [ ] Choose Bootstrap-only (default) OR Tailwind
    - If Bootstrap: remove Tailwind deps from `package.json`
    - If Tailwind: add build pipeline (postcss config, scripts), migrate styles

- [ ] Tests (pytest)
  - [ ] Configure pytest
  - [ ] Add unit tests: `Measurement.__str__`, field constraints, CSV parsing helpers
  - [ ] Add view tests: auth required, add, delete

- [ ] Tooling & CI
  - [ ] Add pre-commit hooks: `ruff`, `black`, `mypy` (gradual), `bandit`
  - [ ] Add GitHub Actions: lint, type-check, tests, coverage artifact
  - [ ] Pin dev dependencies in `requirements-dev.txt`

- [ ] i18n cleanup
  - [ ] Standardize on English msgids (or commit to current pattern) and update `.po` files
  - [ ] Use `blocktrans` for composed strings; ensure user-visible messages are translated

## Later (Backlog)
- [ ] Accessibility
  - [ ] Add aria labels and keyboard focus states; audit with axe or lighthouse
  - [ ] Ensure color contrast and focus visibility in all templates

- [ ] UX enhancements
  - [ ] Add inline validation on forms and helpful help_text
  - [ ] Add loading/progress states for import actions
  - [ ] Optional: client-side CSV validation preview

- [ ] Observability
  - [ ] Structure logging context; add error logging for import failures
  - [ ] Optional: sentry integration (env-gated)

- [ ] Docs
  - [ ] Add CONTRIBUTING.md linked to AGENTS.MD

## Acceptance Criteria (selected items)
- Repo hygiene: Sensitive files ignored, `.env.sample` present, repo clean on fresh clone.
- Settings: App starts in dev with console email; production fails fast without `SECRET_KEY`.
- Import: Decimal-safe, invalid numeric cells skipped gracefully, duplicates resolved per user choice.
- Messages: Success and error messages visible across flows (add, delete, import).
- Tests: Green CI with core view and import behaviors covered.
