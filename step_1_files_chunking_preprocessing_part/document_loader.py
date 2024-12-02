import os
from file_readers import read_text_file, read_pdf_file, read_markdown_file

def load_documents(directory):
    documents = []
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if filename.endswith('.txt'):
            text = read_text_file(file_path)
        elif filename.endswith('.pdf'):
            text = read_pdf_file(file_path)
        elif filename.endswith('.md'):
            text = read_markdown_file(file_path)
        else:
            print(f"Unsupported file format: {filename}")
            continue
        documents.append({'filename': filename, 'content': text})
    return documents
