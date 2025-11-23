class ReflectionAgent:
    def run(self, details):
        """
        Will later: call LLM to critique and improve outputs
        from other agents. For now, returns a static note.
        """
        return {
            "reflection": "ReflectionAgent placeholder: results look okay for now.",
            "details_received": list(details.keys()),
        }