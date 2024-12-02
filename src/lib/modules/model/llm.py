from typing import List, Dict

from openai import OpenAI


class AdHocInference:
    def __init__(self, api_key: str, config: dict):
        self.client = OpenAI(api_key=api_key, **config)

    def completions(self, prompt: str, model: str = "gpt-4o-mini"):
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

    def completions_with_context(self, context: List[Dict], model: str = "gpt-4o-mini"):
        completions = self.client.chat.completions.create(model=model, messages=context)
        result = completions.choices[0].message.content
        return result
