# This script uses the 'requests' library to make HTTP requests to the Ollama API.
import requests
import os
import chromadb

def get_embedding(text, model="nomic-embed-text", api_url="http://localhost:11434/api/embeddings"):
    """Get embedding for given text using Ollama API."""
    payload = {
        "model": model,
        "prompt": text
    }
    
    response = requests.post(api_url, json=payload)
    response.raise_for_status()
    
    return response.json()['embedding']

def read_text_file(file_path):
    """Read and return the contents of a text file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def create_vector_db(db_path="./chroma_db", collection_name="documents"):
    """Create or connect to a ChromaDB vector database.
    
    Args:
        db_path: Path where the database will be stored
        collection_name: Name of the collection to create/get
        
    Returns:
        tuple: (client, collection) - ChromaDB client and collection objects
    """
    # Create persistent client (won't overwrite if exists)
    client = chromadb.PersistentClient(path=db_path)
    
    # Get existing collection or create new one (won't overwrite)
    collection = client.get_or_create_collection(collection_name)
    
    print(f"Connected to vector database at: {db_path}")
    print(f"Collection '{collection_name}' ready (contains {collection.count()} documents)")
    
    return client, collection

def add_document_to_db(collection, text, embedding, doc_id, metadata=None):
    """Add a document to the vector database if it doesn't already exist.
    
    Args:
        collection: ChromaDB collection object
        text: Original text content
        embedding: Vector embedding of the text
        doc_id: Unique identifier for the document
        metadata: Optional dictionary of metadata
        
    Returns:
        bool: True if document was added, False if it already existed
    """
    try:
        # Check if document already exists
        existing = collection.get(ids=[doc_id])
        if existing['ids']:  # Document already exists
            print(f"Document '{doc_id}' already exists in database. Skipping.")
            return False
    except Exception:
        # Document doesn't exist, which is fine
        pass
    
    # Add the document
    if metadata is None:
        metadata = {}
    
    collection.add(
        embeddings=[embedding],
        documents=[text],
        ids=[doc_id],
        metadatas=[metadata]
    )
    
    print(f"Added document '{doc_id}' to database.")
    return True

def main():
    # The path to the text file you want to embed.
    pathToFile = os.path.join(os.getcwd(), 'sample_text.txt')
    
    # Ollama API configuration.
    ollama_api_url = "http://localhost:11434/api/embeddings"
    ollama_model = "nomic-embed-text" 

    # Read the content of the file.
    file_content = read_text_file(pathToFile)

    # Get embedding
    embedding = get_embedding(file_content, ollama_model, ollama_api_url)

    # Print the results.
    print(f"Embedding dimensions: {len(embedding)}")
    print("First 10 values of the embedding vector:")
    print(embedding[:10])
    
    # Create/connect to vector database
    client, collection = create_vector_db()
    
    # Add document to database (won't overwrite if exists)
    doc_id = "sample_text_file"  # Unique ID for this document
    metadata = {
        "filename": "sample_text.txt",
        "model": ollama_model,
        "embedding_dimensions": len(embedding)
    }
    
    success = add_document_to_db(collection, file_content, embedding, doc_id, metadata)
    
    if success:
        print(f"Document successfully stored in vector database!")
    else:
        print(f"Document was already in database.")
        
    print(f"Total documents in database: {collection.count()}")

if __name__ == "__main__":
    main()
