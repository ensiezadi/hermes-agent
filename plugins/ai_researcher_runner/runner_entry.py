from __future__ import annotations

import argparse
import asyncio
import json
import os
from pathlib import Path
import sys


DEFAULT_PROJECT_ROOT = Path("/Volumes/ensiezadi/ensiezadi/AI-Researcher")
PROJECT_ROOT = Path(os.getenv("AI_RESEARCHER_PROJECT_ROOT", str(DEFAULT_PROJECT_ROOT))).expanduser()


def _load_dotenv() -> None:
    try:
        from dotenv import load_dotenv
    except Exception:
        return
    load_dotenv(PROJECT_ROOT / ".env", override=False)


def _make_research_args(payload: dict):
    category = payload["category"]
    instance_id = payload["instance_id"]
    return argparse.Namespace(
        instance_path=str(PROJECT_ROOT / "benchmark" / "final" / category / f"{instance_id}.json"),
        container_name=payload.get("container_name") or os.getenv("CONTAINER_NAME", "paper_eval"),
        task_level=payload.get("task_level") or os.getenv("TASK_LEVEL", "task1"),
        model=payload.get("model") or os.getenv("COMPLETION_MODEL", "openai/MiniMax-M2.7"),
        workplace_name=payload.get("workplace_name") or os.getenv("WORKPLACE_NAME", "workplace"),
        cache_path=payload.get("cache_path") or os.getenv("CACHE_PATH", "cache"),
        port=int(payload.get("port") or os.getenv("PORT", "7020")),
        max_iter_times=int(payload.get("max_iter_times") or os.getenv("MAX_ITER_TIMES", "0")),
        category=category,
    )


def _apply_env_overrides(payload: dict) -> None:
    overrides = payload.get("env") or {}
    for key, value in overrides.items():
        if value is None:
            continue
        os.environ[str(key)] = str(value)


def run_plan(payload: dict) -> None:
    from research_agent import run_infer_plan

    args = _make_research_args(payload)
    idea = payload.get("idea") or ""
    references = payload.get("references") or ""
    run_infer_plan.main(args, idea, references)


def run_idea(payload: dict) -> None:
    from research_agent import run_infer_idea

    args = _make_research_args(payload)
    references = payload.get("references") or ""
    run_infer_idea.main(args, references)


def write_paper(payload: dict) -> None:
    from paper_agent import writing

    category = payload["category"]
    instance_id = payload["instance_id"]
    asyncio.run(writing.writing(category, instance_id))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("workflow", choices=["plan", "idea", "paper"])
    parser.add_argument("payload_path")
    args = parser.parse_args()

    os.chdir(PROJECT_ROOT)
    sys.path.insert(0, str(PROJECT_ROOT))
    _load_dotenv()

    payload = json.loads(Path(args.payload_path).read_text(encoding="utf-8"))
    _apply_env_overrides(payload)

    if args.workflow == "plan":
        run_plan(payload)
    elif args.workflow == "idea":
        run_idea(payload)
    elif args.workflow == "paper":
        write_paper(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
