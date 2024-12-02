import numpy as np
import json
from step_2_generating_embedding_part.embedding_generator import get_embedding

def generate_embeddings():
    # Load chunked_docs from the JSON file
    with open("../step_1_files_chunking_preprocessing_part/chunked_docs.json", "r") as f:
        chunked_docs = json.load(f)

    # Generate embeddings
    embeddings = []
    for doc in chunked_docs:
        embedding = get_embedding(doc['content'])
        embeddings.append({
            "filename": doc['filename'],
            "embedding": np.array(embedding, dtype=np.float32)
        })
    return embeddings

# Example usage: generate embeddings and print
if __name__ == "__main__":
    embeddings = generate_embeddings()
    print("Embeddings generated:", embeddings)
