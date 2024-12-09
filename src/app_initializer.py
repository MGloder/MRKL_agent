"""Main entrypoint module for initializing and configuring the application."""
import os
from dataclasses import dataclass
from typing import Optional

import dotenv

from lib.modules.nlu.intent_detector import IntentDetectService
from src.service.llm import AdHocInference
from src.service.prompt_service import PromptService


@dataclass
class AppConfig:
    """Application configuration and service initialization."""

    llm_service: AdHocInference
    prompt_service: PromptService
    intent_detect_service: IntentDetectService

    @classmethod
    def initialize(cls, openai_api_key: Optional[str] = None) -> "AppConfig":
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

        return cls(
            llm_service=llm, prompt_service=prompts, intent_detect_service=intent_detect
        )


# Create default app configuration
app_config = AppConfig.initialize()
