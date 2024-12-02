# faiss_indexer.py
import faiss
import numpy as np

def create_faiss_index(embeddings):
    # Determine the dimensionality of your embeddings
    embedding_dim = len(embeddings[0]['embedding'])

    # Initialize a FAISS index
    index = faiss.IndexFlatL2(embedding_dim)

    # Extract embeddings and add them to the index
    embedding_vectors = np.array([e['embedding'] for e in embeddings])
    index.add(embedding_vectors)
    return index
