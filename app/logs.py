import json
import secrets

from pathlib import Path
from datetime import datetime

from pydantic import BaseModel
from pydantic_ai.messages import ModelMessagesTypeAdapter

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

def log_entry(agent, messages):
    tools = []
    for ts in agent.toolsets:
        tools.extend(ts.tools.keys())

    return {
        "agent_name": agent.name,
        "system_prompt": agent._instructions,
        "provider": agent.model.system,
        "model": agent.model.model_name,
        "tools": tools,
        "messages": ModelMessagesTypeAdapter.dump_python(messages)
    }

def serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError

def log_interaction_to_file(agent, messages):
    entry = log_entry(agent, messages)
    ts = entry["messages"][-1]["timestamp"]

    if isinstance(ts, str):
        ts = datetime.fromisoformat(ts.replace("Z", "+00:00"))

    filename = f"{agent.name}_{ts:%Y%m%d_%H%M%S}_{secrets.token_hex(3)}.json"
    filepath = LOG_DIR / filename

    with filepath.open("w", encoding="utf-8") as f:
        json.dump(entry, f, indent=2, default=serializer)

    return filepath

class EvaluationCheck(BaseModel):
    check_name: str
    justification: str
    check_pass: bool

class EvaluationChecklist(BaseModel):
    checklist: list[EvaluationCheck]
    summary: str

def load_log_file(log_file):
    with open(log_file) as f:
        data = json.load(f)
    data["log_file"] = log_file
    return data

def simplify_log_messages(messages):
    simplified = []

    for m in messages:
        parts = []
        for p in m["parts"]:
            p = p.copy()
            kind = p["part_kind"]

            for k in ("timestamp", "tool_call_id", "metadata", "id"):
                p.pop(k, None)

            if kind == "tool-return":
                p["content"] = "RETURN_RESULTS_REDACTED"

            parts.append(p)

        simplified.append({"kind": m["kind"], "parts": parts})

    return simplified

def evaluate_log_record(eval_agent, log_record, prompt_format):
    messages = log_record["messages"]

    question = messages[0]["parts"][0]["content"]
    answer = messages[-1]["parts"][0]["content"]

    log = json.dumps(simplify_log_messages(messages))

    prompt = prompt_format.format(
        instructions=log_record["system_prompt"],
        question=question,
        answer=answer,
        log=log
    )

    return eval_agent.run_sync(
        prompt,
        output_type=EvaluationChecklist
    ).output