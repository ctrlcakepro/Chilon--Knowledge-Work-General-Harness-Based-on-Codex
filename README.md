[README.md](https://github.com/user-attachments/files/29607338/README.md)
# Codex Harness Public

A layered Codex harness for long-term knowledge work, reusable workflows, project bootstrapping, and project-specific AGENTS generation.

This repository packages a public version of my Codex harness system. It is designed to make Codex behave less like a one-off chat assistant and more like a reusable working system for multi-project collaboration.

## What This Repository Includes

- `AGENTS.md`
  Global collaboration rules, task routing principles, delivery standards, and reliability boundaries.
- `knowledge-workbench/`
  A modular workbench for recurring workflows, including templates, playbooks, style guidance, quality gates, scoring, calibration, and benchmark routines.
- `skills/project-harness-bootstrap/`
  A reusable skill that turns a project description into project-root harness files such as `AGENTS.md` and `PROJECT-WORKFLOW.md`.

## What This Harness Tries To Do

- Keep the global layer small and stable.
- Push detailed workflows down into reusable modules instead of bloating top-level instructions.
- Help Codex ask fewer vague questions and move work forward more directly.
- Preserve output quality for writing, review, presentation, and structured knowledge work.
- Make it easier to start a new project with a usable project-level harness.

## Architecture

This harness uses a layered structure:

1. Global layer
   `AGENTS.md` holds stable cross-project rules such as collaboration style, task routing, delivery expectations, and reliability constraints.

2. Workbench layer
   `knowledge-workbench/` holds reusable building blocks:
   - `templates/` for common output structures
   - `playbooks/` for routing, delivery, quality, and failure recovery
   - `style/` for aesthetic direction and style translation
   - `architecture/` for rule precedence, scoring, and harness governance
   - `benchmarks/` for calibration and regression checks

3. Project layer
   Each project can define its own root `AGENTS.md` and `PROJECT-WORKFLOW.md` based on its actual purpose, outputs, and recurring workflows.

## Who This Is For

This repository is most useful if you use Codex for:

- knowledge work
- writing and revision
- research and review
- presentation and deck preparation
- multi-project workflow setup
- long-term agent collaboration

## Installation

Copy the files into your Codex home directory.

Recommended layout:

```text
~/.codex/
  AGENTS.md
  knowledge-workbench/
  skills/
    project-harness-bootstrap/
```

Install in this order:

1. Copy `AGENTS.md` into `~/.codex/AGENTS.md`
2. Copy `knowledge-workbench/` into `~/.codex/knowledge-workbench/`
3. Copy `skills/project-harness-bootstrap/` into `~/.codex/skills/project-harness-bootstrap/`

If you already have your own global `AGENTS.md`, merge carefully instead of overwriting blindly.

## Quick Start

After installation, the global harness will shape Codex behavior across projects.

For a new project, use the bootstrap skill with a short project description.

Example:

```text
Use $project-harness-bootstrap to create a project-root harness from this project description.

This is a research and writing project about...
The recurring tasks are...
The main deliverables are...
The preferred tools are...
Actions that require confirmation are...
```

Or in Chinese:

```text
用 $project-harness-bootstrap 根据下面这段项目描述，在项目根目录生成 AGENTS.md 和 PROJECT-WORKFLOW.md。

这个项目是做……
核心重复任务有……
主要交付物有……
希望优先使用的工具有……
需要确认的边界有……
```

## What The Bootstrap Skill Generates

By default, the skill creates or updates:

- `AGENTS.md`
  A project-specific Codex harness that changes behavior inside that project.
- `PROJECT-WORKFLOW.md`
  A human-readable quickstart and workflow map for the project.

The skill is designed to:

- inherit your global rules
- avoid duplicating the global harness
- keep project instructions compact
- turn project descriptions into usable workflows quickly

## Repository Structure

```text
codex-harness-public/
  AGENTS.md
  README.md
  knowledge-workbench/
    architecture/
    benchmarks/
    playbooks/
    questioning/
    style/
    templates/
  skills/
    project-harness-bootstrap/
      SKILL.md
      agents/
      references/
```

## Design Principles

- Keep the global layer small.
- Keep project workflows project-specific.
- Prefer routing over repetition.
- Prefer reusable playbooks over long top-level prompts.
- Prefer explicit delivery standards over vague quality language.
- Prefer repair loops and benchmarks over endlessly adding more rules.

## What Is Not Included

This public package intentionally excludes private local state such as:

- personal config files
- auth files
- plugin caches
- session data
- local databases
- API keys
- machine-specific automations

## Suggested Next Steps

If you want to publish this as your own repository, consider adding:

- a `LICENSE` file such as `MIT`
- a short `CHANGELOG.md`
- example project descriptions
- example generated project-level harness outputs

## Short Repository Description

If you need a GitHub repository description under 350 characters, you can use:

> A layered Codex harness for long-term knowledge work, reusable workflows, project bootstrapping, and project-specific AGENTS generation. Includes a global AGENTS.md, a modular knowledge-workbench, and a skill that turns project descriptions into project-root harness files.
