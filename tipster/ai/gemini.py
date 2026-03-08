import requests
from . import (
    Client,
    TipResponse,
    build_prompt,
    parse_response,
    extract_json,
    register_provider,
)


class GeminiClient(Client):
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model or "gemini-1.5-pro"

    def generate_tip(self, topic: str) -> TipResponse:
        prompt = build_prompt(topic)

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"

        body = {
            "contents": [{"parts": [{"text": prompt}]}],
        }

        response = requests.post(url, json=body)
        if response.status_code != 200:
            raise Exception(f"Gemini API error: {response.text}")

        data = response.json()
        candidates = data.get("candidates", [])
        if not candidates:
            raise Exception("No response from Gemini")

        content = candidates[0].get("content", {})
        parts = content.get("parts", [])
        if not parts:
            raise Exception("No content in response")

        text = parts[0]["text"]
        json_str = extract_json(text)
        return parse_response(json_str)


register_provider("gemini", GeminiClient)
