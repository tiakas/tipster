import json
import random
import re
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


_TOPIC_RE = re.compile(r"^[\w\s\-.,!?+#/]+$")


def validate_topic(topic: str) -> str:
    topic = topic.strip()
    if not topic:
        raise ValueError("topic cannot be empty")
    if len(topic) > 100:
        raise ValueError("topic too long (max 100 characters)")
    if not _TOPIC_RE.match(topic):
        raise ValueError("topic contains invalid characters")
    return topic


_STATUS_MESSAGES = {
    400: "invalid request",
    401: "invalid API key",
    403: "access forbidden",
    404: "not found",
    429: "rate limit exceeded",
    500: "server error",
    503: "service unavailable",
}


def api_error_message(provider: str, status: int) -> str:
    detail = _STATUS_MESSAGES.get(status, f"status {status}")
    return f"{provider} API error: {detail}"


def build_prompt(topic: str) -> str:
    topic = validate_topic(topic)
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
    if not isinstance(data, dict) or not data.get("content"):
        raise ValueError("AI response missing required 'content' field")
    return TipResponse(
        content=data["content"],
        examples=data.get("examples", []),
        labels=data.get("labels", []),
    )


def generate_with_retry(client: "Client", topic: str, attempts: int = 2) -> TipResponse:
    last_err: Optional[json.JSONDecodeError] = None
    for _ in range(max(1, attempts)):
        try:
            return client.generate_tip(topic)
        except json.JSONDecodeError as e:
            last_err = e
    raise Exception(
        f"model returned invalid JSON after {attempts} attempts: {last_err}"
    )


def extract_json(s: str) -> str:
    start = s.find("{")
    end = s.rfind("}")
    if start == -1 or end == -1:
        return s
    return s[start : end + 1]
