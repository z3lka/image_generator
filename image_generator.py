import os
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
from pathlib import Path
from config import GENAI_LLM, GENAI_API_KEY

genai.api_key = GENAI_API_KEY

# NOTE: since I'm using Gemini-2.0-flash-exp model, the response will contain both text and image modalities
# If you want to generate only images, you can use the Gemini-2.0-flash model


class ImageGenerator:
    """Generate and save images based on enhanced prompts"""

    def __init__(self, save_path: str) -> None:
        self.save_path = Path(save_path)
        self.save_path.mkdir(parents=True, exist_ok=True)
        self.image_counter: int = len(os.listdir(self.save_path))

    def generate_image(self, prompt: str) -> None:
        try:
            client = genai.Client()  # initialize the GenAI client

            # Generate content with text and image modalities
            response = client.models.generate_content(
                model=GENAI_LLM,  # specify the model to use (you can change it from config.py)
                contents=prompt,  # provide the enhanced prompt
                config=types.GenerateContentConfig(
                    response_modalities=[
                        "Text",
                        "Image",
                    ]  # specify the modalities to generate
                ),
            )

            # Loop through the response parts and save the images
            for part in response.candidates[0].content.parts:
                if part.text is not None:
                    print(f" Generated Text: {part.text}")
                elif (
                    part.inline_data is not None
                ):  # check if the part contains image data
                    image = Image.open(BytesIO(part.inline_data.data))
                    # if you want to resize the image at specific dimensions adjust the line below
                    # image = image.resize((32, 32), Image.LANCZOS)
                    image_path = self.save_path / f"image_{self.image_counter}.png"
                    image.save(image_path)
                    print(f"Image saved to {image_path}")
                    image.show()
                    self.image_counter += 1
                else:
                    print("No valid content found for generation.")
        except Exception as e:
            print(f"Image generation error: {e}")
