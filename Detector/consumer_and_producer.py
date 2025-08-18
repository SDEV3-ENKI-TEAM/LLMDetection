import json
import pandas as pd
from kafka import KafkaConsumer
from collections import defaultdict
from processor import handle_completed_trace

trace_buffer = defaultdict(list)
trace_end_flags = defaultdict(dict)

consumer = KafkaConsumer(
    'raw_trace',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

print("[Kafka Consumer Started] Waiting for messages...")

for message in consumer:
    data = message.value
    try:
        for resource_span in data.get("resourceSpans", []):
            for scope_span in resource_span.get("scopeSpans", []):
                for span in scope_span.get("spans", []):
                    trace_id = span.get("traceId")
                    span_id = span.get("spanId")

                    attributes = {
                        attr["key"]: list(attr["value"].values())[0]
                        for attr in span.get("attributes", [])
                    }

                    row = {
                        "traceId": trace_id,
                        "spanId": span_id,
                        "parentSpanId": span.get("parentSpanId"),
                        "name": span.get("name"),
                        "startTime": span.get("startTimeUnixNano"),
                        "endTime": span.get("endTimeUnixNano"),
                        "status_code": span.get("status", {}).get("code"),
                        "status_message": span.get("status", {}).get("message")
                    }
                    row.update(attributes)

                    trace_buffer[trace_id].append(row)
                    is_ended = bool(span.get("endTimeUnixNano"))
                    trace_end_flags[trace_id][span_id] = is_ended

                    # 모든 span 종료 확인
                    if trace_end_flags[trace_id] and all(trace_end_flags[trace_id].values()):
                        df = pd.DataFrame(trace_buffer[trace_id])
                        handle_completed_trace(trace_id, df)
                        trace_buffer.pop(trace_id, None)
                        trace_end_flags.pop(trace_id, None)

    except Exception as e:
        print(f"[Error] Failed to process message: {e}")
