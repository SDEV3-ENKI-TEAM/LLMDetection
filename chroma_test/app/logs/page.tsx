"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

export default function LogsPage() {
  const router = useRouter();
  const [logs, setLogs] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:9000/logs")
      .then((res) => res.json())
      .then((data) => {
        setLogs(data.logs || []);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  return (
    <div style={{ minHeight: "100vh", backgroundColor: "white", color: "black" }}>
    <main style={{ padding: 40}}>
      <h1>로그 목록</h1>

      {loading ? (
        <div>불러오는 중...</div>
      ) : (
        <ul>
          {logs.map((log, idx) => (
            <li key={idx} style={{ marginBottom: 8 }}>{log}</li>
          ))}
        </ul>
      )}
    </main>
    </div>
  );
}