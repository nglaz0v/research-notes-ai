from abc import ABC, abstractmethod


class BaseProvider(ABC):
    """Abstract base class for LLM backends."""

    @abstractmethod
    async def generate(self, messages: list[dict], **kwargs) -> str:
        """Generate a response from the LLM.

        Args:
            messages: List of message dicts with 'role' and 'content'.
            **kwargs: Additional parameters (temperature, max_tokens, etc.).

        Returns:
            The generated text response.
        """
        ...
