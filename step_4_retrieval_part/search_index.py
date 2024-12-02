import os
import openai
import numpy as np
import sys
import warnings  # For handling urllib3 warnings
import PyPDF2  # Add this import for PDF handling
import markdown  # Add this import for Markdown handling
sys.path.append('..')
from step_2_generating_embedding_part.embedding_generator import get_embedding

# Suppress urllib3 warnings
warnings.filterwarnings("ignore", message="urllib3.*", category=UserWarning)

def search(query, index, metadata, k=5):
    query_embedding = np.array(get_embedding(query), dtype=np.float32).reshape(1, -1)
    distances, indices = index.search(query_embedding, k)

    unique_results = {}
    for j, i in enumerate(indices[0]):
        filename = metadata[i]
        distance = distances[0][j]
        if filename not in unique_results or distance < unique_results[filename]:
            unique_results[filename] = distance

    results = [(filename, distance) for filename, distance in unique_results.items()]
    results.sort(key=lambda x: x[1])

    # Relevance check: Filter results based on the query
    relevant_results = []
    for filename, distance in results:
        content = read_file_content(os.path.abspath(os.path.join('..', 'step_0_documents', filename)))
        if query.lower() in content.lower():  # Check if query is in content
            relevant_results.append((filename, distance))

    return relevant_results[:k]

def summarize_content(content, max_length=300):
    return content[:max_length] + ("..." if len(content) > max_length else "")

def read_file_content(document_path):
    """Read content from text, PDF, or Markdown files."""
    if document_path.endswith('.pdf'):
        with open(document_path, 'rb') as file:  # Open PDF in binary mode
            reader = PyPDF2.PdfReader(file)
            content = ""
            for page in reader.pages:
                content += page.extract_text() or ""  # Extract text from each page
    elif document_path.endswith('.md'):
        with open(document_path, 'r', encoding='utf-8') as file:  # Open Markdown file
            content = file.read()
    else:  # Default to text file handling
        with open(document_path, 'r', encoding='utf-8') as file:  # Specify encoding
            content = file.read()
    return content

def handle_user_query(user_query):
    from step_3_creating_and_loading_index_part.load_index import load_faiss_index
    index, metadata = load_faiss_index()

    # Retrieve top-k relevant documents
    results = search(user_query, index, metadata)

    file_contents = []
    for filename, _ in results:
        document_path = os.path.abspath(os.path.join('..', 'step_0_documents', filename))  # Updated path
        print(document_path)
        if os.path.exists(document_path):
            try:
                content = read_file_content(document_path)  # Use the new function to read content
            except UnicodeDecodeError:  # Handle decoding error
                with open(document_path, 'r', encoding='latin-1') as file:  # Fallback to a different encoding
                    content = file.read()
            file_contents.append(f"File: {filename}\nContent:\n{content}\n")  # Include full content
        else:
            file_contents.append(f"File: {filename} not found.\n")

    document_summaries = '\n'.join(file_contents)
    prompt = (
        f"The following are contents of relevant documents based on your query:\n"
        f"{document_summaries}\n\n"
        f"Query: {user_query}\n"
        f"Please provide a detailed response based on this context."
    )

    if len(prompt) > 10000:
        prompt = prompt[:10000] + "... [Truncated due to token limit]"

    # Indicate loading state with animated ticker
    import threading
    import time
    import sys

    def animate_loading():
        ticker = "|/-\\"
        idx = 0
        while not stop_event.is_set():
            sys.stdout.write(f"\rGenerating response, please wait... {ticker[idx % len(ticker)]}")
            sys.stdout.flush()
            time.sleep(0.1)
            idx += 1

    stop_event = threading.Event()
    loading_thread = threading.Thread(target=animate_loading)
    loading_thread.start()

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        print("\nGPT-4 Response:\n", response['choices'][0]['message']['content'])
    except Exception as e:
        print("Error communicating with GPT-4:", e)

    stop_event.set()
    loading_thread.join()

if __name__ == "__main__":
    user_query = input("Please enter your query: ")
    handle_user_query(user_query)