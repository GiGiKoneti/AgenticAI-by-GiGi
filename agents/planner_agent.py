import json
import re
from core.llm_client import call_ollama, get_model_for_role

PLANNER_PROMPT = """
You are AURA's Planning Agent.

Your job:
1. Understand the user's goal.
2. Break it into clear, actionable steps.
3. Create a short, structured, realistic plan.
4. ALWAYS output valid JSON.
5. Do NOT add explanations, introductions, or concluding sentences.

IMPORTANT:
- Output ONLY the JSON object.
- Do not include any text before or after the JSON.

Use this JSON template:
{{json}}
{{
  "goal": "string",
  "steps": ["Step 1 ...", "Step 2 ..."],
  "time_estimate": "string",
  "notes": "string"
}}

User request:
\"\"\"{user_text}\"\"\"
"""

def extract_json(text: str):
    """
    Extracts the first valid JSON object from a string.
    Useful when LLM outputs extra text.
    """
    try:
        # Find first '{' and last '}'
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1:
            json_str = text[start:end+1]
            return json.loads(json_str)
    except Exception:
        pass
    return None


class PlannerAgent:
    def run(self, details):
        user_text = details.get("text", "")
        model = get_model_for_role("reasoning")

        prompt = PLANNER_PROMPT.format(user_text=user_text)
        raw = call_ollama(model, prompt)

        # Try to extract JSON reliably
        data = extract_json(raw)

        if data is not None:
            return data

        print("Planner JSON ERROR — using fallback")
        print("RAW OUTPUT:\n", raw)

        # Fallback
        return {
            "goal": user_text,
            "steps": [
                "Break the goal into smaller tasks.",
                "Work in focused sessions.",
                "Review progress after completing tasks."
            ],
            "time_estimate": "1–3 hours (approx)",
            "notes": "Fallback plan used because JSON parsing failed."
        }