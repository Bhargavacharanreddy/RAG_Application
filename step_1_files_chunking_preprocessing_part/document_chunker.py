def chunk_documents(documents, chunk_size=512):
    chunked_docs = []
    for doc in documents:
        words = doc['content'].split()
        for i in range(0, len(words), chunk_size):
            chunk = ' '.join(words[i:i + chunk_size])
            chunked_docs.append({'filename': doc['filename'], 'content': chunk})
    return chunked_docs
