"""Service center will be accessible by the entire project"""
import os
from dataclasses import dataclass
from typing import Optional

import dotenv

from service.event_action_registry import EventActionRegistry
from service.memory_cache_service import MemoryCacheService

from src.service.llm_service import AdHocInference
from src.service.prompt_service import PromptService


@dataclass
class ServiceCenter:
    """Represents the application with its initialized services."""

    _llm_service: AdHocInference
    _prompt_service: PromptService
    _event_action_registry: EventActionRegistry
    _memory_cache_service: MemoryCacheService

    @property
    def event_action_registry(self):
        """Get the event action registry."""
        return self._event_action_registry

    @property
    def llm_service(self):
        """Get the language model service."""
        return self._llm_service

    @property
    def prompt_service(self):
        """Get the prompt service."""
        return self._prompt_service

    @property
    def memory_cache_service(self):
        """Get the memory cache service."""
        return self._memory_cache_service


@dataclass
class ServiceCenterInitializer:
    """Application configuration and service initialization."""

    llm_service: AdHocInference
    prompt_service: PromptService

    @classmethod
    def initialize(cls, openai_api_key: Optional[str] = None) -> ServiceCenter:
        """Initialize application services with configuration.

        Args:
            openai_api_key: Optional OpenAI API key. If not provided, will try to get from environment.

        Returns:
            Configured AppConfig instance
        """
        dotenv.load_dotenv(".env")
        api_key = openai_api_key or os.environ.get("OPENAI_API_KEY", "")

        llm = AdHocInference(api_key=api_key, config={})
        prompts = PromptService()
        event_action_registry = EventActionRegistry()
        memory_cache_service = MemoryCacheService()

        return ServiceCenter(
            _llm_service=llm,
            _prompt_service=prompts,
            _event_action_registry=event_action_registry,
            _memory_cache_service=memory_cache_service,
        )
