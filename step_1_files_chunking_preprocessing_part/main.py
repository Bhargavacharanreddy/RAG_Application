from document_loader import load_documents
from text_preprocessor import preprocess_text
from document_chunker import chunk_documents
import json

def main():
    # Load documents
    docs = load_documents('../step_0_documents/')

    # Preprocess documents
    for doc in docs:
        doc['content'] = preprocess_text(doc['content'])

    # Chunk documents
    chunked_docs = chunk_documents(docs)

    # Save the chunked documents to a JSON file
    with open("chunked_docs.json", "w") as f:
        json.dump(chunked_docs, f)

    # Output the processed chunks
    for chunk in chunked_docs:
        print(f"Filename: {chunk['filename']}")
        print(f"Content: {chunk['content'][:100]}...")  # Print first 100 characters of the chunk
        print('-' * 40)

if __name__ == "__main__":
    main()



