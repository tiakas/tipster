import json
import os
import stat
from pathlib import Path


class Config:
    def __init__(self):
        self.provider: str = ""
        self.model: str = ""
        self.api_key: str = ""
        self.topics: list[str] = []
        self.today_date: str = ""
        self.today_tip_id: str = ""

    def to_dict(self) -> dict:
        return {
            "provider": self.provider,
            "model": self.model,
            "api_key": self.api_key,
            "topics": self.topics,
            "today_date": self.today_date,
            "today_tip_id": self.today_tip_id,
        }

    @staticmethod
    def from_dict(data: dict) -> "Config":
        cfg = Config()
        cfg.provider = data.get("provider", "")
        cfg.model = data.get("model", "")
        cfg.api_key = data.get("api_key", "")
        cfg.topics = data.get("topics", [])
        cfg.today_date = data.get("today_date", "")
        cfg.today_tip_id = data.get("today_tip_id", "")
        return cfg


def get_config_dir() -> Path:
    home = os.path.expanduser("~")
    return Path(home) / ".tipster"


def get_config_path() -> Path:
    return get_config_dir() / "config.json"


def load() -> Config:
    config_path = get_config_path()
    if not config_path.exists():
        return Config()

    with open(config_path, "r") as f:
        data = json.load(f)
    return Config.from_dict(data)


def save(cfg: Config) -> None:
    config_dir = get_config_dir()
    config_dir.mkdir(parents=True, exist_ok=True)

    config_path = get_config_path()
    with open(config_path, "w") as f:
        json.dump(cfg.to_dict(), f, indent=2)
    config_path.chmod(stat.S_IRUSR | stat.S_IWUSR)


def get_api_key(provider: str) -> str:
    cfg = load()
    if cfg.api_key:
        return cfg.api_key

    env_vars = {
        "openai": "OPENAI_API_KEY",
        "anthropic": "ANTHROPIC_API_KEY",
        "gemini": "GEMINI_API_KEY",
        "deepseek": "DEEPSEEK_API_KEY",
        "glm": "GLM_API_KEY",
    }
    env_key = env_vars.get(provider)
    if env_key:
        return os.getenv(env_key, "")
    return ""


def print_config(cfg: Config) -> None:
    print(f"Provider: {cfg.provider}")
    print(f"Model: {cfg.model}")
    if cfg.api_key:
        print("API Key: set")
    else:
        print("API Key: not set (using env var)")
    print(f"Topics: {cfg.topics}")
