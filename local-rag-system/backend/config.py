"""
Configuration loader for Local RAG System.
Reads from config.yaml for easy model swapping.
"""

import os
import yaml
from dataclasses import dataclass
from pathlib import Path


CONFIG_PATH = Path(__file__).parent.parent / "config.yaml"


@dataclass
class ModelConfig:
    name: str = "llama3.2:3b"
    temperature: float = 0.7
    top_k: int = 5
    max_tokens: int = 2048


@dataclass
class EmbeddingConfig:
    model: str = "nomic-embed-text"


@dataclass
class QdrantConfig:
    url: str = "http://localhost:6333"
    documents_collection: str = "documents"
    chat_memory_collection: str = "chat_memory"


@dataclass
class ChunkingConfig:
    size: int = 512
    overlap: int = 50


@dataclass
class RetrievalConfig:
    top_k_documents: int = 5
    top_k_memory: int = 3
    score_threshold: float = 0.5


@dataclass
class OllamaConfig:
    base_url: str = "http://localhost:11434"


@dataclass
class ServerConfig:
    host: str = "0.0.0.0"
    port: int = 8605


@dataclass
class Settings:
    model: ModelConfig
    embedding: EmbeddingConfig
    qdrant: QdrantConfig
    chunking: ChunkingConfig
    retrieval: RetrievalConfig
    ollama: OllamaConfig
    server: ServerConfig

    @classmethod
    def load(cls) -> "Settings":
        """Load settings from YAML config file."""
        if CONFIG_PATH.exists():
            with open(CONFIG_PATH) as f:
                data = yaml.safe_load(f)
        else:
            data = {}

        model_data = data.get("model", {})
        embedding_data = data.get("embedding", {})
        qdrant_data = data.get("qdrant", {})
        chunking_data = data.get("chunking", {})
        retrieval_data = data.get("retrieval", {})
        ollama_data = data.get("ollama", {})
        server_data = data.get("server", {})

        # Handle nested qdrant collections
        qdrant_collections = qdrant_data.get("collections", {})

        return cls(
            model=ModelConfig(
                name=model_data.get("name", "llama3.2:3b"),
                temperature=model_data.get("temperature", 0.7),
                top_k=model_data.get("top_k", 5),
                max_tokens=model_data.get("max_tokens", 2048),
            ),
            embedding=EmbeddingConfig(
                model=embedding_data.get("model", "nomic-embed-text"),
            ),
            qdrant=QdrantConfig(
                url=qdrant_data.get("url", "http://localhost:6333"),
                documents_collection=qdrant_collections.get("documents", "documents"),
                chat_memory_collection=qdrant_collections.get("chat_memory", "chat_memory"),
            ),
            chunking=ChunkingConfig(
                size=chunking_data.get("size", 512),
                overlap=chunking_data.get("overlap", 50),
            ),
            retrieval=RetrievalConfig(
                top_k_documents=retrieval_data.get("top_k_documents", 5),
                top_k_memory=retrieval_data.get("top_k_memory", 3),
                score_threshold=retrieval_data.get("score_threshold", 0.5),
            ),
            ollama=OllamaConfig(
                base_url=ollama_data.get("base_url", "http://localhost:11434"),
            ),
            server=ServerConfig(
                host=server_data.get("host", "0.0.0.0"),
                port=server_data.get("port", 8605),
            ),
        )


# Global settings instance
settings = Settings.load()


def reload_settings():
    """Reload settings from config file."""
    global settings
    settings = Settings.load()
    return settings
