# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
uv sync --all-extras      # Install all dependencies
uv run pytest             # Run all tests
uv run ruff check .       # Lint
uv run mypy tstcls/       # Type check
```

## Architecture

tstcls is a single-class pytest plugin (`tstcls/__init__.py`) that provides `TestClassBase` — a base class for pytest test classes with automatic fixture injection into setup/teardown lifecycle methods.

Flow per test:
1. `init_class` fixture (scope="class", autouse) calls `setup_test_class(**fixtures)` before the class and `teardown_test_class(**fixtures)` after
2. `init` fixture (scope="function", autouse) calls `setup_test(**fixtures)` before each test and `teardown_test(**fixtures)` after
3. `find_fixtures(func, request)` inspects the function signature and resolves each arg name as a pytest fixture via `request.getfixturevalue(arg)`

Users subclass `TestClassBase` and override `setup_test` / `teardown_test` / `setup_test_class` / `teardown_test_class` with fixture names as parameters.

## Code Style

- No comments or docstrings — ever. Don't restate what code does; extract instead.
- No nested `if` — use fast returns.
- Imports at top of file only.
- Prefer `# noqa: RULE` inline comments over adding rules to `lint.ignore` in `pyproject.toml`.

## General

- Do not create example test files, do not create `.md` files to explain solutions.
- When changing something globally, work gradually — small steps without loading full context.
- Read `CLAUDE.local.md` if it exists for machine-specific context.

## Workflow

When the user corrects a workflow mistake (e.g., wrong command, missing `.gitignore` entries), save the correction here — CLAUDE.md is loaded every session and is the authoritative source for project rules.

## Unordered Notes

- When you want to run code to check if things work, create a test case instead and run pytest. This way you have a permanent record of the behavior.
- When running commands from root directory, NEVER run "cd && <command>", just run the command.
