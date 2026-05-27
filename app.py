"""Chainlit app — UI conversacional do chatbot Dracarys."""
import chainlit as cl

from rag import RAGChain


@cl.on_chat_start
async def start():
    chain = RAGChain()
    cl.user_session.set("chain", chain)
    await cl.Message(
        content=(
            "🐉 **Olá! Eu sou o assistente da Dracarys Seguros.**\n\n"
            "Posso te ajudar com dúvidas sobre apólices, sinistros, coberturas e regulamentação. "
            "Como posso te ajudar hoje?"
        ),
    ).send()


@cl.on_message
async def on_message(message: cl.Message):
    chain: RAGChain = cl.user_session.get("chain")
    msg = cl.Message(content="")
    await msg.send()

    sources: list[str] = []
    async for event in chain.astream_answer(message.content):
        if event["type"] == "token":
            await msg.stream_token(event["content"])
        elif event["type"] == "sources":
            sources = event["content"]

    if sources:
        unique = []
        for s in sources:
            if s not in unique:
                unique.append(s)
        footer = "\n\n---\n📚 **Trechos consultados:**\n" + "\n".join(f"- `{s}`" for s in unique)
        await msg.stream_token(footer)

    await msg.update()
