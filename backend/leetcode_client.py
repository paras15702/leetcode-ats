import httpx

LEETCODE_GRAPHQL_URL = "https://leetcode.com/graphql"


QUERY = """
query getUserProfile($username: String!) {
  matchedUser(username: $username) {
    submitStats {
      acSubmissionNum {
        difficulty
        count
      }
    }
    tagProblemCounts {
      fundamental {
        tagName
        problemsSolved
      }
      intermediate {
        tagName
        problemsSolved
      }
      advanced {
        tagName
        problemsSolved
      }
    }
  }
}
"""


async def fetch_leetcode_stats(username: str):
    payload = {
        "query": QUERY,
        "variables": {"username": username}
    }

    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.post(LEETCODE_GRAPHQL_URL, json=payload)
        resp.raise_for_status()
        data = resp.json()

    user = data.get("data", {}).get("matchedUser")
    if not user:
        return None


    parsed = {"easy": 0, "medium": 0, "hard": 0}
    for item in user["submitStats"]["acSubmissionNum"]:
        parsed[item["difficulty"].lower()] = item["count"]


    topics = {}

    for level in ["fundamental", "intermediate", "advanced"]:
        for tag in user["tagProblemCounts"][level]:
            topics[tag["tagName"].lower()] = tag["problemsSolved"]

    parsed["topics"] = topics
    return parsed

