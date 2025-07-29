"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";

export default function SearchPage() {
  const router = useRouter();
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = () => {
    setLoading(true);
    fetch(`http://localhost:9000/search?q=${encodeURIComponent(query)}`)
      .then((res) => res.json())
      .then((data) => {
        setResults(data.results || []);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  };

  return (
    <div style={{ minHeight: "100vh", backgroundColor: "white", color: "black" }}>
    <main style={{ padding: 40 }}>
      <h1>유사 로그 검색</h1>

      <div style={{ marginBottom: 16 }}>
        <input
          value={query}
          onChange={e => setQuery(e.target.value)}
          placeholder="검색어를 입력하세요"
          style={{
            padding: "8px 12px",
            fontSize: 15,
            borderRadius: 4,
            border: "1px solid #ccc",
            marginRight: 8,
          }}
        />
        <button
          style={{
            backgroundColor: "#222",
            color: "white",
            border: "none",
            borderRadius: 6,
            padding: "8px 16px",
            fontSize: 15,
            cursor: "pointer",
            fontWeight: 600,
          }}
          onClick={handleSearch}
          disabled={loading}
        >
          검색
        </button>
      </div>
      {loading ? (
        <div>검색 중...</div>
      ) : (
        <ul>
          {results.map((result, idx) => (
            <li key={idx} style={{ marginBottom: 8 }}>{result}</li>
          ))}
        </ul>
      )}
    </main>
    </div>
  );
}