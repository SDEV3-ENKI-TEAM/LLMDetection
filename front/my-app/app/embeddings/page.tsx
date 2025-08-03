"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

type Embedding = {
  text: string;
  embedding: number[];
};

export default function EmbeddingPage() {
  const router = useRouter();
  const [embeddings, setEmbeddings] = useState<Embedding[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:9000/embeddings")
      .then((res) => res.json())
      .then((data) => {
        setEmbeddings(data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  return (
<div style={{ minHeight: "100vh", backgroundColor: "white", color: "black" }}>
    <main style={{ padding: 40}}>
      <h1>임베딩 벡터</h1>

      {loading ? (
        <div>불러오는 중...</div>
      ) : (
        <ul>
          {embeddings.map((item, idx) => (
            <li key={idx} style={{ marginBottom: 12 }}>
              <div>
                <b>{item.text}</b>
              </div>
              <div style={{ fontSize: 13, color: "#555" }}>
                {item.embedding.join(", ")}
              </div>
            </li>
          ))}
        </ul>
      )}
    </main>
    </div>
  );
}