"""
Tests for LLM Client
"""

import pytest
from unittest.mock import Mock, patch
from quantcli.llm_client import LLMClient, LLMResponse


class TestLLMClient:
    """Test suite for LLMClient class"""

    def test_init_with_api_key(self):
        """Test initialization with explicit API key"""
        with patch('quantcli.llm_client.OpenAI') as mock_openai:
            client = LLMClient(api_key="test-key")
            assert client.api_key == "test-key"
            assert client.model == "gpt-4o-2024-11-20"
            mock_openai.assert_called_once_with(api_key="test-key")

    def test_init_from_env(self, monkeypatch):
        """Test initialization with API key from environment"""
        monkeypatch.setenv("OPENAI_API_KEY", "env-test-key")
        with patch('quantcli.llm_client.OpenAI') as mock_openai:
            client = LLMClient()
            assert client.api_key == "env-test-key"

    def test_init_missing_api_key(self, monkeypatch):
        """Test initialization fails without API key"""
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        with pytest.raises(ValueError, match="OpenAI API key not found"):
            LLMClient()

    @patch('quantcli.llm_client.OpenAI')
    def test_chat_completion_success(self, mock_openai_class):
        """Test successful chat completion"""
        # Mock response
        mock_choice = Mock()
        mock_choice.message.content = "Test response"
        mock_choice.finish_reason = "stop"

        mock_response = Mock()
        mock_response.choices = [mock_choice]
        mock_response.model = "gpt-4o-2024-11-20"
        mock_response.usage.total_tokens = 100

        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai_class.return_value = mock_client

        client = LLMClient(api_key="test-key")
        messages = [{"role": "user", "content": "Test"}]
        result = client.chat_completion(messages)

        assert isinstance(result, LLMResponse)
        assert result.content == "Test response"
        assert result.tokens_used == 100
        assert result.finish_reason == "stop"

    @patch('quantcli.llm_client.OpenAI')
    def test_chat_completion_failure(self, mock_openai_class):
        """Test chat completion handles errors"""
        mock_client = Mock()
        mock_client.chat.completions.create.side_effect = Exception("API Error")
        mock_openai_class.return_value = mock_client

        client = LLMClient(api_key="test-key")
        messages = [{"role": "user", "content": "Test"}]
        result = client.chat_completion(messages)

        assert result is None

    @patch('quantcli.llm_client.OpenAI')
    def test_simple_prompt(self, mock_openai_class):
        """Test simple_prompt convenience method"""
        mock_choice = Mock()
        mock_choice.message.content = "Simple response"
        mock_choice.finish_reason = "stop"

        mock_response = Mock()
        mock_response.choices = [mock_choice]
        mock_response.model = "gpt-4o-2024-11-20"
        mock_response.usage.total_tokens = 50

        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai_class.return_value = mock_client

        client = LLMClient(api_key="test-key")
        result = client.simple_prompt(
            system_message="You are a helper",
            user_message="Help me"
        )

        assert result == "Simple response"
