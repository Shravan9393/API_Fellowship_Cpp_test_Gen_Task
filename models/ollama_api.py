import requests
import yaml

OLLAMA_URL = "http://localhost:11434/api/generate"

def generate_from_yaml(model: str, yaml_path: str, cpp_code_path: str):
    # Read YAML
    with open(yaml_path, "r") as yml:
        prompt_data = yaml.safe_load(yml)

    # Read source code
    with open(cpp_code_path, "r") as code_file:
        cpp_code = code_file.read()

    # Merge into prompt
    full_prompt = prompt_data["instruction"] + "\n\n" + cpp_code

    # API call to Ollama
    response = requests.post(OLLAMA_URL, json={
        "model": model,
        "prompt": full_prompt,
        "stream": False
    })

    # Return response
    if response.status_code == 200:
        return response.json()["response"]
    else:
        raise Exception(f"LLM error: {response.text}")
