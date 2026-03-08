import json
import random
from abc import ABC, abstractmethod
from typing import Optional


class TipResponse:
    def __init__(self, content: str, examples: list[str], labels: list[str]):
        self.content = content
        self.examples = examples
        self.labels = labels


class Client(ABC):
    @abstractmethod
    def generate_tip(self, topic: str) -> TipResponse:
        pass


_providers: dict[str, type[Client]] = {}


def register_provider(name: str, client_class: type[Client]) -> None:
    _providers[name] = client_class


def get_client(provider: str, api_key: str, model: str) -> Optional[Client]:
    client_class = _providers.get(provider)
    if not client_class:
        return None
    return client_class(api_key, model)


def get_provider_names() -> list[str]:
    return list(_providers.keys())


def has_provider(name: str) -> bool:
    return name in _providers


ANGLES = [
    "common mistake to avoid",
    "best practice",
    "performance optimization tip",
    "security consideration",
    "debugging technique",
    "advanced pattern or idiom",
    "productivity hack",
    "common misconception to clarify",
    "architecture or design tip",
    "code review insight",
]


def build_prompt(topic: str) -> str:
    angle = random.choice(ANGLES)
    return f"""Generate a practical tip about {topic} focusing on: {angle}.

Requirements:
- 2-4 sentences of practical advice
- 1-2 code examples if applicable
- 2-3 labels (e.g., beginner, performance, security, best-practice, debugging)

Respond in JSON format only:
{{
  "content": "tip text",
  "examples": ["example1", "example2"],
  "labels": ["label1", "label2"]
}}"""


def parse_response(text: str) -> TipResponse:
    json_str = extract_json(text)
    data = json.loads(json_str)
    return TipResponse(
        content=data.get("content", ""),
        examples=data.get("examples", []),
        labels=data.get("labels", []),
    )


def extract_json(s: str) -> str:
    start = s.find("{")
    end = s.rfind("}")
    if start == -1 or end == -1:
        return s
    return s[start : end + 1]
