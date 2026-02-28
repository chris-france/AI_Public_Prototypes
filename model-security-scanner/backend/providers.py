"""Model provider query functions."""

import subprocess
import requests


def get_ollama_models() -> list[str]:
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=10)
        if result.returncode != 0:
            return []
        lines = result.stdout.strip().split("\n")[1:]
        return [line.split()[0] for line in lines if line.strip()]
    except Exception:
        return []


def query_ollama(model: str, prompt: str, timeout: int = 120) -> str:
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": model, "prompt": prompt, "stream": False, "options": {"num_predict": 1024}},
            timeout=timeout,
        )
        response.raise_for_status()
        return response.json().get("response", "").strip()
    except requests.exceptions.Timeout:
        return "[TIMEOUT]"
    except requests.exceptions.ConnectionError:
        return "[ERROR: Cannot connect to Ollama. Is it running on localhost:11434?]"
    except Exception as e:
        return f"[ERROR: {str(e)}]"


def query_claude(api_key: str, prompt: str, model: str = "claude-sonnet-4-20250514") -> str:
    if not api_key or len(api_key) < 10:
        return "[ERROR: API key is missing or invalid.]"
    try:
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={"x-api-key": api_key, "anthropic-version": "2023-06-01", "content-type": "application/json"},
            json={"model": model, "max_tokens": 1024, "messages": [{"role": "user", "content": prompt}]},
            timeout=120,
        )
        if response.status_code == 401:
            return "[ERROR: Invalid API key]"
        if response.status_code != 200:
            try:
                err_msg = response.json().get("error", {}).get("message", response.text[:200])
            except Exception:
                err_msg = response.text[:200]
            return f"[ERROR: {response.status_code} - {err_msg}]"
        return response.json().get("content", [{}])[0].get("text", "[ERROR: No response content]")
    except requests.exceptions.Timeout:
        return "[TIMEOUT]"
    except Exception as e:
        return f"[ERROR: {str(e)}]"
