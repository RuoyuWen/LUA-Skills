"""Orchestrator: Story -> Plan -> Code with Skills + Validation Feedback Loop."""
import re
from pathlib import Path

from openai import OpenAI

from agents import (
    extract_steps_from_planner_output,
    run_coding_agent,
    run_planner,
    run_story_expert,
)
from stage_loader import get_init_map_code, get_npc_located_code, get_start_game_code
from validate_lua import validate_encounter

MAX_FIX_RETRIES = 2


def run_full_pipeline(
    story_input: str,
    api_key: str,
    story_model: str = "gpt-4.1",
    planning_model: str = "gpt-4.1",
    coding_model: str = "gpt-5.1-codex-max",
    assets: dict | None = None,
) -> dict:
    """
    Execute: Story Expert -> Planner -> Coding Agent (encounters only).
    输出 stages 数组：InitMap, InitEvent, StartGame。
    """
    client = OpenAI(api_key=api_key)
    assets = assets or {"npcs": [], "enemies": [], "props": [], "items": []}
    npc_located = get_npc_located_code()

    expanded_story = run_story_expert(client, story_input, story_model)
    plan_output = run_planner(client, expanded_story, planning_model, assets=assets)
    steps = extract_steps_from_planner_output(plan_output)
    steps = [s for s in steps if str(s.get("type", "")).lower() == "encounter"]
    if not steps:
        steps = [{"id": 1, "name": "SpawnEncounter_main", "type": "encounter", "description": "Main encounter"}]
    # 单奇遇时使用 SpawnEncounter_main，符合正确格式
    if len(steps) == 1:
        steps[0]["name"] = "SpawnEncounter_main"

    previous_code = ""
    init_event_parts = []

    for i, step in enumerate(steps):
        code = _generate_step_with_validation(
            client, step, expanded_story, previous_code, coding_model,
            assets=assets, all_steps=steps, step_index=i,
            npc_located_context=npc_located,
        )
        code = _clean_code_output(code)
        init_event_parts.append(code)
        previous_code += "\n\n" + code

    init_map_code = get_init_map_code()
    init_event_code = "\n\n".join(init_event_parts) if init_event_parts else ""
    # 单奇遇时添加正确格式注释
    if len(steps) == 1 and init_event_code:
        init_event_code = (
            "-- 奇遇：Main encounter from story\n"
            "-- 直接执行：固定坐标生成\n\n"
            + init_event_code
        )
    start_game_code = get_start_game_code()

    stages = [
        {"Type": "InitMap", "Code": init_map_code},
        {"Type": "InitEvent", "Code": init_event_code},
        {"Type": "StartGame", "Code": start_game_code},
    ]
    full_script = "\n\n".join(s["Code"] for s in stages if s["Code"])

    generated_files = {}
    for i, step in enumerate(steps):
        step_name = step.get("name", f"step_{i+1}")
        base = step_name.replace("SpawnEncounter_", "").lower()
        filename = f"Encounters/enc_{base}.lua"
        generated_files[filename] = init_event_parts[i] if i < len(init_event_parts) else ""

    return {
        "expanded_story": expanded_story,
        "plan_output": plan_output,
        "steps": steps,
        "generated_files": generated_files,
        "stages": stages,
        "full_script": full_script,
    }


def _generate_step_with_validation(
    client, step, expanded_story, previous_code, coding_model, assets: dict,
    all_steps: list | None = None,
    step_index: int = 0,
    npc_located_context: str = "",
) -> str:
    """Generate code for one step, with validation feedback loop for Encounter."""
    def _call_agent(errors=None):
        return run_coding_agent(
            client, step, expanded_story, previous_code, coding_model,
            validation_errors=errors, assets=assets, all_steps=all_steps or [],
            step_index=step_index, npc_located_context=npc_located_context,
        )

    code = _call_agent(errors=None)
    code = _clean_code_output(code)

    if step.get("type") != "encounter":
        return code

    errors = validate_encounter(code, assets)
    retries = 0
    while errors and retries < MAX_FIX_RETRIES:
        code = _call_agent(errors=errors)
        code = _clean_code_output(code)
        errors = validate_encounter(code, assets)
        retries += 1

    return code


def _clean_code_output(text: str) -> str:
    """Remove markdown code blocks if present."""
    text = text.strip()
    m = re.search(r"```(?:lua)?\s*\n([\s\S]*?)```", text)
    if m:
        return m.group(1).strip()
    return text


