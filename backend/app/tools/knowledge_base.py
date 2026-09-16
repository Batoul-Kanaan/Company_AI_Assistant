from langchain.tools import tool

from backend.app.ingestion.knowledge_base import (
    search_knowledge_base as search_knowledge_base_function,
)


@tool
def search_knowledge_base(
    query: str,
) -> list[dict]:
    """
    Search the company's internal knowledge base.

    Use this tool when you need information from the company's
    internal documents and policies.

    Args:
        query: The question or information to search for.

    Returns:
        A list of relevant document chunks with their metadata.
    """
    return search_knowledge_base_function(
        query=query,
        limit=5,
    )