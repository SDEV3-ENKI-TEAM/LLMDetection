from langchain.schema import Document
import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from dotenv import load_dotenv

load_dotenv()

vectorstore = chromadb.HttpClient(host="43.201.65.178", port="8000")

# collection 있으면 가져오고 없으면 생성
existing_collections = [col.name for col in vectorstore.list_collections()]

if "my_log_db" in existing_collections:
    collection = vectorstore.get_collection(name="my_log_db")
else:
    collection = vectorstore.create_collection(
        name="my_log_db",
        embedding_function=OpenAIEmbeddingFunction(model_name="text-embedding-3-small"),
        metadata={"hnsw:space": "cosine"},
    )
