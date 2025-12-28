from roles import ROLES
from topic_groups import TOPIC_GROUPS

def normalize_topics(raw_topics: dict):
    normalized = {}

    for canonical, variants in TOPIC_GROUPS.items():
        normalized[canonical] = sum(
            raw_topics.get(v, 0) for v in variants
        )

    return normalized


def calculate_score(stats: dict, role: str):
    role_cfg = ROLES[role]

    base_score = (
        stats["easy"] * role_cfg["easy"] +
        stats["medium"] * role_cfg["medium"] +
        stats["hard"] * role_cfg["hard"]
    )


    topic_score = 0
    strengths = []
    weaknesses = []

    for topic, count in stats["topics"].items():
        weight = role_cfg["topics"].get(topic, 0)
        topic_score += count * weight

        if count >= 15:
            strengths.append(topic)
        elif count < 5:
            weaknesses.append(topic)

    raw_score = base_score + topic_score


    normalized = min(100, round(raw_score / 10))

    return {
        "readiness_score": normalized,
        "strengths": strengths,
        "weaknesses": weaknesses
    }
