import sys
from models import UserPrompt
from prompt_enhancer import PromptEnhancer
from image_generator import ImageGenerator
from pydantic import ValidationError


def main():
    # Get user input
    raw_prompt = (
        str(input("Enter a prompt: ")).strip() or "A knight resting next to the river"
    )

    # don't set it too much (e.g. 1000) since api has a limit for free tier.
    # in my experiments it couldn't generate more than 10 images consecutively
    number_of_images = int(input("Enter the number of images to generate: ") or 5)

    # Get save locations
    raw_save_location_openai = (
        input("Enter save location (press Enter for default './images'): ").strip()
        or "./images/openai"
    )
    raw_save_location_genai = (
        input("Enter save location (press Enter for default './images'): ").strip()
        or "./images/genai"
    )

    try:
        # Validate user input
        user_input = UserPrompt(
            prompt=raw_prompt,
            save_location_openai=raw_save_location_openai,
            save_location_genai=raw_save_location_genai,
        )

    except ValidationError as e:
        print(f"Input validation error: {e}")
        sys.exit(1)

    print(f"\nOriginal prompt: {user_input.prompt}")
    enhancer = PromptEnhancer()  # Initialize the prompt enhancer

    # Generate images based on prompts enhanced with OpenAI and GenAI
    generator_openai = ImageGenerator(user_input.save_location_openai)
    for _ in range(number_of_images):
        enhanced_1 = enhancer.enhance_with_openai(user_input.prompt)
        print(f"\nEnhanced Prompt (OpenAI): {enhanced_1}")
        generator_openai.generate_image(enhanced_1)

    generator_genai = ImageGenerator(user_input.save_location_genai)
    for _ in range(number_of_images):
        enhanced_2 = enhancer.enhance_with_genai(user_input.prompt)
        print(f"\nEnhanced Prompt (GenAI): {enhanced_2}")
        generator_genai.generate_image(enhanced_2)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram terminated by user")
        sys.exit(0)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)
