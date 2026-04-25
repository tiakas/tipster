import json
import pytest
from click.testing import CliRunner

from tipster.cmd import cli


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture(autouse=True)
def setup_temp_config(monkeypatch, tmp_path):
    config_file = tmp_path / "config.json"
    monkeypatch.setattr("tipster.config.get_config_path", lambda: config_file)
    config_file.write_text(json.dumps({}))
    yield


@pytest.fixture(autouse=True)
def setup_temp_storage(monkeypatch, tmp_path):
    from tipster import storage as storage_module

    storage_module.clear_cache()

    storage_file = tmp_path / "tips.json"
    monkeypatch.setattr("tipster.storage.get_tips_path", lambda: storage_file)
    storage_file.write_text(json.dumps({"tips": []}))
    yield


class TestCLI:
    def test_cli_help(self, runner):
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "AI-powered CLI tip generator" in result.output

    def test_cli_version(self, runner):
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "0.2.0" in result.output


class TestTipsCommands:
    def test_tips_list_empty(self, runner):
        result = runner.invoke(cli, ["tips", "list"])
        assert result.exit_code == 0

    def test_tips_list_with_tips(self, runner, monkeypatch, tmp_path):
        storage_file = tmp_path / "tips.json"
        storage_file.write_text(
            json.dumps(
                {
                    "tips": [
                        {
                            "id": "abc123",
                            "topic": "python",
                            "content": "Use pathlib",
                            "examples": [],
                            "labels": [],
                            "favorited": False,
                            "created_at": "2024-01-01",
                        }
                    ]
                }
            )
        )
        result = runner.invoke(cli, ["tips", "list"])
        assert result.exit_code == 0
        assert "python" in result.output

    def test_tips_show_not_found(self, runner):
        result = runner.invoke(cli, ["tips", "show", "nonexistent"])
        assert result.exit_code == 0
        assert "not found" in result.output

    def test_tips_delete_not_found(self, runner):
        result = runner.invoke(cli, ["tips", "delete", "nonexistent"])
        assert result.exit_code == 0
        assert "not found" in result.output


class TestFavCommands:
    def test_fav_add_not_found(self, runner):
        result = runner.invoke(cli, ["fav", "add", "nonexistent"])
        assert result.exit_code == 0
        assert "not found" in result.output

    def test_fav_list_empty(self, runner):
        result = runner.invoke(cli, ["fav", "list"])
        assert result.exit_code == 0

    def test_fav_remove_not_found(self, runner):
        result = runner.invoke(cli, ["fav", "remove", "nonexistent"])
        assert result.exit_code == 0


class TestTopicsCommands:
    def test_topics_list_empty(self, runner):
        result = runner.invoke(cli, ["topics", "list"])
        assert result.exit_code == 0

    def test_topics_delete_not_found(self, runner):
        result = runner.invoke(cli, ["topics", "delete", "--yes", "nonexistent"])
        assert result.exit_code == 0


class TestConfigCommand:
    def test_config_show_empty(self, runner):
        result = runner.invoke(cli, ["config", "--show"])
        assert result.exit_code == 0

    def test_config_set_provider(self, runner, monkeypatch):
        result = runner.invoke(cli, ["config", "--provider", "openai"])
        assert result.exit_code == 0
        assert "saved" in result.output.lower()

    def test_config_set_invalid_provider(self, runner):
        result = runner.invoke(cli, ["config", "--provider", "invalid_provider"])
        assert result.exit_code == 0
        assert "unknown provider" in result.output.lower()


class TestSearchCommand:
    def test_search_empty(self, runner):
        result = runner.invoke(cli, ["search", "python"])
        assert result.exit_code == 0 or result.exit_code == 2


class TestExportCommand:
    def test_export_json(self, runner, tmp_path, monkeypatch):
        output_file = tmp_path / "export.json"
        result = runner.invoke(
            cli, ["export", "--format", "json", "--output", str(output_file)]
        )
        assert result.exit_code == 0
        assert output_file.exists()


class TestImportCommand:
    def test_import_file_not_found(self, runner):
        result = runner.invoke(cli, ["import", "/nonexistent/file.json"])
        assert result.exit_code == 0
        assert "failed to read" in result.output.lower()

    def test_import_invalid_json(self, runner, tmp_path):
        import_file = tmp_path / "import.json"
        import_file.write_text("not valid json")

        result = runner.invoke(cli, ["import", str(import_file)])
        assert result.exit_code == 0
        assert "failed to read" in result.output.lower()


class TestVersionCommand:
    def test_version(self, runner):
        result = runner.invoke(cli, ["version"])
        assert result.exit_code == 0
        assert "0.2.0" in result.output
