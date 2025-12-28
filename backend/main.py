from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from scoring import calculate_score
from leetcode_client import fetch_leetcode_stats
from topic_groups import TOPIC_GROUPS
from scoring import normalize_topics  
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="LeetCode ATS")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



class AnalyzeUsernameRequest(BaseModel):
    username: str
    role: str

@app.post("/analyze/leetcode")
async def analyze_leetcode_profile(req: AnalyzeUsernameRequest):
    stats = await fetch_leetcode_stats(req.username)

    if not stats:
        raise HTTPException(status_code=404, detail="LeetCode user not found")


    normalized_topics = normalize_topics(stats["topics"])

    result = calculate_score(
        stats={
            "easy": stats["easy"],
            "medium": stats["medium"],
            "hard": stats["hard"],
            "topics": normalized_topics
        },
        role=req.role
    )

    return {
        "username": req.username,
        "leetcode_stats": stats,
        "normalized_topics": normalized_topics,
        **result
    }
