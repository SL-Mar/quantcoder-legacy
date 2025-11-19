"""
LLM Client Abstraction Layer
=============================

Provides a unified interface for OpenAI API calls, supporting both legacy (0.28)
and modern (1.x+) SDK versions. This abstraction layer allows seamless migration
and future flexibility to swap LLM providers.

Author: SL-MAR
License: MIT
"""

import os
import logging
from typing import Optional, List, Dict
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class LLMResponse:
    """Standardized response structure from LLM calls."""
    content: str
    model: str
    tokens_used: int
    finish_reason: str


class LLMClient:
    """
    Unified LLM client supporting OpenAI API (v1.x+).

    Handles API authentication, request formatting, error handling,
    and response parsing.
    """

    def __init__(self, model: str = "gpt-4o-2024-11-20", api_key: Optional[str] = None):
        """
        Initialize LLM client.

        Args:
            model: Model identifier (default: gpt-4o-2024-11-20)
            api_key: OpenAI API key (reads from OPENAI_API_KEY env if not provided)
        """
        self.model = model
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')

        if not self.api_key:
            raise ValueError(
                "OpenAI API key not found. Set OPENAI_API_KEY environment variable "
                "or pass api_key parameter."
            )

        # Initialize OpenAI client (v1.x+ SDK)
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=self.api_key)
            logger.info(f"Initialized OpenAI client with model: {self.model}")
        except ImportError:
            raise ImportError(
                "OpenAI SDK v1.x+ not found. Install with: pip install openai>=1.0.0"
            )

    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        max_tokens: int = 1500,
        temperature: float = 0.3,
        **kwargs
    ) -> Optional[LLMResponse]:
        """
        Perform a chat completion request.

        Args:
            messages: List of message dicts with 'role' and 'content'
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature (0.0-2.0)
            **kwargs: Additional parameters passed to OpenAI API

        Returns:
            LLMResponse object or None if request fails
        """
        try:
            logger.debug(f"Sending chat completion request: {len(messages)} messages")

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                **kwargs
            )

            choice = response.choices[0]

            result = LLMResponse(
                content=choice.message.content.strip(),
                model=response.model,
                tokens_used=response.usage.total_tokens,
                finish_reason=choice.finish_reason
            )

            logger.info(
                f"Chat completion successful. Tokens used: {result.tokens_used}, "
                f"Finish reason: {result.finish_reason}"
            )

            return result

        except Exception as e:
            logger.error(f"Chat completion failed: {e}", exc_info=True)
            return None

    def simple_prompt(
        self,
        system_message: str,
        user_message: str,
        **kwargs
    ) -> Optional[str]:
        """
        Simplified interface for single-turn prompts.

        Args:
            system_message: System role instruction
            user_message: User's prompt
            **kwargs: Additional parameters for chat_completion

        Returns:
            Response content string or None if request fails
        """
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]

        response = self.chat_completion(messages, **kwargs)
        return response.content if response else None
