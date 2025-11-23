import subprocess, json

def call_ollama(model, prompt):
    result = subprocess.run(
        ["ollama", "run", model],
        input=prompt.encode(),
        stdout=subprocess.PIPE
    )
    return result.stdout.decode()

print(call_ollama("llama3.1", "Say hello in JSON only."))