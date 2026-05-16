# Hooks Policy

This repository does not enable workspace hooks by default.

Use hooks only when they provide a deterministic, low-ambiguity benefit such as:
- validating a generated or edited file
- enforcing a protected-file rule
- running a formatter or lightweight consistency check
- blocking unsafe tool usage

Do not use hooks for:
- planning decisions
- interactive clarification
- open-ended documentation writing
- anything that should remain visible and user-directed in the chat flow

## Placement

Store workspace hook definitions in this folder as `.json` files.

## Design Rules

- Keep hook commands cross-platform where possible.
- Prefer repo-local scripts or commands over machine-specific paths.
- Keep side effects narrow and easy to explain.
- Avoid secrets, tokens, or environment-specific assumptions in hook configs.
- Document what the hook protects, when it runs, and how to disable it safely.

## Suggested First Hooks

If the repo later adopts hooks, start with one of these:
- protect generated project `docs/` outputs from manual edits
- protect shared `tools/yapp/YAPPgenerator_v3.scad` from accidental modification
- run a lightweight validation after customization files in `.github/` are edited

Use agent handoffs and structured ask-question prompts for workflow control. Use hooks for deterministic guardrails only.
