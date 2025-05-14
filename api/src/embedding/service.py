import torch
from bs4 import BeautifulSoup
from pathlib import Path
from sentence_transformers import SentenceTransformer
import logging

logger = logging.getLogger(__name__)

class EmbeddingService:
    MODEL_IDENTIFIER = "paraphrase-multilingual-mpnet-base-v2"
    MODEL_PATH = f"{Path(__file__).parent.parent}/.model/{MODEL_IDENTIFIER}"

    INPUT_LENGHT_LIMIT = 1678

    DEVICE_TYPE_CUDA = "cuda"
    DEVICE_TYPE_CPU = "cpu"

    DEFAULT_CHUNK_SIZE = 1000

    BEAUTIFULSOUP_PARSER = "html.parser"

    def __init__(self) -> None:
        self.model = SentenceTransformer(self.MODEL_PATH)
        self.device = self.DEVICE_TYPE_CUDA if torch.cuda.is_available() else self.DEVICE_TYPE_CPU
        if torch.cuda.is_available():
            logger.info("CUDA is currently available, embedding service using GPU.")
        else:
            logger.warning("CUDA is currently not available, embedding service using CPU.")
        self.model.to(self.device)

    def embed_text(self, text, chunk_size=DEFAULT_CHUNK_SIZE):
        chunks = [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]
        # Compute embeddings for each chunk
        chunk_embeddings = [self.model.encode(chunk, convert_to_tensor=True) for chunk in chunks]
        try:
            # Average the embeddings
            avg_embedding = sum(chunk_embeddings) / len(chunk_embeddings)
            return avg_embedding.tolist()
        except:
            return [0] * 1024

    def get_vector(self, text: str|list[str]) -> dict:
        if isinstance(text, str):
            response = self.embed_text(text)
        else: 
            response = self.embed_text(text[0])
        return {"embeddings": response}

    def generate(self, label, description):
        text = f"{label} {description}"
        soup = BeautifulSoup(text, self.BEAUTIFULSOUP_PARSER)
        concept_text = soup.get_text()

        text = concept_text[:self.INPUT_LENGHT_LIMIT]

        search_response = self.get_vector(text)
        search_vector = search_response['embeddings']

        return search_vector