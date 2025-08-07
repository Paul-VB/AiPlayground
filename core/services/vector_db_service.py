# Vector Database Operations
# Core functions for training and querying the vector database

import requests
import chromadb

OLLAMA_API_URL = "http://localhost:11434/api/embeddings"
OLLAMA_EMBEDDING_MODEL = "nomic-embed-text"
CHROMA_DB_PATH = "./chroma_db"
CHROMA_DB_COLLECTION = "documents"

def _get_chroma_collection():
	client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
	collection = client.get_or_create_collection(CHROMA_DB_COLLECTION)
	return collection

_chroma_collection = _get_chroma_collection()

def _vectorize_data(data: str):
	vectorize_data_response = requests.post(OLLAMA_API_URL, json={
		"model": OLLAMA_EMBEDDING_MODEL,
		"prompt": data
	})
	if not vectorize_data_response.ok:
		raise ValueError(f"Error getting embedding: {vectorize_data_response.status_code}")

	return vectorize_data_response.json()['embedding']


def train_on_resource(document_text: str, resource_name: str, metadata=None):
	collection = _chroma_collection

	existing_resources = collection.get()['ids'] 
	if resource_name in existing_resources:
		raise ValueError(f"Resource '{resource_name}' already exists")

	vectorized_data = _vectorize_data(document_text)

	collection.add(
		documents=[document_text],
		embeddings=[vectorized_data],
		ids=[resource_name],
		metadatas=[metadata or {}]
	)

def query_against_resource(query_text: str, resource_name: str = None, n_results=5):
	vectorized_query = _vectorize_data(query_text)
	collection = _chroma_collection

	should_query_all_resources = resource_name is None or resource_name == ""
	if should_query_all_resources:
		result = collection.query(
			query_embeddings=[vectorized_query],
			n_results=n_results
		)
	else:
		result = collection.query(
			query_embeddings=[vectorized_query],
			ids=[resource_name],
			n_results=n_results
		)

	return result

def list_resources():
	# Get ChromaDB ready
	collection = _chroma_collection

	# Get all documents from the collection
	all_docs = collection.get()
	
	# Extract resource names (which are the IDs)
	resource_names = all_docs['ids']
	
	# Return as list of dictionaries with resource info
	resources = []
	for name in resource_names:
		resources.append({
			"resource_name": name,
			"document_count": 1  # Since each resource = 1 document
		})
	
	return resources