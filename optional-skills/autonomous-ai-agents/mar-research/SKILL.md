---
name: mar-research
description: Run a staged MAR research workflow.
version: 0.1.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Autonomous-AI-Agents, Research, MAR, Judge, State-Machine]
    related_skills: [hermes-agent]
---

# MAR Research Workflow

Use this skill to run a staged medical image artifact reduction research workflow. It is a controller layer for research execution, not the medical model itself. The workflow separates intake, survey, idea selection, protocol design, implementation, judge review, and paper writing so each stage can be resumed and audited independently.

## When to Use

- Turning a MAR idea into a controlled research plan.
- Reviewing a set of MAR papers and extracting candidate directions.
- Designing a minimal experiment protocol with explicit safety checks.
- Reviewing an implementation for novelty, medical validity, and experiment quality.
- Converting verified research outputs into paper-ready material.

## Prerequisites

- Hermes Agent with access to the usual coding tools.
- Recommended tools for this workflow: `memory`, `clarify`, `delegate_task`, `terminal`, `read_file`, `create_file`, and `apply_patch`.
- A local working state directory with the templates in `state/`.

## How to Run

Load this skill when the task is about MAR research strategy or coordination. Start by reading `state/research_state.yaml` and `state/current_task.md`, then use the controller prompt to decide whether the task belongs in intake, survey, idea, protocol, ML, judge, or paper.

Example operating pattern:

1. Read the current state.
2. Classify the request into one stage.
3. Produce the stage artifact.
4. Write the result into `decision_log.md`.
5. If the stage is judged incomplete, return to the earliest safe stage instead of jumping ahead.

## Quick Reference

| Stage | Purpose | Output |
|---|---|---|
| Intake | Normalize the user request | Task framing and scope |
| Survey | Gather papers, code, and benchmark evidence | Evidence matrix |
| Idea | Generate and filter candidate directions | Shortlist of ideas |
| Protocol | Freeze the experiment design | Dataset, metrics, and evaluation plan |
| ML | Implement the agreed plan | Code changes and runnable pipeline |
| Judge | Check novelty, safety, and validity | Verdict and required fixes |
| Paper | Turn validated work into writing material | Section drafts and figure notes |

## Procedure

1. Start in Intake and record the user goal in `state/current_task.md`.
2. Run Survey only after the question is clear enough to investigate.
3. Use Idea to produce candidate directions, then reduce them to the smallest testable one.
4. Use Protocol to freeze dataset choice, metrics, and safety checks before implementation begins.
5. Delegate implementation to ML only after Protocol is stable.
6. Send the implementation to Judge before any paper drafting.
7. Write Paper artifacts only from verified results; do not invent new claims here.
8. Log every stage transition in `state/decision_log.md` so the flow can be resumed later.

## Pitfalls

- Do not jump directly from idea generation to paper writing.
- Do not let ML redefine the research question after the protocol is frozen.
- Do not treat appearance-only improvement as medical validity.
- Do not skip Judge when the workflow touches lesion retention, HU drift, or hallucination risk.
- Do not overwrite state without a log entry for the transition.

## Verification

- `state/research_state.yaml` exists and names the current stage.
- `state/current_task.md` captures the active objective and next action.
- `state/decision_log.md` records the latest stage decision.
- Controller and Judge prompts exist and can be loaded independently.
- A failed stage can be resumed from the latest recorded state without rerunning the entire workflow.