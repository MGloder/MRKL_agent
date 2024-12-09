"""Service center will be accessible by the entire project"""
import os
from dataclasses import dataclass
from typing import Optional

import dotenv

from service.event_action_registry import EventActionRegistry
from service.intent_detect_service import IntentDetectService
from src.service.llm_service import AdHocInference
from src.service.prompt_service import PromptService


@dataclass
class ServiceCenter:
    """Represents the application with its initialized services."""

    _llm_service: AdHocInference
    _prompt_service: PromptService
    _intent_detect_service: IntentDetectService
    _event_action_registry: EventActionRegistry

    @property
    def intent_detection_service(self):
        """Detect intent from the given message."""
        return self._intent_detect_service


@dataclass
class ServiceCenterInitializer:
    """Application configuration and service initialization."""

    llm_service: AdHocInference
    prompt_service: PromptService
    intent_detect_service: IntentDetectService

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

        intent_detect = IntentDetectService(llm_service=llm, prompt_service=prompts)
        event_action_registry = EventActionRegistry()

        return ServiceCenter(
            _llm_service=llm,
            _prompt_service=prompts,
            _intent_detect_service=intent_detect,
            _event_action_registry=event_action_registry,
        )
