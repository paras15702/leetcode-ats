"use client";

import { useState } from "react";

export default function Home() {
  const [username, setUsername] = useState("");
  const [role, setRole] = useState("swe_intern");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState("");

  async function analyze() {
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const res = await fetch("http://127.0.0.1:8000/analyze/leetcode", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, role }),
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "Something went wrong");
      }

      const data = await res.json();
      setResult(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen p-8 max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">LeetCode ATS</h1>

      <div className="space-y-4">
        <input
          className="w-full border p-2 rounded"
          placeholder="LeetCode username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />

        <select
          className="w-full border p-2 rounded"
          value={role}
          onChange={(e) => setRole(e.target.value)}
        >
          <option value="swe_intern">SWE Intern</option>
          <option value="backend">Backend Engineer</option>
        </select>

        <button
          onClick={analyze}
          disabled={!username || loading}
          className="w-full bg-black text-white p-2 rounded disabled:opacity-50"
        >
          {loading ? "Analyzing..." : "Analyze"}
        </button>
      </div>

      {error && <p className="text-red-600 mt-4">{error}</p>}

      {result && (
        <div className="mt-8 border rounded p-4 space-y-3">
          <p className="text-xl font-semibold">
            Readiness Score: {result.readiness_score}
          </p>

          <div>
            <p className="font-medium">Strengths</p>
            <p>{result.strengths.length ? result.strengths.join(", ") : "None"}</p>
          </div>

          <div>
            <p className="font-medium">Weaknesses</p>
            <p>{result.weaknesses.length ? result.weaknesses.join(", ") : "None"}</p>
          </div>
        </div>
      )}
    </main>
  );
}
