import pytest
import json


class TestStorage:
    """Tests for storage module"""

    @pytest.fixture(autouse=True)
    def setup_temp_storage(self, monkeypatch, tmp_path):
        """Setup temporary storage for each test"""
        from tipster import storage as storage_module

        storage_module.clear_cache()

        storage_file = tmp_path / "tips.json"
        monkeypatch.setattr("tipster.storage.get_tips_path", lambda: storage_file)

        storage_file.write_text(json.dumps({"tips": []}))
        yield
        if storage_file.exists():
            storage_file.unlink()

    def test_add_tip(self):
        from tipster import storage

        tip = storage.add_tip("python", "Use pathlib", ["example"], ["best-practice"])

        assert tip.topic == "python"
        assert tip.content == "Use pathlib"
        assert tip.examples == ["example"]
        assert tip.labels == ["best-practice"]
        assert tip.favorited is False
        assert tip.id is not None

    def test_get_tips_by_topic(self):
        from tipster import storage

        storage.add_tip("python", "Tip 1", [], [])
        storage.add_tip("python", "Tip 2", [], [])
        storage.add_tip("ruby", "Ruby tip", [], [])

        tips = storage.get_tips_by_topic("python")

        assert len(tips) == 2
        assert all(t.topic == "python" for t in tips)

    def test_get_all_topics(self):
        from tipster import storage

        storage.add_tip("python", "Tip 1", [], [])
        storage.add_tip("ruby", "Tip 2", [], [])
        storage.add_tip("python", "Tip 3", [], [])

        topics = storage.get_all_topics()

        assert set(topics) == {"python", "ruby"}

    def test_toggle_favorite(self):
        from tipster import storage

        tip = storage.add_tip("python", "Test tip", [], [])

        result = storage.toggle_favorite(tip.id)
        assert result.favorited is True

        result = storage.toggle_favorite(tip.id)
        assert result.favorited is False

    def test_get_favorites(self):
        from tipster import storage

        tip1 = storage.add_tip("python", "Tip 1", [], [])
        storage.add_tip("ruby", "Tip 2", [], [])

        storage.toggle_favorite(tip1.id)

        favorites = storage.get_favorites()

        assert len(favorites) == 1
        assert favorites[0].id == tip1.id

    def test_search_tips(self):
        from tipster import storage

        storage.add_tip("python", "Use pathlib for paths", [], ["best-practice"])
        storage.add_tip("python", "Use list comprehension", [], ["intermediate"])
        storage.add_tip("ruby", "Ruby tip", [], [])

        results = storage.search_tips("pathlib")

        assert len(results) == 1
        assert "pathlib" in results[0].content

    def test_remove_topic(self):
        from tipster import storage

        storage.add_tip("python", "Tip 1", [], [])
        storage.add_tip("python", "Tip 2", [], [])
        storage.add_tip("ruby", "Ruby tip", [], [])

        storage.remove_topic("python")

        tips = storage.get_tips_by_topic("python")
        assert len(tips) == 0

        ruby_tips = storage.get_tips_by_topic("ruby")
        assert len(ruby_tips) == 1

    def test_export_import(self):
        from tipster import storage

        storage.add_tip("python", "Export test", ["example"], ["test"])

        data = storage.export()

        storage.import_tips(data)

        tips = storage.get_tips_by_topic("python")
        assert len(tips) == 1

    def test_get_tip_by_id(self):
        from tipster import storage

        tip = storage.add_tip("python", "Test tip", [], [])

        found = storage.get_tip_by_id(tip.id[:8])

        assert found is not None
        assert found.id == tip.id

    def test_get_tip_by_id_not_found(self):
        from tipster import storage

        storage.add_tip("python", "Test tip", [], [])

        found = storage.get_tip_by_id("nonexistent")

        assert found is None
