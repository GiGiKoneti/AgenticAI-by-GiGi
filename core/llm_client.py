import subprocess
import os

def call_ollama(model: str, prompt: str) -> str:
    """
    Simple wrapper to call a local Ollama model.
    Returns raw text output from the model.
    """
    process = subprocess.Popen(
        ["ollama", "run", model],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = process.communicate(input=prompt.encode("utf-8"))

    if stderr:
        # You can log this later
        print("OLLAMA ERROR:", stderr.decode("utf-8"))

    return stdout.decode("utf-8")


def get_model_for_role(role: str) -> str:
    """
    Map roles like 'reasoning', 'extraction', 'summary' to models.
    Reads from environment or uses defaults.
    """
    default_map = {
        "reasoning": os.getenv("MODEL_REASONING", "llama3.1"),
        "extraction": os.getenv("MODEL_EXTRACTION", "phi3"),
        "summary": os.getenv("MODEL_SUMMARY", "mistral"),
    }
    return default_map.get(role, "llama3.1")