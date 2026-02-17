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
from validate_lua import validate_encounter

MAX_FIX_RETRIES = 2
SETUP_TEMPLATE_PATH = Path(__file__).parent / "setup_template.lua"


def _load_setup_template() -> str:
    if SETUP_TEMPLATE_PATH.exists():
        return SETUP_TEMPLATE_PATH.read_text(encoding="utf-8").strip()
    return ""


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
    Setup 使用固定模板，不生成。仅生成奇遇，且仅使用素材库内的 NPC/Enemy/Prop。
    """
    client = OpenAI(api_key=api_key)
    assets = assets or {"npcs": [], "enemies": [], "props": []}

    expanded_story = run_story_expert(client, story_input, story_model)
    plan_output = run_planner(client, expanded_story, planning_model, assets=assets)
    steps = extract_steps_from_planner_output(plan_output)
    # 只保留 encounter 步骤，Setup 使用固定模板
    steps = [s for s in steps if str(s.get("type", "")).lower() == "encounter"]
    if not steps:
        steps = [{"id": 1, "name": "SpawnEncounter_main", "type": "encounter", "description": "Main encounter"}]

    generated_files = {}
    previous_code = ""
    setup_template = _load_setup_template()

    for i, step in enumerate(steps):
        code = _generate_step_with_validation(
            client, step, expanded_story, previous_code, coding_model,
            assets=assets, all_steps=steps, step_index=i
        )
        code = _clean_code_output(code)

        step_name = step.get("name", f"step_{i+1}")
        base = step_name.replace("SpawnEncounter_", "").lower()
        filename = f"Encounters/enc_{base}.lua"
        generated_files[filename] = code
        previous_code += "\n\n" + code

    generated_files["Setup_World.lua"] = setup_template
    main_code = _generate_main_lua(generated_files)
    generated_files["Main.lua"] = main_code

    full_script = _assemble_full_script(generated_files, steps, setup_template)
    if not full_script or len(full_script.strip()) < 50:
        full_script = _assemble_full_script_fallback(generated_files, setup_template)

    return {
        "expanded_story": expanded_story,
        "plan_output": plan_output,
        "steps": steps,
        "generated_files": generated_files,
        "full_script": full_script,
    }


def _generate_step_with_validation(
    client, step, expanded_story, previous_code, coding_model, assets: dict,
    all_steps: list | None = None,
    step_index: int = 0,
) -> str:
    """Generate code for one step, with validation feedback loop for Encounter."""
    code = run_coding_agent(
        client, step, expanded_story, previous_code, coding_model,
        validation_errors=None, assets=assets, all_steps=all_steps or [],
        step_index=step_index
    )
    code = _clean_code_output(code)

    if step.get("type") != "encounter":
        return code

    errors = validate_encounter(code)
    retries = 0
    while errors and retries < MAX_FIX_RETRIES:
        code = run_coding_agent(
            client, step, expanded_story, previous_code, coding_model,
            validation_errors=errors, assets=assets, all_steps=all_steps or [],
            step_index=step_index
        )
        code = _clean_code_output(code)
        errors = validate_encounter(code)
        retries += 1

    return code


def _clean_code_output(text: str) -> str:
    """Remove markdown code blocks if present."""
    text = text.strip()
    m = re.search(r"```(?:lua)?\s*\n([\s\S]*?)```", text)
    if m:
        return m.group(1).strip()
    return text


def _generate_main_lua(files: dict) -> str:
    """Generate Main.lua that requires all modules in correct order."""
    setup_lines = []
    enc_lines = []
    if "Setup_World.lua" in files:
        setup_lines.append('require("Setup_World")')
    if "Spawn_AmbientNPC.lua" in files:
        setup_lines.append('require("Spawn_AmbientNPC")')
    for k in sorted(files.keys()):
        if k.startswith("Encounters/") and k.endswith(".lua"):
            mod = k.replace("Encounters/", "").replace(".lua", "")
            enc_lines.append(f'require("Encounters.{mod}")')
    if not setup_lines:
        setup_lines.append('-- require("Setup_World")')
    if not enc_lines:
        enc_lines.append('-- require("Encounters.enc_main")')

    main = """Time.Pause()

-- 1) build world
"""
    main += "\n".join(setup_lines)
    main += """

-- 2) register encounters
"""
    main += "\n".join(enc_lines)
    main += """

World.StartGame()
Time.Resume()
UI.Toast("游戏开始")
"""
    return main


def _assemble_full_script(files: dict, steps: list, setup_template: str = "") -> str:
    """
    拼装为单个完整 LUA 脚本。Setup 使用固定模板（含路人NPC），奇遇来自生成。
    """
    try:
        parts = []
        setup_code = (setup_template or files.get("Setup_World.lua", "")).strip()
        if setup_code.startswith("Time.Pause()"):
            setup_code = setup_code.replace("Time.Pause()", "", 1).strip()
        if setup_code:
            parts.append(setup_code)
            parts.append("\n\n")

        # 奇遇：先按 steps 顺序尝试匹配
        added_enc = set()
        for step in (steps or []):
            stype = str(step.get("type", "")).lower()
            if stype != "encounter":
                continue
            step_name = step.get("name", "main")
            base = step_name.replace("SpawnEncounter_", "").replace("spawnencounter_", "").lower()
            for cand in [f"Encounters/enc_{base}.lua", f"Encounters/enc_{step_name.lower()}.lua"]:
                if cand in files and cand not in added_enc:
                    desc = (step.get("description") or base).strip()[:40].replace("\n", " ")
                    parts.append("-- 奇遇：")
                    parts.append(desc)
                    parts.append("\n-- 直接执行：固定坐标生成\n\n")
                    parts.append(files[cand].strip())
                    parts.append("\n\n")
                    added_enc.add(cand)
                    break

        # 回退：若有 Encounters 文件未被加入，按文件名顺序补充
        for k in sorted(files.keys()):
            if k.startswith("Encounters/") and k.endswith(".lua") and k not in added_enc:
                base = k.replace("Encounters/enc_", "").replace(".lua", "")
                parts.append("-- 奇遇：")
                parts.append(base.replace("_", " "))
                parts.append("\n-- 直接执行：固定坐标生成\n\n")
                parts.append(files[k].strip())
                parts.append("\n\n")

        parts.append("World.StartGame()\n")
        parts.append("Time.Resume()\n")
        parts.append('UI.Toast("游戏开始")\n')

        return "".join(parts)
    except Exception:
        return _assemble_full_script_fallback(files, setup_template)


def _assemble_full_script_fallback(files: dict, setup_template: str = "") -> str:
    """最简回退：固定 Setup + 拼接奇遇"""
    parts = []
    st = (setup_template or files.get("Setup_World.lua", "")).strip()
    if st:
        if st.startswith("Time.Pause()"):
            st = st.replace("Time.Pause()", "", 1).strip()
        parts.append(st)
        parts.append("\n\n")
    for k in sorted(files.keys()):
        if k not in ("Main.lua", "Setup_World.lua"):
            parts.append(f"-- === {k} ===\n")
            parts.append(files.get(k, "").strip())
            parts.append("\n\n")
    parts.append("World.StartGame()\nTime.Resume()\nUI.Toast(\"游戏开始\")\n")
    return "".join(parts)
