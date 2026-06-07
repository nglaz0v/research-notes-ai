import ollama
from providers.base import BaseProvider
from config import Config


class OllamaProvider(BaseProvider):
    """Local Ollama provider for offline/self-hosted inference."""

    def __init__(self):
        self.client = ollama.AsyncClient(host=Config.OLLAMA_HOST)

    async def generate(self, messages: list[dict], **kwargs) -> str:
        response = await self.client.chat(
            model=Config.OLLAMA_MODEL,
            messages=messages,
            options={
                "temperature": kwargs.get("temperature", Config.TEMPERATURE),
                "num_predict": kwargs.get("max_tokens", Config.MAX_TOKENS),
            },
        )
        return response["message"]["content"]
