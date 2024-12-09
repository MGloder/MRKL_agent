"""Main entrypoint module for initializing and configuring the application."""
import os
from dataclasses import dataclass
from typing import Optional

import dotenv

from service.intent_detect_service import IntentDetectService
from service.user_engagement_service import UserEngagementService
from src.service.llm_service import AdHocInference
from src.service.prompt_service import PromptService


@dataclass
class Application:
    """Represents the application with its initialized services."""

    _llm_service: AdHocInference
    _prompt_service: PromptService
    _intent_detect_service: IntentDetectService
    _user_engagement_service: UserEngagementService

    def _intent_detection(self, engagement_id: str, raw_query: str) -> str:
        """Detect intent from the given message."""
        context = self._user_engagement_service.get_context(engagement_id)
        return self._intent_detect_service.intent_detection(context, raw_query)

    @property
    def user_engagement_service(self):
        """Get the user engagement service."""
        return self._user_engagement_service

    def interact(self, engagement_id: str, raw_query: str) -> str:
        """Interact with the agent for the given engagement."""
        return self._intent_detection(engagement_id, raw_query)


@dataclass
class ApplicationInitializer:
    """Application configuration and service initialization."""

    llm_service: AdHocInference
    prompt_service: PromptService
    intent_detect_service: IntentDetectService
    user_engagement_service: UserEngagementService

    @classmethod
    def initialize(cls, openai_api_key: Optional[str] = None) -> Application:
        """Initialize application services with configuration.

        Args:
            openai_api_key: Optional OpenAI API key. If not provided, will try to get from environment.

        Returns:
            Configured AppConfig instance
        """
        dotenv.load_dotenv(".env")
        # Use provided API key or get from environment
        api_key = openai_api_key or os.environ.get("OPENAI_API_KEY", "")

        # Initialize LLM service
        llm = AdHocInference(api_key=api_key, config={})

        # Initialize prompt service
        prompts = PromptService()

        intent_detect = IntentDetectService(llm_service=llm, prompt_service=prompts)
        user_engagement = UserEngagementService()

        return Application(
            _llm_service=llm,
            _prompt_service=prompts,
            _intent_detect_service=intent_detect,
            _user_engagement_service=user_engagement,
        )
