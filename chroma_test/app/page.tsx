"use client";
import { useRouter } from "next/navigation";
import { useState } from "react";

export default function Home() {
  const router = useRouter();
  const [deleting, setDeleting] = useState(false);
  const [deleteMsg, setDeleteMsg] = useState("");

  const buttonStyle = {
  backgroundColor: "#222",   // 어두운 배경
  color: "white",            // 흰색 글씨
  border: "none",
  borderRadius: 6,
  padding: "12px 24px",
  fontSize: 16,
  cursor: "pointer",
  fontWeight: 600,
  boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
  transition: "background 0.2s",
  };

  const handleDelete = async () => {
    setDeleting(true);
    setDeleteMsg("");
    try {
      const res = await fetch("http://localhost:9000/clear", { method: "DELETE" });
      if (res.ok) {
        setDeleteMsg("Chroma DB 내용이 성공적으로 삭제되었습니다.");
      } else {
        setDeleteMsg("삭제에 실패했습니다.");
      }
    } catch {
      setDeleteMsg("삭제 요청 중 오류가 발생했습니다.");
    }
    setDeleting(false);
  };


  return (
    <main style={{ padding: 40 }}>
      <h1 style={{padding:40, backgroundColor: "white", color: "black"}}>Chroma DB 테스트</h1>
      <div style={{ display: "flex", gap: 16, marginTop: 24 }}>
        <button style={buttonStyle} onClick={() => router.push("/logs")}>로그 목록</button>
        <button style={buttonStyle} onClick={() => router.push("/embeddings")}>임베딩 벡터</button>
        <button style={buttonStyle} onClick={() => router.push("/search")}>유사 로그 검색</button>
        <button
          style={{ ...buttonStyle, backgroundColor: "#b71c1c" }}
          onClick={handleDelete}
          disabled={deleting}
        >
          {deleting ? "삭제 중..." : "Chroma DB 내용 지우기"}
        </button>
      </div>
      {deleteMsg && (
        <div style={{ marginTop: 24, color: "#b71c1c", fontWeight: 600 }}>{deleteMsg}</div>
      )}
    </main>
  );
}