import json
from core.llm_client import call_ollama, get_model_for_role

DOC_PROMPT = """
You are AURA's Document Intelligence Agent.

Your task:
- Extract important information from the given text.
- Identify dates, deadlines, events, tasks, subjects, or anything useful.
- ALWAYS output clean and valid JSON.
- Keep responses short and actionable.

JSON format:
{{
  "entities": {{
    "dates": [],
    "deadlines": [],
    "events": [],
    "subjects": [],
    "tasks": []
  }},
  "summary": ""
}}

Text:
\"\"\"{text}\"\"\"
"""

class DocumentAgent:
    def run(self, details):
        text = details.get("text", "")

        if not text:
            return {
                "entities": {
                    "dates": [],
                    "deadlines": [],
                    "events": [],
                    "subjects": [],
                    "tasks": []
                },
                "summary": "No text provided."
            }

        model = get_model_for_role("extraction")
        prompt = DOC_PROMPT.format(text=text)

        raw = call_ollama(model, prompt)

        try:
            data = json.loads(raw)
            return data
        except Exception as e:
            print("DocumentAgent JSON ERROR:", e)
            print("RAW:", raw)

            return {
                "entities": {
                    "dates": [],
                    "deadlines": [],
                    "events": [],
                    "subjects": [],
                    "tasks": []
                },
                "summary": raw[:200]
            }