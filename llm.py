"""Cliente LLM — chama o Ollama na Spark via SSH tunnel."""
from langchain_ollama import ChatOllama
import config


def get_llm() -> ChatOllama:
    return ChatOllama(
        base_url=config.OLLAMA_BASE_URL,
        model=config.LLM_MODEL,
        temperature=config.LLM_TEMPERATURE,
        num_ctx=config.LLM_NUM_CTX,
    )
