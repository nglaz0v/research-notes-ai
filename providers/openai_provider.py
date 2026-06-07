import openai
from providers.base import BaseProvider
from config import Config


class OpenAIProvider(BaseProvider):
    """OpenAI API provider."""

    def __init__(self):
        self.client = openai.AsyncOpenAI(
            api_key=Config.OPENAI_API_KEY,
            base_url=Config.OPENAI_BASE_URL
        )

    async def generate(self, messages: list[dict], **kwargs) -> str:
        response = await self.client.chat.completions.create(
            model=Config.OPENAI_MODEL,
            messages=messages,
            temperature=kwargs.get("temperature", Config.TEMPERATURE),
            max_tokens=kwargs.get("max_tokens", Config.MAX_TOKENS),
        )
        return response.choices[0].message.content
