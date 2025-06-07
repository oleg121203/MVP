from typing import Dict, List, Optional
import os
import pandas as pd
from sentence_transformers import SentenceTransformer
import pinecone
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class VectorDBService:
    def __init__(self):
        self.api_key = os.getenv('PINECONE_API_KEY')
        self.environment = os.getenv('PINECONE_ENVIRONMENT', 'us-west1-gcp')
        self.index_name = os.getenv('PINECONE_INDEX_NAME', 'ventai-materials')
        self.dimension = 384  # Dimension for all-MiniLM-L6-v2 model
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = self._initialize_index()

    def _initialize_index(self):
        """
        Initialize Pinecone index if it doesn't exist.
        """
        pinecone.init(api_key=self.api_key, environment=self.environment)
        
        if self.index_name not in pinecone.list_indexes():
            pinecone.create_index(
                name=self.index_name,
                dimension=self.dimension,
                metric='cosine'
            )
        
        return pinecone.Index(self.index_name)

    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate vector embedding for a given text.

        Args:
            text: Input text to embed.

        Returns:
            List[float]: Vector embedding.
        """
        return self.model.encode(text).tolist()

    def upsert_vector(self, vector_id: str, vector: List[float], metadata: Dict) -> None:
        """
        Upsert a vector with metadata to Pinecone.

        Args:
            vector_id: Unique ID for the vector.
            vector: Vector embedding.
            metadata: Metadata associated with the vector.
        """
        self.index.upsert([(vector_id, vector, metadata)])

    def batch_upsert_vectors(self, vectors_data: List[Dict]) -> None:
        """
        Upsert multiple vectors to Pinecone in a batch.

        Args:
            vectors_data: List of dictionaries with id, vector, and metadata.
        """
        vectors = [(data['id'], data['vector'], data['metadata']) for data in vectors_data]
        self.index.upsert(vectors)

    def search_similar(self, query: str, top_k: int = 5, filter: Optional[Dict] = None) -> List[Dict]:
        """
        Search for similar vectors based on a query text.

        Args:
            query: Query text to search.
            top_k: Number of top results to return.
            filter: Optional metadata filter.

        Returns:
            List[Dict]: List of matching results with metadata and scores.
        """
        query_vector = self.generate_embedding(query)
        results = self.index.query(query_vector, top_k=top_k, include_metadata=True, filter=filter)
        return [{'id': match['id'], 'score': match['score'], 'metadata': match['metadata']} for match in results['matches']]

    def update_vector(self, vector_id: str, vector: Optional[List[float]] = None, metadata: Optional[Dict] = None) -> None:
        """
        Update an existing vector or its metadata.

        Args:
            vector_id: ID of the vector to update.
            vector: New vector embedding (optional).
            metadata: New metadata (optional).
        """
        update_data = {}
        if vector:
            update_data['values'] = vector
        if metadata:
            update_data['metadata'] = metadata
        if update_data:
            self.index.update(id=vector_id, **update_data)

    def delete_vector(self, vector_id: str) -> None:
        """
        Delete a vector from the index.

        Args:
            vector_id: ID of the vector to delete.
        """
        self.index.delete(ids=[vector_id])
