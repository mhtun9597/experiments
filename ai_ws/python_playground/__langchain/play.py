import asyncio
import sys
from typing import Any, Awaitable, Callable, Dict, cast
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

from pydantic import BaseModel, Field

embeddings = OllamaEmbeddings(model="llama3", validate_model_on_init=True)

file_paths = [
    Path("__langchain\\knowledges\\MH Markets.pdf"),
]


loader = UnstructuredLoader(file_paths)
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,  # chunk size (characters)
    chunk_overlap=200,  # chunk overlap (characters)
    add_start_index=True,  # track index in original document
)
all_splits: list[Document] = text_splitter.split_documents(docs)


# path = Path("data/faiss")
# if path.exists():
#     vector_store = FAISS.load_local(
#         "data", embeddings=embeddings, allow_dangerous_deserialization=True
#     )
# else:
index = faiss.IndexFlatL2(4096)

vector_store = FAISS(
    embedding_function=embeddings,
    index=index,
    docstore=InMemoryDocstore(),
    index_to_docstore_id={},
)


vector_store.add_documents(all_splits)


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
def _after_model(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    print("_after_model ware called")
    # messages = state["messages"]
    # print(messages)
    return None


@before_model
async def _before_model(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    print("before_model ware called")
    # messages = state["messages"]
    # print(messages)
    return None


@before_agent
async def _before_agent(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    print("before_agent ware called")

    return None


@after_agent
async def _after_agent(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    print("after_agent ware called")

    return None


@wrap_model_call
async def wwrap_model_call(
    request: ModelRequest,
    handler: Callable[[ModelRequest], Awaitable[ModelResponse]],
) -> ModelResponse:
    print("_wrap_model_call ware called")

    return await handler(request)


class Response(BaseModel):
    ans: str = Field(description="Answer from model")
    tool_calls: list[str] = Field(
        description="List of tool names call during invocation."
    )


@dynamic_prompt
async def _dynamic_prompt(request: ModelRequest) -> str:
    prompt = request.system_prompt
    # await asyncio.sleep(2)
    print("dynamic prompt called ", prompt)
    return prompt


PROMPT = """
You are a routing rule evaluation agent. Your task is to determine the final ordered list of queues for a customer based on routing rules and customer preferences.

# Inputs
You will be given:
1. Routing Rules
  1.1. An ordered list (highest priority first).
  1.2. Each routing rule contains:
    1.2.1. primary_rules: a list of objects { rule: dict, queue: str }
           - Each rule dict can have any arbitrary key-value pairs (e.g., lang, intent, timezone)
    1.2.2. fallback_queue: a list of queue names

2. Customer Preferences
  2.1. A dictionary of customer attributes (any arbitrary key-value pairs)
  2.2. Values may contain spelling mistakes, synonyms, or variations

# Matching Instructions

1. Attribute Normalization
  1.1. Equivalent keys should match: e.g., lang = language, intent = intention
  1.2. Values that are synonyms or have minor spelling mistakes should match: e.g., eng = en, job_seeking = job seaking
  1.3. Normalization happens before evaluating rules

2. Primary Rule Matching
  2.1. A primary rule matches **only if all customer preferences are semantically covered** by the rule
  2.2. If any preference is missing or contradicts the rule, the primary rule is excluded
  2.3. Multiple primary rules from the same routing rule can match — include all in their listed order

3. Wildcard Rules
  3.1. A primary rule with { "*": "*" } matches any customer preference
  3.2. Wildcard rules are treated like normal primary rules; their position in the final queue list depends on their order in the routing rules
  3.3. Wildcards do not automatically appear last — their position respects routing rule priority

4. Fallback Queue Logic
  4.1. If at least one primary rule in a routing rule is selected, append that rule’s fallback_queue **immediately after the matched primary queues**
  4.2. If no primary rule from a routing rule matches, exclude its fallback_queue entirely

5. Queue Deduplication
  5.1. Do not repeat queue names
  5.2. Preserve the first occurrence based on priority

# Output Requirements
1. Output only the final list of queue names as a JSON array. Do not include any explaining text. Refer following example output format.
2. Order must follow priority:
   2.1. Matched primary queues (in their order from routing rules)
   2.2. Their corresponding fallback queues
   2.3. Lower-priority queues appear later, respecting the order in the routing rules
3. Never invent queues


# Example

## Input
Routing Rules:
[
  {
    "primary_rules": [
      { "rule": { "lang": "en", "intent": "withdraw/deposit, account_operations" }, "queue": "en_cs_queue" },
      { "rule": { "lang": "en", "intent": "job seaking" }, "queue": "en_hr_queue" },
      { "rule": { "lang": "en", "intent": "investment" }, "queue": "en_investor_queue" }
    ],
    "fallback_queue": ["en_general"]
  },
  {
    "primary_rules": [
      { "rule": { "*": "*" }, "queue": "Default" }
    ],
    "fallback_queue": []
  }
]

Customer Preferences:
{
  "intent": "job_seeking",
  "language": "eng"
}

## Output
"en_hr_queue", "en_general", "Default"

## Reasoning Summary
1. Normalize attributes: language → lang, job_seeking → job seaking, eng → en
2. Match primary rules that fully cover **all** customer preferences
3. Include all matched primary rules in order
4. Append fallback queues for routing rules with at least one matched primary rule
5. Include wildcard rules according to their position in routing rules
6. Deduplicate queues
"""


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


routing_rules: list[dict[str, Any]] = [
    {
        "primary_rules": [
            {
                "rule": {
                    "lang": "en",
                    "intent": "withdraw/deposit, account_operations",
                },
                "queue": "en_cs_queue",
            },
            {"rule": {"lang": "en", "intent": "job seaking"}, "queue": "en_hr_queue"},
            {
                "rule": {"lang": "en", "intent": "investment"},
                "queue": "en_investor_queue",
            },
        ],
        "fallback_queue": ["en_general"],
    },
    {
        "primary_rules": [
            {
                "rule": {
                    "lang": "zh",
                    "intent": "withdraw/deposit, account_operations",
                },
                "queue": "zh_cs_queue",
            },
            {"rule": {"lang": "zh", "intent": "job seaking"}, "queue": "zh_hr_queue"},
            {
                "rule": {"lang": "zh", "intent": "investment"},
                "queue": "zh_investor_queue",
            },
        ],
        "fallback_queue": ["zh_general"],
    },
    {"primary_rules": [{"rule": {"*": "*"}, "queue": "Default"}], "fallback_queue": []},
]

msg = f"""
Routing Rule: {routing_rules}   
Customer Preferences: intent=$$intent$$, lang=$$lang$$
"""


async def run():
    _model = ChatOllama(
        model="deepseek-r1:8b",
        validate_model_on_init=True,
        reasoning=True
        # other params ...
    )
    agent = create_agent(  # type: ignore
        model=_model,
        middleware=[_dynamic_prompt],
        tools=[],
        system_prompt=SystemMessage(content=PROMPT),
        checkpointer=InMemorySaver(),
    )
    print("Hello sir. I am your little bot. What can i help you?")
    while True:
        inputs = input("\n")
        intent, lang = inputs.split(",")
        cnt = msg.replace("$$intent$$", intent).replace("$$lang$$", lang)
        ans = await agent.ainvoke(  # type: ignore
            {"messages": [HumanMessage(cnt)]},
            {"configurable": {"thread_id" : "1"}}
        )

        print(ans)

        # async for token, metadata in agent.astream(  # type: ignore
        #     {"messages": cnt},  # type: ignore
        #     {"configurable": {"thread_id": "1"}},
        #     stream_mode="messages",
        # ):
        #    print(token)
          


if __name__ == "__main__":
    asyncio.run(run())
