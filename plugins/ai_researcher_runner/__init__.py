from __future__ import annotations

import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
from typing import Any

from hermes_constants import get_hermes_home


DEFAULT_PROJECT_ROOT = Path("/Volumes/ensiezadi/ensiezadi/AI-Researcher")
PROJECT_ROOT = Path(os.getenv("AI_RESEARCHER_PROJECT_ROOT", str(DEFAULT_PROJECT_ROOT))).expanduser()
RUNS_ROOT = Path(get_hermes_home()) / "ai_researcher_runs"
PLUGIN_DIR = Path(__file__).resolve().parent


def _json(data: dict[str, Any]) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2)


def _project_python() -> str:
    candidate = PROJECT_ROOT / ".venv" / "bin" / "python"
    if candidate.exists():
        return str(candidate)
    return sys.executable


def _sanitize(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_.-]+", "-", value.strip())
    return cleaned.strip("-") or "run"


def _instance_path(category: str, instance_id: str) -> Path:
    return PROJECT_ROOT / "benchmark" / "final" / category / f"{instance_id}.json"


def _common_payload(
    args: dict[str, Any],
    *,
    require_idea: bool = False,
    require_refs: bool = False,
) -> tuple[dict[str, Any] | None, str | None]:
    category = str(args.get("category") or os.getenv("CATEGORY") or "vq")
    instance_id = str(args.get("instance_id") or os.getenv("INSTANCE_ID") or "one_layer_vq")
    if not _instance_path(category, instance_id).exists():
        return None, f"benchmark instance not found: {_instance_path(category, instance_id)}"

    idea = str(args.get("idea") or "")
    references = args.get("references") or ""
    if isinstance(references, list):
        references = "\n".join(str(item) for item in references)
    else:
        references = str(references)

    if require_idea and not idea.strip():
        return None, "idea is required for ai_researcher_run_plan"
    if require_refs and not references.strip():
        return None, "references is required for this workflow"

    payload = {
        "category": category,
        "instance_id": instance_id,
        "task_level": str(args.get("task_level") or os.getenv("TASK_LEVEL") or "task1"),
        "container_name": str(args.get("container_name") or os.getenv("CONTAINER_NAME") or "paper_eval"),
        "workplace_name": str(args.get("workplace_name") or os.getenv("WORKPLACE_NAME") or "workplace"),
        "cache_path": str(args.get("cache_path") or os.getenv("CACHE_PATH") or "cache"),
        "port": int(args.get("port") or os.getenv("PORT") or 7020),
        "max_iter_times": int(args.get("max_iter_times") or os.getenv("MAX_ITER_TIMES") or 0),
        "model": str(args.get("model") or os.getenv("COMPLETION_MODEL") or "openai/MiniMax-M2.7"),
        "idea": idea,
        "references": references,
        "env": args.get("env") or {},
    }
    return payload, None


def _start_run(workflow: str, payload: dict[str, Any], *, dry_run: bool = False) -> str:
    RUNS_ROOT.mkdir(parents=True, exist_ok=True)
    run_id = f"{time.strftime('%Y%m%d-%H%M%S')}-{workflow}-{_sanitize(payload['category'])}-{_sanitize(payload['instance_id'])}"
    run_dir = RUNS_ROOT / run_id
    run_dir.mkdir(parents=True, exist_ok=False)

    payload_path = run_dir / "payload.json"
    payload_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    command = [
        _project_python(),
        str(PLUGIN_DIR / "runner_entry.py"),
        workflow,
        str(payload_path),
    ]
    (run_dir / "command.json").write_text(json.dumps(command, ensure_ascii=False, indent=2), encoding="utf-8")

    if dry_run:
        return _json({
            "success": True,
            "dry_run": True,
            "run_id": run_id,
            "run_dir": str(run_dir),
            "command": command,
            "payload": {k: v for k, v in payload.items() if k != "env"},
        })

    stdout = open(run_dir / "stdout.log", "ab", buffering=0)
    stderr = open(run_dir / "stderr.log", "ab", buffering=0)
    process = subprocess.Popen(
        command,
        cwd=str(PROJECT_ROOT),
        stdout=stdout,
        stderr=stderr,
        stdin=subprocess.DEVNULL,
        start_new_session=True,
    )
    (run_dir / "pid.txt").write_text(str(process.pid), encoding="utf-8")
    (run_dir / "started_at.txt").write_text(time.strftime("%Y-%m-%d %H:%M:%S"), encoding="utf-8")

    return _json({
        "success": True,
        "started": True,
        "run_id": run_id,
        "pid": process.pid,
        "run_dir": str(run_dir),
        "stdout": str(run_dir / "stdout.log"),
        "stderr": str(run_dir / "stderr.log"),
        "status_tool": "ai_researcher_run_status",
    })


def _tail(path: Path, lines: int) -> list[str]:
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8", errors="replace")
    return text.splitlines()[-max(1, min(lines, 200)):]


def _pid_running(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def ai_researcher_preflight(args: dict[str, Any], **_: Any) -> str:
    timeout = int(args.get("timeout") or 300)
    command = [_project_python(), "scripts/doctor.py"]
    result = subprocess.run(
        command,
        cwd=str(PROJECT_ROOT),
        check=False,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    instances = []
    final_dir = PROJECT_ROOT / "benchmark" / "final"
    for path in sorted(final_dir.glob("*/*.json")):
        instances.append(str(path.relative_to(final_dir)).removesuffix(".json"))
    return _json({
        "success": result.returncode == 0,
        "returncode": result.returncode,
        "project_root": str(PROJECT_ROOT),
        "command": command,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "instances": instances,
    })


def ai_researcher_run_plan(args: dict[str, Any], **_: Any) -> str:
    payload, error = _common_payload(args, require_idea=True)
    if error:
        return _json({"success": False, "error": error})
    return _start_run("plan", payload, dry_run=bool(args.get("dry_run")))


def ai_researcher_run_idea(args: dict[str, Any], **_: Any) -> str:
    payload, error = _common_payload(args, require_refs=True)
    if error:
        return _json({"success": False, "error": error})
    return _start_run("idea", payload, dry_run=bool(args.get("dry_run")))


def ai_researcher_write_paper(args: dict[str, Any], **_: Any) -> str:
    payload, error = _common_payload(args)
    if error:
        return _json({"success": False, "error": error})
    return _start_run("paper", payload, dry_run=bool(args.get("dry_run")))


def ai_researcher_run_status(args: dict[str, Any], **_: Any) -> str:
    run_id = str(args.get("run_id") or "").strip()
    lines = int(args.get("lines") or 80)
    if not run_id:
        runs = sorted([p.name for p in RUNS_ROOT.glob("*") if p.is_dir()]) if RUNS_ROOT.exists() else []
        return _json({"success": True, "runs": runs[-20:]})

    run_dir = RUNS_ROOT / run_id
    if not run_dir.is_dir():
        return _json({"success": False, "error": f"unknown run_id: {run_id}"})

    pid = None
    running = False
    pid_path = run_dir / "pid.txt"
    if pid_path.exists():
        try:
            pid = int(pid_path.read_text(encoding="utf-8").strip())
            running = _pid_running(pid)
        except ValueError:
            pid = None

    return _json({
        "success": True,
        "run_id": run_id,
        "run_dir": str(run_dir),
        "pid": pid,
        "running": running,
        "stdout_tail": _tail(run_dir / "stdout.log", lines),
        "stderr_tail": _tail(run_dir / "stderr.log", lines),
        "payload": json.loads((run_dir / "payload.json").read_text(encoding="utf-8")) if (run_dir / "payload.json").exists() else None,
    })


_COMMON_PROPS = {
    "category": {"type": "string", "description": "Benchmark category, e.g. vq, gnn, recommendation, diffu_flow, reasoning."},
    "instance_id": {"type": "string", "description": "Benchmark instance id without .json, e.g. one_layer_vq."},
    "task_level": {"type": "string", "description": "Task level for Level 1 workflows, usually task1 or task2."},
    "container_name": {"type": "string", "description": "Docker container base name."},
    "workplace_name": {"type": "string", "description": "Workspace directory name inside the AI-Researcher environment."},
    "cache_path": {"type": "string", "description": "Flow/cache directory name."},
    "port": {"type": "integer", "description": "Communication port for the Docker-backed agent environment."},
    "max_iter_times": {"type": "integer", "description": "Maximum refinement iterations after the first implementation pass."},
    "model": {"type": "string", "description": "LiteLLM model string, e.g. openai/MiniMax-M2.7."},
    "dry_run": {"type": "boolean", "description": "Return the command and payload without launching the workflow."},
}


def register(ctx) -> None:
    ctx.register_tool(
        name="ai_researcher_preflight",
        toolset="ai_researcher",
        schema={
            "name": "ai_researcher_preflight",
            "description": "Run AI-Researcher's local doctor check and list available benchmark instances.",
            "parameters": {"type": "object", "properties": {"timeout": {"type": "integer", "description": "Doctor timeout in seconds."}}},
        },
        handler=ai_researcher_preflight,
    )
    ctx.register_tool(
        name="ai_researcher_run_plan",
        toolset="ai_researcher",
        schema={
            "name": "ai_researcher_run_plan",
            "description": "Start AI-Researcher Level 1: run_infer_plan.py for a detailed idea plus references. Returns a run_id.",
            "parameters": {
                "type": "object",
                "properties": {
                    **_COMMON_PROPS,
                    "idea": {"type": "string", "description": "Detailed research idea to implement and evaluate."},
                    "references": {"type": "string", "description": "Reference paper titles, URLs, notes, or paths."},
                },
                "required": ["idea"],
            },
        },
        handler=ai_researcher_run_plan,
    )
    ctx.register_tool(
        name="ai_researcher_run_idea",
        toolset="ai_researcher",
        schema={
            "name": "ai_researcher_run_idea",
            "description": "Start AI-Researcher Level 2: run_infer_idea.py for reference-based ideation. Returns a run_id.",
            "parameters": {
                "type": "object",
                "properties": {
                    **_COMMON_PROPS,
                    "references": {"type": "string", "description": "Reference paper titles, URLs, notes, or paths."},
                },
                "required": ["references"],
            },
        },
        handler=ai_researcher_run_idea,
    )
    ctx.register_tool(
        name="ai_researcher_write_paper",
        toolset="ai_researcher",
        schema={
            "name": "ai_researcher_write_paper",
            "description": "Start AI-Researcher's paper_agent writing workflow for a category and instance. Returns a run_id.",
            "parameters": {"type": "object", "properties": _COMMON_PROPS},
        },
        handler=ai_researcher_write_paper,
    )
    ctx.register_tool(
        name="ai_researcher_run_status",
        toolset="ai_researcher",
        schema={
            "name": "ai_researcher_run_status",
            "description": "Check an AI-Researcher background run and tail stdout/stderr logs.",
            "parameters": {
                "type": "object",
                "properties": {
                    "run_id": {"type": "string", "description": "Run id returned by an AI-Researcher start tool. Omit to list recent runs."},
                    "lines": {"type": "integer", "description": "Number of tail lines to return from each log."},
                },
            },
        },
        handler=ai_researcher_run_status,
    )
