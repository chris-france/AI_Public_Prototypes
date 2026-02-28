"""Ollama SSE streaming client."""

import json
import requests


def is_ollama_available(base_url="http://localhost:11434"):
    try:
        return requests.get(f"{base_url}/api/tags", timeout=2).status_code == 200
    except Exception:
        return False


def get_models(base_url="http://localhost:11434"):
    try:
        r = requests.get(f"{base_url}/api/tags", timeout=5)
        if r.status_code == 200:
            return [m["name"] for m in r.json().get("models", [])]
    except Exception:
        pass
    return []


def stream_ollama(prompt, model="llama3.2", base_url="http://localhost:11434"):
    try:
        r = requests.post(
            f"{base_url}/api/generate",
            json={"model": model, "prompt": prompt, "stream": True, "options": {"temperature": 0.7, "num_predict": 1000}},
            stream=True, timeout=120,
        )
        r.raise_for_status()
        for line in r.iter_lines():
            if line:
                data = json.loads(line)
                token = data.get("response", "")
                if token:
                    yield token
                if data.get("done"):
                    break
    except Exception as e:
        yield f"\n\n[Error: {str(e)}]"
