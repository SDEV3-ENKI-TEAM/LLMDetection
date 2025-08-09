# consumer.py
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    "langgraph-test-topic",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    group_id="test-group",
    enable_auto_commit=True,
)

print("🔥 Consumer 시작됨. 메시지 수신 대기 중...")

for message in consumer:
    print(f"[Consumer] 받은 메시지: {message.value.decode('utf-8')}")

