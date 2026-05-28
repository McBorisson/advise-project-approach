# Security Policy

## Supported Versions

The latest tagged release is the supported version.

## Reporting Issues

If you find a security issue, please open a GitHub issue with enough detail to reproduce or understand the risk. If the issue involves sensitive information, avoid posting secrets, private repository contents, tokens, or proprietary code.

## Security Scope

This skill is designed to be read-only by default. Security-relevant reports include:

- instructions that could cause the agent to expose secrets
- instructions that could cause destructive file, git, or deployment actions without explicit user approval
- prompt-injection weaknesses in the review workflow
- misleading install/package instructions
- packaged `.skill` contents that differ from the source folder

## Package Safety

The packaged skill currently contains only:

```text
advise-project-approach/SKILL.md
advise-project-approach/agents/openai.yaml
```

It does not include executable scripts. If that changes in the future, the README, contributing guide, release notes, and validation notes should call it out explicitly.
