import pytest
import json


class TestConfig:
    """Tests for config module"""

    @pytest.fixture(autouse=True)
    def setup_temp_config(self, monkeypatch, tmp_path):
        """Setup temporary config for each test"""
        config_file = tmp_path / "config.json"
        monkeypatch.setattr("tipster.config.get_config_path", lambda: config_file)

        config_file.write_text(json.dumps({}))
        yield
        if config_file.exists():
            config_file.unlink()

    def test_load_empty_config(self):
        from tipster import config

        cfg = config.load()

        assert cfg.provider == ""
        assert cfg.model == ""
        assert cfg.api_key == ""
        assert cfg.topics == []

    def test_save_config(self):
        from tipster import config

        cfg = config.Config()
        cfg.provider = "openai"
        cfg.model = "gpt-4"
        cfg.topics = ["python", "ruby"]

        config.save(cfg)

        cfg_loaded = config.load()
        assert cfg_loaded.provider == "openai"
        assert cfg_loaded.model == "gpt-4"
        assert cfg_loaded.topics == ["python", "ruby"]

    def test_get_api_key_from_config(self, monkeypatch, tmp_path):
        config_file = tmp_path / "config.json"
        config_file.write_text(json.dumps({"api_key": "test-key-123"}))
        monkeypatch.setattr("tipster.config.get_config_path", lambda: config_file)

        from tipster import config

        key = config.get_api_key("openai")

        assert key == "test-key-123"

    def test_get_api_key_from_env(self, monkeypatch, tmp_path):
        config_file = tmp_path / "config.json"
        config_file.write_text(json.dumps({}))
        monkeypatch.setattr("tipster.config.get_config_path", lambda: config_file)
        monkeypatch.setenv("OPENAI_API_KEY", "env-key-456")

        from tipster import config

        key = config.get_api_key("openai")

        assert key == "env-key-456"

    def test_print_config(self, capsys):
        from tipster import config

        cfg = config.Config()
        cfg.provider = "anthropic"
        cfg.model = "claude-3"
        cfg.topics = ["python"]

        config.print_config(cfg)

        captured = capsys.readouterr()
        assert "anthropic" in captured.out
        assert "claude-3" in captured.out
        assert "python" in captured.out

    def test_topics_list(self):
        from tipster import config

        cfg = config.Config()
        cfg.topics = ["python", "ruby", "go"]

        config.save(cfg)

        cfg_loaded = config.load()
        assert cfg_loaded.topics == ["python", "ruby", "go"]

    def test_today_date_stored(self):
        from tipster import config

        cfg = config.Config()
        cfg.today_date = "2024-01-01"
        cfg.today_tip_id = "abc123"

        config.save(cfg)

        cfg_loaded = config.load()
        assert cfg_loaded.today_date == "2024-01-01"
        assert cfg_loaded.today_tip_id == "abc123"
