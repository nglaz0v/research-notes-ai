import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Central configuration loaded from environment variables."""

    LLM_BACKEND = os.getenv("LLM_BACKEND", "openai")

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.smartbuddy.ru/v1")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    GIGACHAT_AUTH_KEY = os.getenv("GIGACHAT_AUTH_KEY", "")
    GIGACHAT_SCOPE = os.getenv("GIGACHAT_SCOPE", "GIGACHAT_API_PERS")
    GIGACHAT_MODEL = os.getenv("GIGACHAT_MODEL", "GigaChat-2")

    YANDEX_IAM_TOKEN = os.getenv("YANDEX_IAM_TOKEN", "")
    YANDEX_FOLDER_ID = os.getenv("YANDEX_FOLDER_ID", "")
    YANDEX_MODEL = os.getenv("YANDEX_MODEL", "yandexgpt-lite")

    OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3.5:4b")

    VK_BOT_TOKEN = os.getenv("VK_BOT_TOKEN", "")

    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "4096"))
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.3"))
