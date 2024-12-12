"""Prompt service to manage prompts for different models and functions.

This service handles the organization, formatting, and delivery of prompts
for various models and functional components of the system.
"""
import os
from typing import Dict, Optional

import yaml


class PromptService:
    """Service class to manage and format prompts."""

    _instance: Optional["PromptService"] = None

    def __new__(cls, *args, **kwargs) -> "PromptService":
        """Implement singleton pattern."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, prompt_template_dir: str = "./src/config/prompts"):
        """Initialize the prompt service.

        Args:
            prompt_template_dir: Directory containing prompt template YAML files
        """
        self.prompt_template_dir = prompt_template_dir
        self.prompt_templates: Dict[str, Dict] = {}
        self.role_prompts: Dict[str, Dict] = {}
        self._load_prompt_templates()

    def _load_prompt_templates(self) -> None:
        """Load all prompt templates from YAML files in the template directory."""
        if not os.path.exists(self.prompt_template_dir):
            raise FileNotFoundError(
                f"Prompt template directory not found: {self.prompt_template_dir}"
            )

        for filename in os.listdir(self.prompt_template_dir):
            if filename.endswith(".yaml") or filename.endswith(".yml"):
                template_path = os.path.join(self.prompt_template_dir, filename)
                with open(template_path, "r", encoding="utf-8") as file:
                    template_name = os.path.splitext(filename)[0]
                    template = yaml.safe_load(file)
                    if template.get("type", "") == "role":
                        self.role_prompts[template_name] = template
                    else:
                        self.prompt_templates[template_name] = template

    def get_prompt(self, template_name: str, **kwargs) -> str:
        """Get a formatted prompt using the specified template and parameters.

        Args:
            template_name: Name of the prompt template to use
            **kwargs: Key-value pairs to format the prompt template

        Returns:
            Formatted prompt string

        Raises:
            KeyError: If template_name doesn't exist
        """
        if template_name not in self.prompt_templates:
            raise KeyError(f"Prompt template not found: {template_name}")

        template = self.prompt_templates[template_name]
        prompt_template = template.get("prompt", "")

        try:
            return prompt_template.format(**kwargs)
        except KeyError as e:
            raise KeyError(f"Missing required parameter in prompt template: {e}") from e

    def add_template(self, template_name: str, template: Dict) -> None:
        """Add a new prompt template programmatically.

        Args:
            template_name: Name for the new template
            template: Template dictionary containing prompt format
        """
        self.prompt_templates[template_name] = template

    def get_template_parameters(self, template_name: str) -> Optional[Dict]:
        """Get the required parameters for a prompt template.

        Args:
            template_name: Name of the prompt template

        Returns:
            Dictionary of parameter descriptions if available, None otherwise
        """
        if template_name not in self.prompt_templates:
            raise KeyError(f"Prompt template not found: {template_name}")

        return self.prompt_templates[template_name].get("parameters")

    def remove_template(self, template_name: str) -> None:
        """Remove a prompt template.

        Args:
            template_name: Name of the template to remove

        Raises:
            KeyError: If template_name doesn't exist
        """
        if template_name not in self.prompt_templates:
            raise KeyError(f"Prompt template not found: {template_name}")

        del self.prompt_templates[template_name]

    def build_prompt_from_template(self, template_name: str, **kwargs) -> str:
        """Build prompt using the specified template with unified context.

        Args:
            template_name: Name of the prompt template to use
            **kwargs: Additional parameters for template formatting

        Returns:
            Formatted prompt string

        Raises:
            KeyError: If template not found or required parameters missing
        """
        if template_name not in self.prompt_templates:
            raise KeyError(f"Prompt template not found: {template_name}")

        # Default context parameters from unified_context
        context_params = {}

        # Merge with additional kwargs, allowing kwargs to override defaults
        template_params = {**context_params, **kwargs}

        return self.get_prompt(template_name, **template_params)

    def get_start_prompt_by_role(self, role: str) -> str:
        """Load the start prompt for the agent's role."""
        template = self.role_prompts.get(role, {"prompt": "you are a helpful agent"})
        return template.get("prompt")
