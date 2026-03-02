"""LangSmith tracing setup"""

import os
import logging

logger = logging.getLogger(__name__)


def setup_langsmith_tracing(project_name: str = "docuquery-rag") -> bool:
    langsmith_api_key = os.getenv("LANGSMITH_API_KEY")
    
    if not langsmith_api_key:
        logger.info("LANGSMITH_API_KEY not found - tracing disabled")
        os.environ["LANGCHAIN_TRACING_V2"] = "false"
        return False
    
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_PROJECT"] = project_name
    os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
    
    logger.info(f"LangSmith tracing enabled for project: {project_name}")
    return True


def get_tracing_status() -> dict:
    return {
        "enabled": os.getenv("LANGCHAIN_TRACING_V2") == "true",
        "project": os.getenv("LANGCHAIN_PROJECT", "N/A")
    }
