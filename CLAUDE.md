# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working in this repository.

## Purpose

- Experiment with GitHub automation agents and manage repositories via gh CLI.
- Automate GitHub operations (repo management, issues, PRs, releases) using the `gh_cli` skill.
- Build a codebase management workflow centered on the AI agent `Chunsik`.

## Tone

- Concise and clear.
- Professional and objective.
- Output results only — no filler or unnecessary modifiers.

## Format

- Commit messages: auto-generated, context-aware, accurately describing each change.
- Output: confirm only the executed commands and their result status.
- Skill reference: `~/.claude/skills/gh_cli.md`

## Skills

| Skill | Path | Description |
|-------|------|-------------|
| `gh_cli` | `~/.claude/skills/gh_cli.md` | Full GitHub CLI command reference |
| `card-news-maker` | `~/.claude/skills/card-news-maker.md` | Card news generator using Python Pillow |

## Connected Repository

- `com-dj-tech/ai_agent` — main experimental repository
