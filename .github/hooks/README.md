# Hooks Policy

This repository does not enable workspace hooks by default.

Hooks are part of the meta layer, not part of day-to-day project authoring. They should only be introduced when a deterministic protection is clearly better than ordinary instructions, validation commands, or reviewer checks.

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

## Before Adding A Hook

Ask these questions first:

1. Is the problem deterministic enough that a script can decide it correctly every time?
2. Would an instruction, prompt, reviewer step, or validation command solve the problem more transparently?
3. Is the hook protecting a narrow surface such as generated outputs, protected files, or a lightweight consistency rule?

If the answer to any of those is no, do not add a hook.

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

## Validation Expectations

- Document what the hook protects and why the hook exists.
- Keep failure messages short and actionable.
- Prefer repo-local scripts over inline machine-specific commands.
- Test the hook against both expected and failing cases before committing it.

Use agent handoffs and structured ask-question prompts for workflow control. Use hooks for deterministic guardrails only.
