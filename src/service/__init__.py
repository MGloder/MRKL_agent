"""Service module for various functionalities."""
from .llm_service import AdHocInference
from .prompt_service import PromptService
from .service_center import ServiceCenterInitializer

# Create default app configuration
service_center = ServiceCenterInitializer.initialize()

__all__ = ["service_center"]
