from pydantic import BaseModel, field_validator


# Define the UserPrompt model
class UserPrompt(BaseModel):
    prompt: str
    save_location_openai: str = "./images/openai"
    save_location_genai: str = "./images/genai"

    @field_validator("prompt")
    def prompt_length(cls, v):
        if len(v) < 10:
            raise ValueError("Prompt must be at least 10 characters long")
        return v
