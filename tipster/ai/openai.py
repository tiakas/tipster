from . import Client, TipResponse, build_prompt, parse_response, register_provider


class OpenAIClient(Client):
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model or "gpt-4"

    def generate_tip(self, topic: str) -> TipResponse:
        from openai import OpenAI

        client = OpenAI(api_key=self.api_key)
        prompt = build_prompt(topic)

        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
        )

        content = response.choices[0].message.content
        return parse_response(content)


register_provider("openai", OpenAIClient)
