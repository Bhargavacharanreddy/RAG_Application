# save_index.py
import faiss
import pickle

def save_faiss_index(index, embeddings, index_file="faiss_index.index", metadata_file="metadata.pkl"):
    # Save the FAISS index
    faiss.write_index(index, index_file)

    # Save metadata (e.g., filenames) associated with each embedding
    metadata = [e['filename'] for e in embeddings]
    with open(metadata_file, "wb") as f:
        pickle.dump(metadata, f)

if __name__ == "__main__":
    # Example usage
    from faiss_indexer import create_faiss_index
    import sys
    sys.path.append('..')  # Add parent directory to Python path
    from step_2_generating_embedding_part.generate_embeddings import generate_embeddings

    # Generate embeddings for your documents
    embeddings = generate_embeddings()

    # Create the FAISS index
    index = create_faiss_index(embeddings)

    # Save the index and metadata
    save_faiss_index(index, embeddings)
