import asyncio
from langchain_ollama import OllamaEmbeddings
from langchain_unstructured import UnstructuredLoader
from langchain_community.vectorstores import FAISS
import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
import aiofiles
import io


async def get_source_bytes(path: str) -> bytes:
    async with aiofiles.open(path, "rb") as f:
        return await f.read()


async def run():
    # model1 = OllamaEmbeddings(
    #     model="nomic-embed-text",
    #     validate_model_on_init=True,
    #     base_url="http://mohicans:mohicans_6123@91.72.121.198:8000/ollama/",
    # )

    model2 = OllamaEmbeddings(
        model="qwen3-embedding:8b",
        validate_model_on_init=True,
        base_url="http://mohicans:mohicans_6123@91.72.121.198:8000/ollama/",
    )
    file_name = "2.png"
    # dim1 = await model1.aembed_query("testing")
    dim2 = await model2.aembed_query("testing")
    b = await get_source_bytes(f"__langchain/knowledges/{file_name}")

    loader = UnstructuredLoader(
        file=io.BytesIO(b),
        chunking_strategy="basic",
        metadata_filename=file_name,
    )

    docs = await loader.aload()

    print(docs)

    # faiss1 = FAISS(
    #     embedding_function=model1,
    #     index=faiss.IndexFlatL2(len(dim1)),
    #     docstore=InMemoryDocstore(),
    #     index_to_docstore_id={},
    # )

    # await faiss1.aadd_documents(docs)

    faiss2 = FAISS(
        embedding_function=model2,
        index=faiss.IndexFlatL2(len(dim2)),
        docstore=InMemoryDocstore(),
        index_to_docstore_id={},
    )
    await faiss2.aadd_documents(docs)

    # result1 = await faiss1.asimilarity_search("Europe deposit Group")  # type: ignore
    # print(result1)

    # result2 = await faiss2.asimilarity_search("Europe deposit Group")  # type: ignore
    # print(result2)


if __name__ == "__main__":
    asyncio.run(run())
