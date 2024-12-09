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

    llm_service: AdHocInference
    prompt_service: PromptService
    intent_detect_service: IntentDetectService
    user_engagement_service: UserEngagementService


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
            llm_service=llm,
            prompt_service=prompts,
            intent_detect_service=intent_detect,
            user_engagement_service=user_engagement,
        )
