from Detector.langgraph_node import (
    search_similar_logs,
    llm_judgment,
    final_decision,
    save_final_decision_to_chroma,
    TraceState,
    retriever,
)
from langgraph.graph import StateGraph, END
from kafka import KafkaProducer

import time

# from dotenv import load_dotenv

# load_dotenv()

# opensearch_setup.py 실행
from opensearch_setup import summarized


# LangGraph 생성
workflow = StateGraph(TraceState)

workflow.add_node("SimilaritySearch", search_similar_logs)
workflow.add_node("LLMJudgment", llm_judgment)
workflow.add_node("Decision", final_decision)
workflow.add_node("SaveToChroma", save_final_decision_to_chroma)

workflow.set_entry_point("SimilaritySearch")  # 시작 노드
workflow.add_edge("SimilaritySearch", "LLMJudgment")
workflow.add_edge("LLMJudgment", "Decision")
workflow.add_edge("Decision", "SaveToChroma")
workflow.add_edge("SaveToChroma", END)  # 종료 노드

graph = workflow.compile()

langgraph_results = []
for trace in summarized:
    input_state = {
        "trace_id": trace["trace_id"],
        "cleaned_trace": trace["summary"],
        "similar_logs": [],
        "llm_output": "",
        "decision": "",
        "reason": "",
        "retriever": retriever,
    }
    result = graph.invoke(input_state)
    langgraph_results.append(result)

# 결과 출력
for i, res in enumerate(langgraph_results):
    print(f"==== 로그 {i+1} 결과 ====")
    for k, v in res.items():
        print(f"{k}: {v}")


producer = KafkaProducer(bootstrap_servers="localhost:9092")
for i, result in enumerate(langgraph_results):
    message = f"Log {i+1} Result: {result}"
    producer.send("langgraph-test-topic", message.encode("utf-8"))
    print(f"[Producer] 전송: Log {i+1}")
    time.sleep(1)

producer.flush()
