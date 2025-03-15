import os
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

# set your openai and genai api keys in a ".env" file
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]

# change the model names to the ones you want to use
OPENAI_LLM = "gpt-4o-mini"
GENAI_LLM = "gemini-2.0-flash-exp"
THINK_LLM = "gemini-2.0-flash-thinking-exp"
