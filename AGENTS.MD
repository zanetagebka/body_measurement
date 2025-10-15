# AGENTS Guidelines

Purpose: Establish shared, concise rules for writing clear, testable, and maintainable Python code in this repository. Prefer simplicity over cleverness. Optimize for readability and long‑term change.

## Core Principles
- DRY: Don’t Repeat Yourself. Extract shared logic; avoid copy/paste.
- KISS: Keep It Simple. Prefer straightforward solutions over abstractions.
- YAGNI: Don’t build for hypothetical futures; add only when needed.
- Single Responsibility: Each module/class/function does one thing well.
- Readability First: Code is for humans. Explicit > implicit; clear > terse.
- Pure Functions: Prefer side‑effect free logic where practical.
- Fail Fast: Validate inputs early and raise actionable errors.

## Code Style
- PEP 8: Follow Python’s style guide (line length 100–120 if project uses it).
- Typing: Use type hints (PEP 484) everywhere; enable strict type checking.
- Docstrings: Use PEP 257. Public functions/classes need concise docstrings.
- Naming: Descriptive, consistent names. Avoid abbreviations; no magic numbers.
- Small Units: Functions < ~40 lines; modules cohesive; break up complexity.
- Immutability: Favor dataclasses with `frozen=True` for value objects.
- Public API: Keep internal details private (leading underscore) and stable APIs documented.

## Project Structure
- Clear Packages: Group by domain, not layer when it helps maintainability.
- `__init__.py`: Keep minimal; avoid heavy imports at package import time.
- Configuration: 12‑factor friendly. Use environment variables; provide `.env.sample`.
- Separations: Keep domain logic separate from I/O, frameworks, and UI.

## Testing & TDD
- TDD Mindset: Write (or at least outline) tests first for new behavior.
- Test Pyramid: Unit > integration > end‑to‑end; cover critical paths.
- Pytest: Prefer `pytest` with fixtures and parametrization; avoid global state.
- AAA Pattern: Arrange, Act, Assert; one behavior per test.
- Coverage: Target ≥ 90% on changed code; don’t chase meaningless 100%.
- Fast & Deterministic: No sleeps or network in unit tests; use fakes.
- Property Tests: Consider `hypothesis` for core invariants.

## Tooling
- Formatting: `black` (or `ruff format`) for consistent, automated formatting.
- Linting: `ruff` (or `flake8`) with sensible error set; fix, don’t ignore.
- Types: `mypy --strict` (or pyright) on CI; annotate public boundaries.
- Pre‑commit: Enforce format/lint/type checks before commit.
- Imports: `isort` rules (or ruff) for deterministic ordering.

## Error Handling & Logging
- Don’t Swallow: Catch only when adding context or recovery; re‑raise otherwise.
- Custom Exceptions: Model domain errors with clear names and messages.
- Logging: Use `logging` with structured context; no `print` in production code.
- Levels: INFO for lifecycle, DEBUG for diagnostics, WARNING/ERROR for actionable issues.

## Performance & Reliability
- Complexity: Be mindful of Big‑O on hot paths; measure before optimizing.
- Memory: Stream/iterate large data; avoid loading everything into memory.
- Timeouts & Retries: Use sane defaults with jitter; avoid infinite waits.
- Idempotency: Make operations safe to retry where possible.

## Security
- Secrets: Never commit secrets. Use env vars or a secret manager.
- Input Validation: Validate and sanitize all external inputs.
- Dependencies: Pin and regularly update; avoid unmaintained packages.
- Static Analysis: Run `bandit` (or equivalent) for security checks in CI.

## Dependencies & Packaging
- Minimal Set: Prefer standard library when reasonable; justify new deps.
- Pinning: Use lockfiles (`pip‑tools` or Poetry) for reproducible builds.
- Boundaries: Import dependencies at edges; keep core domain decoupled.

## Data, Time, and I/O
- Serialization: Use explicit schemas (pydantic/dataclasses + marshaling) for boundaries.
- Time: Always timezone‑aware UTC internally; only localize at presentation.
- Numeric: Be explicit with decimal precision for money and measurements.

## API & CLI Design
- Backwards Compatibility: Version public APIs; deprecate with notices and tests.
- Helpful Errors: Clear, actionable messages for users; avoid leaking internals.
- CLI UX: Provide `--help`, sensible defaults, and safe behaviors by default.

## Documentation
- READMEs: Keep setup, run, and troubleshooting instructions current.
- Docstrings: Describe purpose, parameters, return types, and raised exceptions.
- Changelogs: Summarize meaningful changes; note breaking changes visibly.

## Git & Reviews
- Small PRs: Prefer focused, reviewable changes with passing checks.
- Conventional Commits: `feat:`, `fix:`, `refactor:`, `test:`, `docs:`, etc.
- Code Review: Discuss intent, correctness, readability, and test coverage.
- CI Required: Format, lint, types, tests must pass before merge.

## UI/UX Notes
- Consistency: Keep components and patterns consistent across the app.
- Accessibility: Labels, keyboard navigation, and color contrast matter.
- Feedback: Show progress/errors; avoid silent failures and jarring changes.
- Performance: Fast first paint and interactions; avoid blocking operations.

## How to Propose Changes
1) Open an issue describing the problem and desired outcome.
2) Draft a small PR with tests and docs; reference the issue.
3) Ensure pre‑commit passes locally; request review.
4) Address feedback promptly; keep commits focused and meaningful.

By contributing, you agree to uphold these guidelines to keep the codebase healthy, change‑friendly, and a pleasure to work in.

