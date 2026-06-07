from config import Config


def get_provider():
    """Factory: return the configured LLM backend provider.

    Supported backends: openai, gigachat, yandexgpt, ollama.
    """
    backend = Config.LLM_BACKEND.lower()

    if backend == "openai":
        from providers.openai_provider import OpenAIProvider

        return OpenAIProvider()

    if backend == "gigachat":
        from providers.gigachat_provider import GigaChatProvider

        return GigaChatProvider()

    if backend in ("yandexgpt", "yandex", "yandex_gpt"):
        from providers.yandex_provider import YandexGPTProvider

        return YandexGPTProvider()

    if backend == "ollama":
        from providers.ollama_provider import OllamaProvider

        return OllamaProvider()

    raise ValueError(f"Unknown LLM_BACKEND: {backend}. Supported: openai, gigachat, yandexgpt, ollama")
