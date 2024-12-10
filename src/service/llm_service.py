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

    def completion_with_object(
        self, prompt: str, response_format: type, model: str = "gpt-4o"
    ):
        """Generate completions from the given prompt and parse into specified object type.

        Args:
            prompt: The input prompt text
            response_format: The Pydantic model class to parse the response into
            model: The LLM model to use

        Returns:
            An instance of the specified response_format type
        """

        completions = self.client.beta.chat.completions.parse(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "Return the information based on the prompt.",
                },
                {"role": "user", "content": prompt},
            ],
            response_format=response_format,
        )
        return completions.choices[0].message.parsed

    def completions_with_context(
        self, context: List[Dict], model: str = "gpt-4o-mini"
    ) -> str:
        """Generate completions from the given context."""
        completions = self.client.chat.completions.create(model=model, messages=context)
        result = completions.choices[0].message.content
        return result
