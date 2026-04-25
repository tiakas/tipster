import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


class Tip:
    def __init__(
        self,
        id: str,
        topic: str,
        content: str,
        examples: list[str],
        labels: list[str],
        favorited: bool,
        created_at: str,
    ):
        self.id = id
        self.topic = topic
        self.content = content
        self.examples = examples
        self.labels = labels
        self.favorited = favorited
        self.created_at = created_at

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "topic": self.topic,
            "content": self.content,
            "examples": self.examples,
            "labels": self.labels,
            "favorited": self.favorited,
            "created_at": self.created_at,
        }

    @staticmethod
    def from_dict(data: dict) -> "Tip":
        return Tip(
            id=data.get("id", ""),
            topic=data.get("topic", ""),
            content=data.get("content", ""),
            examples=data.get("examples", []),
            labels=data.get("labels", []),
            favorited=data.get("favorited", False),
            created_at=data.get("created_at", ""),
        )


class TipsData:
    def __init__(self):
        self.tips: list[Tip] = []

    def to_dict(self) -> dict:
        return {
            "tips": [tip.to_dict() for tip in self.tips],
        }

    @staticmethod
    def from_dict(data: dict) -> "TipsData":
        td = TipsData()
        td.tips = [Tip.from_dict(t) for t in data.get("tips", [])]
        return td


_cache: Optional[TipsData] = None


def get_tips_path() -> Path:
    home = os.path.expanduser("~")
    config_dir = Path(home) / ".tipster"
    return config_dir / "tips.json"


def load() -> TipsData:
    global _cache
    if _cache is not None:
        return _cache

    tips_path = get_tips_path()
    if not tips_path.exists():
        return TipsData()

    with open(tips_path, "r") as f:
        data = json.load(f)
    _cache = TipsData.from_dict(data)
    return _cache


def save(data: TipsData) -> None:
    global _cache
    config_dir = get_tips_path().parent
    config_dir.mkdir(parents=True, exist_ok=True)

    tips_path = get_tips_path()
    with open(tips_path, "w") as f:
        json.dump(data.to_dict(), f, indent=2)
    _cache = data


def add_tip(topic: str, content: str, examples: list[str], labels: list[str]) -> Tip:
    tips_data = load()
    tip = Tip(
        id=str(uuid.uuid4()),
        topic=topic,
        content=content,
        examples=examples,
        labels=labels,
        favorited=False,
        created_at=datetime.now(timezone.utc).isoformat(),
    )
    tips_data.tips.append(tip)
    save(tips_data)
    return tip


def get_tips_by_topic(topic: str) -> list[Tip]:
    tips_data = load()
    return [tip for tip in tips_data.tips if tip.topic == topic]


def remove_topic(topic: str) -> None:
    tips_data = load()
    tips_data.tips = [tip for tip in tips_data.tips if tip.topic != topic]
    save(tips_data)


def get_tip_by_id(tip_id: str) -> Optional[Tip]:
    tips_data = load()
    matches = [tip for tip in tips_data.tips if tip.id.startswith(tip_id)]
    if len(matches) == 1:
        return matches[0]
    return None


def toggle_favorite(tip_id: str) -> Optional[Tip]:
    tips_data = load()
    for tip in tips_data.tips:
        if tip.id.startswith(tip_id):
            tip.favorited = not tip.favorited
            save(tips_data)
            return tip
    return None


def get_favorites() -> list[Tip]:
    tips_data = load()
    return [tip for tip in tips_data.tips if tip.favorited]


def search_tips(query: str) -> list[Tip]:
    tips_data = load()
    query_lower = query.lower()
    results = []
    for tip in tips_data.tips:
        if query_lower in tip.content.lower():
            results.append(tip)
        elif query_lower in tip.topic.lower():
            results.append(tip)
        elif any(query_lower in label.lower() for label in tip.labels):
            results.append(tip)
    return results


def get_all_topics() -> list[str]:
    tips_data = load()
    topics = set()
    for tip in tips_data.tips:
        topics.add(tip.topic)
    return list(topics)


def export() -> TipsData:
    return load()


def import_tips(data: TipsData) -> None:
    existing = load()
    existing_ids = {tip.id for tip in existing.tips}
    for tip in data.tips:
        if tip.id not in existing_ids:
            existing.tips.append(tip)
    save(existing)
