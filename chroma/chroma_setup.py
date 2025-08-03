from langchain.schema import Document
import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

# API 키 로드
from dotenv import load_dotenv

load_dotenv()

vectorstore = chromadb.HttpClient(host="43.201.65.178", port="8000")

# Chroma DB 컬렉션 삭제
vectorstore.delete_collection(name="my_log_db")

# 컬렉션 새로 생성 및 데이터 추가
collection = vectorstore.create_collection(
    name="my_log_db",
    embedding_function=OpenAIEmbeddingFunction(model_name="text-embedding-3-small"),
    metadata={"hnsw:space": "cosine"},
)

# 샘플 데이터(원본+메타)
samples = [
    {
        "doc_id": "log_1",
        "cleaned_trace": "database connection refused error",
        "metadata": {
            "label": "anomaly",
            "decision": "suspicious",
            "reason": "Database service is unreachable, indicating potential outage or misconfiguration.",
            "judgement": "error",
        },
    },
    {
        "doc_id": "log_2",
        "cleaned_trace": "user login successful from 192.168.1.10",
        "metadata": {
            "label": "normal",
            "decision": "normal",
            "reason": "Expected successful login from known IP.",
            "judgement": "ok",
        },
    },
    {
        "doc_id": "log_3",
        "cleaned_trace": "multiple failed ssh login attempts from unknown ip",
        "metadata": {
            "label": "anomaly",
            "decision": "suspicious",
            "reason": "Brute force attack suspected due to repeated failed logins.",
            "judgement": "warning",
        },
    },
    {
        "doc_id": "log_4",
        "cleaned_trace": "file /etc/passwd modified",
        "metadata": {
            "label": "anomaly",
            "decision": "suspicious",
            "reason": "Critical system file modified unexpectedly.",
            "judgement": "critical",
        },
    },
    {
        "doc_id": "log_5",
        "cleaned_trace": "system backup completed successfully",
        "metadata": {
            "label": "normal",
            "decision": "normal",
            "reason": "Regular scheduled backup finished without errors.",
            "judgement": "ok",
        },
    },
    {
        "doc_id": "log_6",
        "cleaned_trace": "high cpu usage detected on server",
        "metadata": {
            "label": "anomaly",
            "decision": "suspicious",
            "reason": "Unusual CPU spike could indicate heavy load or malware.",
            "judgement": "warning",
        },
    },
    {
        "doc_id": "log_7",
        "cleaned_trace": "disk space usage at 75 percent",
        "metadata": {
            "label": "normal",
            "decision": "normal",
            "reason": "Disk usage within acceptable threshold.",
            "judgement": "ok",
        },
    },
    {
        "doc_id": "log_8",
        "cleaned_trace": "unauthorized access to admin panel detected",
        "metadata": {
            "label": "anomaly",
            "decision": "suspicious",
            "reason": "Access attempt to admin panel without valid credentials.",
            "judgement": "critical",
        },
    },
    {
        "doc_id": "log_9",
        "cleaned_trace": "scheduled cron job executed",
        "metadata": {
            "label": "normal",
            "decision": "normal",
            "reason": "Cron job ran at its scheduled time.",
            "judgement": "ok",
        },
    },
    {
        "doc_id": "log_10",
        "cleaned_trace": "unexpected service restart detected",
        "metadata": {
            "label": "anomaly",
            "decision": "suspicious",
            "reason": "Service restarted unexpectedly, possible crash or external trigger.",
            "judgement": "warning",
        },
    },
]

# collection에 넣기
collection.add(
    ids=[s["doc_id"] for s in samples],
    documents=[s["cleaned_trace"] for s in samples],
    metadatas=[s["metadata"] for s in samples],
)
