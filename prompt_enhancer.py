import openai
from google import genai
from google.genai import types
from config import OPENAI_LLM, THINK_LLM


class PromptEnhancer:
    "Enhance prompts with different AI models"

    @staticmethod
    def enhance_with_openai(prompt: str) -> str:
        try:
            # Create a chat completion with the user's prompt
            messages = [
                {
                    "role": "system",
                    "content": "You are a talented prompt enhancer specializing in image generation prompts. \
                     						Enhance the user's prompt to be more vivid, detailed, and imaginative while keeping \
                    						their original intent intact.",
                },
                {"role": "user", "content": prompt},
            ]
            response = openai.chat.completions.create(
                model=OPENAI_LLM, messages=messages, temperature=0.7, max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI enhancement error: {e}")
            return prompt

    @staticmethod
    def enhance_with_genai(prompt: str) -> str:
        try:
            # Initialize the GenAI client
            client = genai.Client(http_options={"api_version": "v1alpha"})

            # Enhance prompt content with the THINK_LLM model
            response = client.models.generate_content(
                model=THINK_LLM,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=[
                        "Enhance the user's prompt for image generation into a detailed, vivid single paragraph. "
                        "Maintain the original intent while adding rich descriptive elements."
                    ]
                ),
            )
            return response.text
        except Exception as e:
            print(f"GenAI enhancement error: {e}")
            return prompt
