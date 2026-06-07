# AGENTS.md

## Project
AI assistant for summarizing scientific articles (academic notes, key theses, self-check questions).

## Architecture
```
main.py            — CLI entry point + VK bot launcher
config.py          — Env-based config (python-dotenv)
summarizer.py      — Core orchestrator: prompt + KB + LLM call
scraper.py         — Web article fetcher (requests + bs4 + html5lib)
vkbot.py           — VK bot integration (vkbottle)
providers/         — LLM backend implementations
  base.py          — Abstract BaseProvider
  openai_provider.py
  gigachat_provider.py
  yandex_provider.py
  ollama_provider.py
  factory.py       — get_provider() router
prompts/           — System prompt templates
  system_prompt_base.py
  __init__.py      — get_prompt(type) + type variants
knowledge_base/    — CSV data files
  templates.csv    — Summary templates by discipline
  formulations.csv — Ready-made academic formulations
  questions.csv    — Self-check question bank
```

## Commands
```bash
pip install -r requirements.txt   # install deps

# CLI: from file
python main.py --file article.txt

# CLI: from URL
python main.py https://example.com/article

# CLI: from stdin
echo "text" | python main.py

# With type/discipline
python main.py --file article.txt --type experimental --discipline "Компьютерные науки"

# VK bot
python main.py --vkbot
```

## Dependencies
- `openai`, `ollama` — LLM backends
- `requests`, `beautifulsoup4`, `html5lib` — web scraping
- `python-dotenv` — env loading (copy `.env.example` to `.env` locally)
- `vkbottle` — VK bot integration

## Key facts
- Multi-backend: OpenAI / GigaChat / YandexGPT / Ollama via factory pattern
- Backend selected via `LLM_BACKEND` env var (default: `openai`)
- YandexGPT uses direct REST calls (IAM token auth)
- GigaChat uses OpenAI-compatible interface with custom base_url
- Ollama uses local `ollama.AsyncClient`
- Knowledge base is local CSV files, not Google Sheets (CSV is simpler for this project)
- System prompt is bilingual (Russian) for Russian-language output
- VK bot supports commands: `/start`, `/help`, `/type`, `/discipline`
- No test suite exists — verify by running the CLI with a sample article
- No linting/formatting configured — follow PEP 8 and project style
