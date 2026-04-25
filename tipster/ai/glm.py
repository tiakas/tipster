import requests
from . import (
    Client,
    TipResponse,
    build_prompt,
    parse_response,
    extract_json,
    register_provider,
)


class GLMClient(Client):
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model or "glm-4"
        self.session = requests.Session()

    def generate_tip(self, topic: str) -> TipResponse:
        prompt = build_prompt(topic)

        url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        body = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
        }

        response = self.session.post(url, json=body, headers=headers, timeout=(5, 30))
        if response.status_code != 200:
            raise Exception(f"GLM API error: status {response.status_code}")

        data = response.json()
        choices = data.get("choices", [])
        if not choices:
            raise Exception("No response from GLM")

        message = choices[0].get("message", {})
        content = message.get("content", "")
        json_str = extract_json(content)
        return parse_response(json_str)


register_provider("glm", GLMClient)
