from providers.base import BaseProvider
from config import Config

import uuid
import requests
import httpx
import urllib3


# Отключение предупреждений SSL (только для разработки)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class GigaChatProvider(BaseProvider):
    """GigaChat API provider.

    GigaChat uses an OpenAI-compatible interface.
    Authentication is via OAuth token (client_id + client_secret).
    In production you must first exchange credentials for an access token.
    """

    def __init__(self):
        import openai

        access_token = self._get_access_token()
        self.client = openai.AsyncOpenAI(
            api_key=access_token,
            base_url="https://gigachat.devices.sberbank.ru/api/v1",
            http_client=httpx.AsyncClient(verify=False),  # Только для разработки
        )

    def _get_access_token(self) -> str:
        """Получает токен доступа для GigaChat API."""
        url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "RqUID": str(uuid.uuid4()),
            "Authorization": f"Basic {Config.GIGACHAT_AUTH_KEY}",
        }
        data = {"scope": Config.GIGACHAT_SCOPE}

        response = requests.post(
            url, headers=headers, data=data, timeout=30, verify=False
        )
        response.raise_for_status()
        return response.json()["access_token"]


    async def generate(self, messages: list[dict], **kwargs) -> str:
        response = await self.client.chat.completions.create(
            model=Config.GIGACHAT_MODEL,
            messages=messages,
            temperature=kwargs.get("temperature", Config.TEMPERATURE),
            max_tokens=kwargs.get("max_tokens", Config.MAX_TOKENS),
        )
        return response.choices[0].message.content
