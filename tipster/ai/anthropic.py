import requests
from . import (
    Client,
    TipResponse,
    build_prompt,
    parse_response,
    extract_json,
    register_provider,
)


class AnthropicClient(Client):
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model or "claude-3-5-sonnet-20241022"
        self.session = requests.Session()

    def generate_tip(self, topic: str) -> TipResponse:
        prompt = build_prompt(topic)

        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
        }
        body = {
            "model": self.model,
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": prompt}],
        }

        response = self.session.post(url, json=body, headers=headers, timeout=(5, 30))
        if response.status_code != 200:
            raise Exception(f"Anthropic API error: status {response.status_code}")

        data = response.json()
        content = data["content"]
        if content and len(content) > 0:
            text = content[0]["text"]
            json_str = extract_json(text)
            return parse_response(json_str)

        raise Exception("No response from Anthropic")


register_provider("anthropic", AnthropicClient)
