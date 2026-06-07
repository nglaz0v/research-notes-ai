import requests
from providers.base import BaseProvider
from config import Config


class YandexGPTProvider(BaseProvider):
    """YandexGPT API provider.

    Uses IAM token for authentication and direct REST calls.
    Docs: https://yandex.cloud/ru/docs/foundation-models/quickstart/yandexgpt
    """

    API_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

    def __init__(self):
        self.iam_token = Config.YANDEX_IAM_TOKEN
        self.folder_id = Config.YANDEX_FOLDER_ID
        self.model = Config.YANDEX_MODEL

    def _make_request(self, text: str, system_prompt: str, **kwargs) -> dict:
        headers = {
            "Authorization": f"Bearer {self.iam_token}",
            "x-folder-id": self.folder_id,
            "Content-Type": "application/json",
        }
        payload = {
            "modelUri": f"gpt://{self.folder_id}/{self.model}",
            "completionOptions": {
                "stream": False,
                "temperature": kwargs.get("temperature", Config.TEMPERATURE),
                "maxTokens": kwargs.get("max_tokens", Config.MAX_TOKENS),
            },
            "messages": [
                {"role": "system", "text": system_prompt},
                {"role": "user", "text": text},
            ],
        }
        response = requests.post(self.API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()

    async def generate(self, messages: list[dict], **kwargs) -> str:
        system_prompt = ""
        user_text = ""
        for msg in messages:
            if msg["role"] == "system":
                system_prompt = msg["content"]
            else:
                user_text += msg["content"] + "\n"

        result = self._make_request(user_text, system_prompt, **kwargs)
        return result["result"]["alternatives"][0]["message"]["text"]
