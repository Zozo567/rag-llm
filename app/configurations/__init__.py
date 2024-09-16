import logging
from app.configurations.builder import (
    Parameters,
    RAG
)

logging.basicConfig(level=logging.INFO)

API_PREFIX = '/api/v1'

parameters = Parameters().__call__()
rag_chain = RAG(parameters).__call__()
