import pandas as pd
from kafka import KafkaProducer
from workflow import build_workflow

graph, retriever = build_workflow()

def handle_completed_trace(trace_id, df):
    """
    완성된 trace DataFrame을 LangGraph에 넘기고 처리
    """
    print(f"\n=== Trace Completed: {trace_id} ===")
    # print(df)

    # DataFrame → LangGraph 입력용 cleaned_trace
    cleaned_trace = df.to_json(orient="records", force_ascii=False)

    input_state = {
        "trace_id": trace_id,
        "cleaned_trace": cleaned_trace,
        "similar_logs": [],
        "llm_output": "",
        "decision": "",
        "reason": "",
        "retriever": retriever,
    }

    # LangGraph 실행
    result = graph.invoke(input_state)

    print(f"\n[LangGraph Result for Trace {trace_id}]")
    for k, v in result.items():
        print(f"{k}: {v}")

    # Kafka Producer
    producer = KafkaProducer(bootstrap_servers="localhost:9092")
    message = f"Trace {trace_id} Result: {result}"
    producer.send("processed_trace", message.encode("utf-8"))
    producer.flush()
    print(f"[Producer] 전송 완료: Trace {trace_id}")
