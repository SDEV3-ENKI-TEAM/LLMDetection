# Opensearch -> Kafka -> Chroma DB
# 로그 추가 시 kafka를 이용해 chroma db에 추카
from fastapi import FastAPI
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document
from chromadb.config import Settings

app = FastAPI()

# API 키를 환경변수로 관리하기 위한 설정 파일
from dotenv import load_dotenv

# API 키 정보 로드
load_dotenv()

client_settings = Settings(
    chroma_api_impl="chromadb.api.fastapi.FastAPI",
    chroma_server_host="43.201.65.178",  # chromadb 서버의 IP 주소
    chroma_server_http_port=8000,  # 서버에서 사용하는 포트
)

cleaned_trace_list = [
    "GET /login 200 OK",
    "POST /api/login 500 internal server error",
    "user not found",
    "authentication failed for user root",
    "database connection timeout",
    "session expired redirect to /login",
    "unauthorized access attempt detected",
    "file not found: /var/tmp/data.csv",
    "systemd failed to start nginx",
    "email verification code invalid",
]

embedding_model = OpenAIEmbeddings()
traces_to_documents = [Document(page_content=log) for log in cleaned_trace_list]
embeddings = embedding_model.embed_documents(
    [doc.page_content for doc in traces_to_documents]
)

# (필요하다면) 컬렉션 새로 생성 및 데이터 추가
db = Chroma(
    collection_name="my_log_db",
    embedding_function=embedding_model,
    client_settings=client_settings,
)

db.add_documents(documents=traces_to_documents, embeddings=embeddings)


@app.get("/logs")
def get_logs():
    # 컬렉션의 모든 문서(page_content) 반환
    docs = db.similarity_search("", k=100)  # 빈 쿼리로 최대 100개 반환
    return {"logs": [doc.page_content for doc in docs]}


@app.get("/search")
def search_logs(q: str, k: int = 5):
    # 쿼리로 유사 로그 검색
    docs = db.similarity_search(q, k=k)
    return {"results": [doc.page_content for doc in docs]}


@app.get("/embeddings")
def get_embeddings():
    # 컬렉션에서 임베딩 벡터와 원본 텍스트를 모두 가져옴
    # limit=10: 최대 10개만 예시로 출력
    data = db._collection.get(include=["embeddings", "documents"], limit=10)
    result = []
    for doc, emb in zip(data["documents"], data["embeddings"]):
        result.append(
            {"text": doc, "embedding": list(emb[:10])}  # numpy 배열을 list로 변환
        )
    return result


@app.delete("/clear")
def reset_collection():
    # 모든 document ID 가져오기
    all_ids = db._collection.get(include=[])["ids"]

    if all_ids:
        db._collection.delete(ids=all_ids)

    return {"status": f"{len(all_ids)} documents deleted"}


from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 또는 ["http://localhost:3000"] 등 Next.js 주소
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
