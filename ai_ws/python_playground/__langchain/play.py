import asyncio
import sys
from typing import Any, Awaitable, Callable, Dict, cast
import aiofiles
from langchain_core.language_models import ModelProfile
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain.messages import SystemMessage, HumanMessage
from langgraph.runtime import Runtime
import ollama
from langchain.agents.middleware import (
    before_model,
    before_agent,
    wrap_model_call,
    after_model,
    after_agent,
    AgentState,
    ModelRequest,
    ModelResponse,
)
from langchain.agents.middleware import SummarizationMiddleware

from langchain.agents.middleware.types import before_agent
from langchain.tools import tool, ToolRuntime
from langgraph.checkpoint.memory import InMemorySaver
from langchain_unstructured import UnstructuredLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore

from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document
from pathlib import Path
from langchain.agents.middleware import HumanInTheLoopMiddleware, dynamic_prompt
import json
from langchain.agents.structured_output import ToolStrategy

from pydantic import BaseModel, Field

# from pydantic import BaseModel, Field

# embeddings = OllamaEmbeddings(model="llama3", validate_model_on_init=True)

# file_paths = [
#     Path("__langchain\\knowledges\\MH Markets.pdf"),
# ]


# loader = UnstructuredLoader(file_paths)
# docs = loader.load()

# text_splitter = RecursiveCharacterTextSplitter(
#     chunk_size=1000,  # chunk size (characters)
#     chunk_overlap=200,  # chunk overlap (characters)
#     add_start_index=True,  # track index in original document
# )
# all_splits: list[Document] = text_splitter.split_documents(docs)


# path = Path("data/faiss")
# if path.exists():
#     vector_store = FAISS.load_local(
#         "data", embeddings=embeddings, allow_dangerous_deserialization=True
#     )
# else:
# index = faiss.IndexFlatL2(4096)

# vector_store = FAISS(
#     embedding_function=embeddings,
#     index=index,
#     docstore=InMemoryDocstore(),
#     index_to_docstore_id={},
# )


# vector_store.add_documents(all_splits)


print("successfully added documents ")


@tool
def send_email(recipient: str, subj: str, body: str) -> str:
    """
    Send email to a recipient
    Args:
      recipient (str) : recipient address
      subj (str) : subject of email
      body (str) : email bdoy

    Returns:
      Confirmation Message
    """
    print("called sent email")
    return f"Successfully sent email to {recipient}"


@tool
def handoff(case: str, runtime: ToolRuntime) -> str:
    """
    Hanoff to an agent
    Args:
      case (str): User asking case like withdrawl/deposit.
    Returns:
      str: Result whether handoff successfully or not
    """
    print("Handoff tool is called", case)
    return "Successfully transfered."


@tool
def summerize(title: str, runtime: ToolRuntime) -> None:
    """
    Insert generated summerized title to the DB.
    Args:
      title (str) : Generated Summerized title.
    Returns
      None
    """
    print(f"Successfully inserted generated title {title}")

    # @tool
    # async def retrive_context(
    #     query: str, runtime: ToolRuntime
    # ) -> tuple[str, list[Document]]:
    #     """
    #     Retrieve information to help answer a query.
    #     Args:
    #       query (str) : What user ask.
    #     Returns:
    #       tuple : ( Serialized form of retrived doc, Orignal Retrived Docs.)
    #     """

    # retrieved_docs = await vector_store.asimilarity_search(query, k=2)  # type: ignore


#     serialized = "\n\n".join(
#         (f"Source: {doc.metadata}\nContent: {doc.page_content}")  # type: ignore
#         for doc in retrieved_docs
#     )
#     # print("Retrived DOC ", retrieved_docs)
#     # print("Seralized ", serialized)
#     return serialized, retrieved_docs


@after_model
async def _after_model(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    print("_after_model ware called")
    messages = state["messages"]
    print(messages)
    return None


@before_model
async def _before_model(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    print("before_model ware called")
    messages = state["messages"]
    print(messages)
    return None


@before_agent
async def _before_agent(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    print("before_agent ware called")
    messages = state["messages"]
    print(messages)
    return None


@after_agent
async def _after_agent(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    print("after_agent ware called")
    messages = state["messages"]
    print(messages)
    return None


@wrap_model_call
async def wwrap_model_call(
    request: ModelRequest,
    handler: Callable[[ModelRequest], Awaitable[ModelResponse]],
) -> ModelResponse:
    print("_wrap_model_call ware called")

    return await handler(request)


# class Response(BaseModel):
#     ans: str = Field(description="Answer from model")
#     tool_calls: list[str] = Field(
#         description="List of tool names call during invocation."
#     )


# @dynamic_prompt
# async def _dynamic_prompt(request: ModelRequest) -> str:
#     prompt = request.system_prompt
#     # await asyncio.sleep(2)
#     print("dynamic prompt called ", prompt)
#     return prompt


from langchain.messages import AIMessage, AIMessageChunk, AnyMessage, ToolMessage


def _render_message_chunk(token: AIMessageChunk) -> None:
    if token.text:
        print(token.text, end="|")
    if token.tool_call_chunks:
        print("tool call chunk ", token.tool_call_chunks)
    # N.B. all content is available through token.content_blocks


def _render_completed_message(message: AnyMessage) -> None:
    if isinstance(message, AIMessage) and message.tool_calls:
        print(f"Tool calls: {message.tool_calls}")
    if isinstance(message, ToolMessage):
        print(f"Tool response: {message.content_blocks}")


import io

PROMPT: str = """
You are a conversation summarization agent.

Summarize the conversation clearly, concisely, and accurately.

Focus on:
- what the conversation is about
- any goal, request, decision, or important context already expressed
"""

# PROMPT: str = """
# You are a context compression agent.

# Compress the conversation clearly and concisely to reduce context window usage for a downstream agent.

# Focus on:
# - the important information expressed in the conversation
# - key facts, context, decisions, constraints, and relevant details
# - anything that should not be lost during compression

# Rules:
# - compress the whole conversation while keeping important information
# - remove repetition, filler, and low-value history
# - prefer the latest confirmed information if something changed
# - do not invent missing context
# - write a summary, not a transcript
# """


class Summary(BaseModel):
    title: str = Field(description="Title of summary")
    summary: str = Field(description="Full expression of summary")
    lang: str = Field(description="Language used in the conversation")
    intentions: list[str] = Field(description="Human intentions", default=[])
    sentiment: list[str] = Field(description="Setiment that agent have", default=[])
    outcome: str | None = Field(description="Overall evaluated outcome", default=None)


from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
import aiosqlite


async def run():
    conn = await aiosqlite.connect("__langchain/checkpoint.db")

    checkpointer = AsyncSqliteSaver(conn=conn)

    await checkpointer.setup()
    _model = ChatOllama(
        model="gemma4:e4b",
        validate_model_on_init=True,
        profile=ModelProfile(max_input_tokens=1000),
        # other params ...
    )

    # async with aiofiles.open("2.png", "rb") as f:
    #     b = await f.read()
    # import base64

    # with open("1.pdf", "rb") as f:
    #     encoded = base64.b64encode(f.read()).decode("utf-8")
    # print(f"B64 {encoded}")

    # loader = UnstructuredLoader(
    #     file=io.BytesIO(b),
    #     chunking_strategy="basic",
    #     max_characters=1000000,
    #     metadata_filename="1.pdf",
    # )

    # docs = await loader.aload()

    # for doc in docs:
    #     print(doc.page_content)

    while True:
        inputs = input("Ask Anything \n")

        agent = create_agent(
            model=_model,
            middleware=[
                _before_model,
                _after_agent,
                _before_agent,
                _after_model,
                wwrap_model_call,
            ],
            tools=[],
            system_prompt="AI Agent",
            # response_format=ToolStrategy(Summary),
            checkpointer=checkpointer,
        )

        ans = await agent.ainvoke(  # type: ignore
            {"messages": [HumanMessage(inputs)]},
            {"configurable": {"thread_id": "1234"}},
            # type: ignore
        )

        messages = ans["messages"]

        print(messages)

    # async for token, metadata in agent.astream(  # type: ignore
    #     {"messages": [HumanMessage(content=[{"type": "text", "text": "where is india?"}])]},  # type: ignore
    #     {"configurable": {"thread_id": "1"}},
    #     stream_mode="messages",
    # ):
    #     _render_message_chunk(token)

    # async for token, metadata in agent.astream(  # type: ignore
    #     {"messages": [HumanMessage(content=[{"type": "text", "text": "where is china?"}])]},  # type: ignore
    #     {"configurable": {"thread_id": "1"}},
    #     stream_mode="messages",
    # ):
    #     _render_message_chunk(token)


if __name__ == "__main__":
    asyncio.run(run())
