# embedding_generator.py
from step_2_generating_embedding_part.openai_client import client
import openai

def get_embedding(text, model="text-embedding-ada-002"):
    try:
        # New OpenAI API (v1.0.0+)
        response = client.embeddings.create(input=[text], model=model)
        embedding = response.data[0].embedding
    except AttributeError:
        # Old OpenAI API (<v1.0.0)
        response = openai.Embedding.create(input=[text], model=model)
        embedding = response['data'][0]['embedding']
    return embedding
