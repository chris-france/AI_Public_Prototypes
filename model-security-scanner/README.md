# Model Security Scanner

**LLM vulnerability testing across 10 attack categories.**

A Streamlit application that scans large language models for security weaknesses. Tests local Ollama models and Claude API against prompt injection, jailbreaking, data extraction, and seven other attack vectors. Tracks scan history with pass/fail rates and generates security scorecards.

---

## Key Features

- **10 attack categories** — Prompt injection, jailbreaking, data extraction, bias exploitation, hallucination triggers, system prompt leakage, and more
- **Multi-model support** — Test any Ollama model or Claude via Anthropic API
- **Security scorecards** — Visual pass/fail dashboards with severity ratings
- **Scan history** — SQLite-backed history with trend analysis
- **Detailed results** — See exact prompts, responses, and vulnerability classifications
- **Configurable thresholds** — Adjust detection sensitivity per category

## Tech Stack

Streamlit, Plotly, Pandas, Ollama, Anthropic API

## Quick Start

```bash
cd model-security-scanner
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Opens at [http://localhost:8604](http://localhost:8604).

Requires [Ollama](https://ollama.ai) for local model testing. Claude API testing requires an Anthropic API key (entered at runtime in the sidebar — never stored).

## License

[MIT](LICENSE)
