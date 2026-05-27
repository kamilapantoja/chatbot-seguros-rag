"""RAG chain — retrieval no Chroma + chamada ao LLM da Spark."""
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.messages import SystemMessage, HumanMessage

import config
from llm import get_llm
from prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE


def get_retriever():
    embeddings = HuggingFaceEmbeddings(
        model_name=config.EMBEDDING_MODEL,
        model_kwargs={"device": config.EMBEDDING_DEVICE},
        encode_kwargs={"normalize_embeddings": True},
    )
    vs = Chroma(
        collection_name=config.COLLECTION_NAME,
        persist_directory=str(config.DATA_CHROMA),
        embedding_function=embeddings,
    )
    return vs.as_retriever(search_kwargs={"k": config.RETRIEVAL_TOP_K})


def format_context(docs: list[Document]) -> str:
    blocks = []
    for i, d in enumerate(docs, 1):
        src = d.metadata.get("source", "desconhecido")
        blocks.append(f"[Trecho {i} | fonte: {src}]\n{d.page_content.strip()}")
    return "\n\n---\n\n".join(blocks)


class RAGChain:
    def __init__(self):
        self.retriever = get_retriever()
        self.llm = get_llm()

    def answer(self, question: str) -> dict:
        docs = self.retriever.invoke(question)
        context = format_context(docs)
        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=USER_PROMPT_TEMPLATE.format(context=context, question=question)),
        ]
        response = self.llm.invoke(messages)
        return {
            "question": question,
            "answer": response.content,
            "sources": [d.metadata.get("source", "?") for d in docs],
            "context_used": context,
        }

    async def astream_answer(self, question: str):
        docs = self.retriever.invoke(question)
        context = format_context(docs)
        sources = [d.metadata.get("source", "?") for d in docs]
        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=USER_PROMPT_TEMPLATE.format(context=context, question=question)),
        ]
        async for chunk in self.llm.astream(messages):
            yield {"type": "token", "content": chunk.content}
        yield {"type": "sources", "content": sources}


if __name__ == "__main__":
    chain = RAGChain()
    q = "Como faço para acionar o seguro de automóvel em caso de roubo?"
    print(f"P: {q}\n")
    result = chain.answer(q)
    print("R:", result["answer"])
    print("\nFontes:", result["sources"])
