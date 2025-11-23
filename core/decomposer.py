from typing import Dict, Any
import json, re
from .llm_client import call_ollama, get_model_for_role

DECOMPOSER_PROMPT = """
You are AURA's Task Decomposer.

Your job:
1. Analyze user input.
2. Break it into subtasks.
3. Assign each subtask to an agent.
4. ALWAYS output valid JSON.
5. Agents allowed:
   - "document"
   - "notification"
   - "planner"
   - "reflection"

STRICT RULES:
- Output ONLY JSON. No explanation.
- Do not add backticks.
- Do not add commentary.
- Output must start with '{' and end with '}'.

Format:
{
  "original": "...",
  "tasks": [
    {
      "agent": "...",
      "goal": "...",
      "details": {...}
    }
  ]
}

User message:
"""

def extract_json(text: str) -> dict:
    """
    Extracts the FIRST valid JSON object from raw LLM output.
    """
    try:
        # Find the first {...} block
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            json_text = match.group(0)
            return json.loads(json_text)

    except Exception as e:
        print("JSON extraction failed:", e)

    return None


def decompose_task(user_message: str) -> Dict[str, Any]:
    """
    Uses local LLM to decompose into tasks.
    Falls back to simple planner-only if fail.
    """
    model = get_model_for_role("reasoning")

    prompt = f"{DECOMPOSER_PROMPT}\n\"\"\"\n{user_message}\n\"\"\""

    raw = call_ollama(model, prompt)
    print("\n[RAW DECOMPOSER OUTPUT]:\n", raw, "\n")

    # Attempt JSON extraction
    data = extract_json(raw)
    if data:
        return data

    # Fallback
    print("JSON ERROR → Fallback to planner-only.")
    return {
        "original": user_message,
        "tasks": [
            {
                "agent": "planner",
                "goal": "create_plan",
                "details": {"text": user_message}
            }
        ]
    }