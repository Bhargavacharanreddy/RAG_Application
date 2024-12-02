# load_index.py
import faiss
import pickle
import os

def load_faiss_index():
    # Update these paths to be relative to the script location
    current_dir = os.path.dirname(os.path.abspath(__file__))
    index_file = os.path.join(current_dir, 'faiss_index.index')
    metadata_file = os.path.join(current_dir, 'metadata.pkl')
    
    # Load the FAISS index
    index = faiss.read_index(index_file)

    # Load metadata
    with open(metadata_file, "rb") as f:
        metadata = pickle.load(f)
    return index, metadata
