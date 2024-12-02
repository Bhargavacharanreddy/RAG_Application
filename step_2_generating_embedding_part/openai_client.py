# openai_client.py
import openai
import os

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Create and export the client
try:
    # For newer versions of openai package
    client = openai.OpenAI()
except AttributeError:
    # For older versions of openai package
    client = openai


