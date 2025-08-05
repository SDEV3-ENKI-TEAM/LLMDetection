from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from chroma_setup import vectorstore

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db_collection = vectorstore.get_collection(name="my_log_db")


@app.get("/", response_class=HTMLResponse)
def default():
    return """
    <h2>Welcome to the Chroma DB API</h2>
    <p>Move to <a href="/logs">/logs</a>, <a href="/embeddings/">/embeddings/</a>, or <a href="/search">/search</a> to interact with the database.</p>
    """


@app.get("/logs")
def get_logs():
    data = db_collection.get(include=["documents", "metadatas"])
    return {
        "original": data.get("documents", []),
        "metadata": data.get("metadatas", []),
    }


@app.get("/search")
def search_logs(q: str, threshold: float = 1.0):
    try:
        results = db_collection.query(query_texts=[q], n_results=5)
        ids = results.get("ids", [])
        docs = results.get("documents", [])
        distances = results.get("distances", [])

        # 임계값 이상(이하)인 결과만 필터링, 거리가 작을수록 유사도 높음이라고 가정
        filtered = []
        for _id, doc, dist in zip(ids, docs, distances):
            # if dist <= threshold:  # 임계값 이하일 때만 포함
            filtered.append({"id": _id, "document": doc, "score": dist})

        return {"results": filtered}

    except Exception as e:
        return {"error": str(e)}


@app.get("/embeddings")
def get_embeddings():
    data = db_collection.get(include=["embeddings", "documents"], limit=10)
    result = []
    for doc, emb in zip(data.get("documents", []), data.get("embeddings", [])):
        # numpy 배열일 경우 tolist() 사용
        emb_list = emb.tolist() if hasattr(emb, "tolist") else list(emb)
        result.append(
            {"text": doc, "embedding": emb_list[:10]}
        )  # 임베딩 앞 10개만 반환
    return result
