---
name: ai-researcher-project
title: AI-Researcher Project Operator
description: Operate AI-Researcher research workflows safely.
version: 0.1.0
author: Chris Ezadiensi and Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [research, machine-learning, experiments, paper-writing, ai-researcher]
    category: domain
    related_skills: [research-paper-writing, arxiv, codebase-inspection, systematic-debugging]
    requires_toolsets: [terminal, files]
---

# AI-Researcher Project Operator Skill

Use this skill to operate the local AI-Researcher project as a dedicated scientific agent. It covers environment checks, benchmark selection, Level 1 and Level 2 research runs, experiment review, and paper-generation handoff.

It does not invent research results. Treat every claim as provisional until supported by paper metadata, source code, logs, metrics, or a reproducible run.

## When to Use

Use this skill when the user asks to:

- configure or run the AI-Researcher project;
- turn reference papers into an ML research idea;
- implement and validate an ML idea through the project workflow;
- inspect failed research-agent, Docker, benchmark, or paper-agent runs;
- generate paper sections from completed AI-Researcher outputs.

## Prerequisites

Project root:

```text
/Volumes/ensiezadi/ensiezadi/AI-Researcher
```

Expected local pieces:

- Python environment at `.venv` with Python 3.11+.
- Project `.env` based on `.env.template`.
- Docker available for the research execution environment.
- Valid benchmark instance under `benchmark/final/<category>/<instance_id>.json`.
- LLM and search credentials configured through `.env` or the shell environment.

Prefer the structured Hermes tools from the `ai_researcher` toolset:

- `ai_researcher_preflight`
- `ai_researcher_run_plan`
- `ai_researcher_run_idea`
- `ai_researcher_write_paper`
- `ai_researcher_run_status`

Use `terminal` for fallback commands, `read_file` for source/config inspection, and `patch` only when changing project files.

## How to Run

Start every session with `ai_researcher_preflight` unless the user explicitly asks only for reading or planning.

CLI fallback:

```bash
cd /Volumes/ensiezadi/ensiezadi/AI-Researcher
source .venv/bin/activate
python scripts/doctor.py
```

Launch the web interface:

```bash
cd /Volumes/ensiezadi/ensiezadi/AI-Researcher
source .venv/bin/activate
python web_ai_researcher.py
```

Level 1, detailed idea description: call `ai_researcher_run_plan` with `idea`, optional `references`, and benchmark fields. It returns a `run_id`; then poll with `ai_researcher_run_status`.

CLI fallback:

```bash
cd /Volumes/ensiezadi/ensiezadi/AI-Researcher/research_agent
source ../.venv/bin/activate
python run_infer_plan.py --instance_path ../benchmark/final/${CATEGORY}/${INSTANCE_ID}.json --container_name ${CONTAINER_NAME:-paper_eval} --task_level ${TASK_LEVEL:-task1} --model "$COMPLETION_MODEL" --workplace_name ${WORKPLACE_NAME:-workplace} --cache_path ${CACHE_PATH:-cache} --port ${PORT:-7020} --max_iter_times ${MAX_ITER_TIMES:-0} --category ${CATEGORY}
```

Level 2, reference-based ideation: call `ai_researcher_run_idea` with `references` and benchmark fields. It returns a `run_id`; then poll with `ai_researcher_run_status`.

CLI fallback:

```bash
cd /Volumes/ensiezadi/ensiezadi/AI-Researcher/research_agent
source ../.venv/bin/activate
python run_infer_idea.py --instance_path ../benchmark/final/${CATEGORY}/${INSTANCE_ID}.json --container_name ${CONTAINER_NAME:-paper_eval} --model "$COMPLETION_MODEL" --workplace_name ${WORKPLACE_NAME:-workplace} --cache_path ${CACHE_PATH:-cache} --port ${PORT:-7020} --max_iter_times ${MAX_ITER_TIMES:-0} --category ${CATEGORY}
```

Paper-generation handoff: call `ai_researcher_write_paper` with `category` and `instance_id`.

CLI fallback:

```bash
cd /Volumes/ensiezadi/ensiezadi/AI-Researcher
source .venv/bin/activate
python -m paper_agent.cli
```

## Quick Reference

Benchmark categories:

```text
diffu_flow, gnn, reasoning, recommendation, vq
```

Known instance examples:

```text
vq/one_layer_vq.json
gnn/gnn_nodeformer.json
recommendation/dccf.json
diffu_flow/con_flowmatching.json
reasoning/self_discover.json
```

Important files:

```text
README.md
.env.template
scripts/doctor.py
main_ai_researcher.py
research_agent/run_infer_plan.py
research_agent/run_infer_idea.py
paper_agent/writing.py
benchmark/final/
logs/
```

## Procedure

1. Classify the request as setup, Level 1, Level 2, debugging, analysis, or writing.
2. Inspect `README.md`, `.env.template`, the selected benchmark JSON, and the relevant entry script when context is missing.
3. Run `scripts/doctor.py` before long-running workflows.
4. Confirm `CATEGORY`, `INSTANCE_ID`, `TASK_LEVEL`, `PORT`, `CONTAINER_NAME`, `COMPLETION_MODEL`, and `CHEEP_MODEL`.
5. For Level 1, ask for or locate the detailed idea text and reference list, then use `ai_researcher_run_plan`.
6. For Level 2, ask for or locate reference papers, then use `ai_researcher_run_idea`.
7. After a run starts, keep the `run_id` and inspect it with `ai_researcher_run_status` before summarizing results.
8. For paper writing, only draft sections from verified outputs, logs, implementation details, and source papers.

## Pitfalls

- `readlink -f` in shipped shell scripts is Linux-oriented; on macOS prefer direct Python entry commands from the project root or `research_agent` directory.
- Do not run long workflows with placeholder keys in `.env`.
- Ports can collide across runs; check the selected `PORT` before starting another container-backed workflow.
- The project may use actual datasets and Docker images; budget time, disk, network, and GPU availability before launching.
- Do not treat generated ideas, benchmark scores, or paper sections as true until logs and artifacts are checked.

## Verification

A configured profile is healthy when:

- `hermes -p ai-researcher chat` starts with this profile.
- `/profile` reports `ai-researcher`.
- `pwd` inside `terminal` defaults to `/Volumes/ensiezadi/ensiezadi/AI-Researcher`.
- `python scripts/doctor.py` passes or reports only explicit external blockers such as missing Docker or placeholder credentials.
- The selected benchmark file exists under `benchmark/final/<category>/<instance_id>.json`.
