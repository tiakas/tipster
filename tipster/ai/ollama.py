import requests
from . import (
    Client,
    TipResponse,
    build_prompt,
    parse_response,
    extract_json,
    register_provider,
)


class OllamaClient(Client):
    def __init__(self, api_key: str, model: str):
        self.model = model or "llama2"
        self.base_url = "http://localhost:11434"
        self.session = requests.Session()

    def generate_tip(self, topic: str) -> TipResponse:
        prompt = build_prompt(topic)

        url = f"{self.base_url}/api/generate"
        body = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }

        response = self.session.post(url, json=body, timeout=(5, 30))
        if response.status_code != 200:
            raise Exception(f"Ollama API error: status {response.status_code}")

        data = response.json()
        text = data.get("response", "")
        json_str = extract_json(text)
        return parse_response(json_str)


register_provider("ollama", OllamaClient)
