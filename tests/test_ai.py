class TestAI:
    """Tests for AI module"""

    def test_tip_response_creation(self):
        from tipster.ai import TipResponse

        response = TipResponse("Test content", ["example1"], ["label1"])

        assert response.content == "Test content"
        assert response.examples == ["example1"]
        assert response.labels == ["label1"]

    def test_register_provider(self):
        from tipster import ai

        class DummyClient(ai.Client):
            def generate_tip(self, topic):
                return ai.TipResponse("dummy", [], [])

        ai.register_provider("dummy", DummyClient)

        assert ai.has_provider("dummy")
        assert "dummy" in ai.get_provider_names()

    def test_get_client_unknown_provider(self):
        from tipster import ai

        client = ai.get_client("nonexistent", "key", "model")

        assert client is None

    def test_build_prompt(self):
        from tipster import ai

        prompt = ai.build_prompt("python")

        assert "python" in prompt
        assert "JSON" in prompt
        assert "content" in prompt
        assert "examples" in prompt
        assert "labels" in prompt

    def test_parse_response(self):
        from tipster import ai

        json_str = '{"content": "Use pathlib", "examples": ["from pathlib import Path"], "labels": ["best-practice"]}'

        response = ai.parse_response(json_str)

        assert response.content == "Use pathlib"
        assert response.examples == ["from pathlib import Path"]
        assert response.labels == ["best-practice"]

    def test_parse_response_with_extra_text(self):
        from tipster import ai

        text = 'Here is a tip: {"content": "Test", "examples": [], "labels": ["test"]} for you!'

        response = ai.parse_response(text)

        assert response.content == "Test"
        assert response.labels == ["test"]

    def test_extract_json(self):
        from tipster import ai

        text = 'Some text {"key": "value"} more text'

        result = ai.extract_json(text)

        assert result == '{"key": "value"}'

    def test_extract_json_no_json(self):
        from tipster import ai

        text = "No JSON here"

        result = ai.extract_json(text)

        assert result == "No JSON here"

    def test_provider_registration(self):
        from tipster import ai

        assert ai.has_provider("openai")
        assert ai.has_provider("anthropic")
        assert ai.has_provider("gemini")
        assert ai.has_provider("deepseek")
        assert ai.has_provider("glm")
        assert ai.has_provider("ollama")

    def test_get_provider_names(self):
        from tipster import ai

        names = ai.get_provider_names()

        assert "openai" in names
        assert "anthropic" in names
        assert "gemini" in names
        assert "deepseek" in names
        assert "glm" in names
        assert "ollama" in names


class TestAIClients:
    """Tests for AI client implementations"""

    def test_openai_client_default_model(self):
        from tipster.ai.openai import OpenAIClient

        client = OpenAIClient("test-key", "")

        assert client.model == "gpt-4"

    def test_openai_client_custom_model(self):
        from tipster.ai.openai import OpenAIClient

        client = OpenAIClient("test-key", "gpt-4o")

        assert client.model == "gpt-4o"

    def test_anthropic_client_default_model(self):
        from tipster.ai.anthropic import AnthropicClient

        client = AnthropicClient("test-key", "")

        assert client.model == "claude-3-5-sonnet-20241022"

    def test_anthropic_client_custom_model(self):
        from tipster.ai.anthropic import AnthropicClient

        client = AnthropicClient("test-key", "claude-3-opus")

        assert client.model == "claude-3-opus"

    def test_gemini_client_default_model(self):
        from tipster.ai.gemini import GeminiClient

        client = GeminiClient("test-key", "")

        assert client.model == "gemini-1.5-pro"

    def test_deepseek_client_default_model(self):
        from tipster.ai.deepseek import DeepSeekClient

        client = DeepSeekClient("test-key", "")

        assert client.model == "deepseek-chat"

    def test_glm_client_default_model(self):
        from tipster.ai.glm import GLMClient

        client = GLMClient("test-key", "")

        assert client.model == "glm-4"

    def test_ollama_client_default_model(self):
        from tipster.ai.ollama import OllamaClient

        client = OllamaClient("", "")

        assert client.model == "llama2"
        assert client.base_url == "http://localhost:11434"
