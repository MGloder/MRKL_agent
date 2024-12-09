"""LLM module for ad-hoc inference."""
from typing import List, Dict

from openai import OpenAI


class AdHocInference:
    """Ad-hoc inference module for generating completions from prompts."""

    def __init__(self, api_key: str, config: dict):
        """Initialize the ad-hoc inference module with the OpenAI API key and configuration."""
        self.client = OpenAI(api_key=api_key, **config)

    def completions(self, prompt: str, model: str = "gpt-4o-mini") -> str:
        """Generate completions from the given prompt."""
        completions = self.client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )
        result = completions.choices[0].message.content
        return result

    def completions_with_context(
        self, context: List[Dict], model: str = "gpt-4o-mini"
    ) -> str:
        """Generate completions from the given context."""
        completions = self.client.chat.completions.create(model=model, messages=context)
        result = completions.choices[0].message.content
        return result
