import requests
from . import (
    Client,
    TipResponse,
    build_prompt,
    parse_response,
    extract_json,
    register_provider,
)


class DeepSeekClient(Client):
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model or "deepseek-chat"

    def generate_tip(self, topic: str) -> TipResponse:
        prompt = build_prompt(topic)

        url = "https://api.deepseek.com/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        body = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
        }

        response = requests.post(url, json=body, headers=headers)
        if response.status_code != 200:
            raise Exception(f"DeepSeek API error: {response.text}")

        data = response.json()
        choices = data.get("choices", [])
        if not choices:
            raise Exception("No response from DeepSeek")

        message = choices[0].get("message", {})
        content = message.get("content", "")
        json_str = extract_json(content)
        return parse_response(json_str)


register_provider("deepseek", DeepSeekClient)
