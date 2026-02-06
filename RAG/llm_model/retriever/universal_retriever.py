import json
import re
from pathlib import Path
from typing import List, Dict

BASE_DIR = Path(__file__).resolve().parents[2]
CHUNK_DIR = BASE_DIR / "data_chunk"


def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)

    synonyms = {
        "informations": "information",
        "details": "detail",
        "fees": "fee",
        "placements": "placement",
        "hostels": "hostel",
        "clubs": "club",
        "societies": "club",
        "numbers": "contact",
        "phone": "contact",
        "email": "contact",
        "address": "contact",
        "all": "all",
        "complete": "all",
        "full": "all",
        "list": "all",
    }

    for k, v in synonyms.items():
        text = text.replace(k, v)

    return text.strip()


# ---------------- Load All Chunks ----------------

def load_all_chunks() -> List[Dict]:
    chunks = []

    for file in CHUNK_DIR.glob("*_chunks.json"):
        try:
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    chunks.extend(data)
        except Exception as e:
            print(f"❌ Failed to load {file.name}: {e}")

    return chunks


# ---------------- Intent Helpers ----------------

def is_all_intent(query: str) -> bool:
    return any(w in query for w in ["all", "complete", "full", "list"])


def is_single_fact_intent(query: str) -> bool:
    return any(w in query for w in [
        "what is",
        "who is",
        "where is",
        "how many",
        "contact",
        "email",
        "phone",
        "address"
    ])


# ---------------- Scoring ----------------

def score_chunk(query_words: List[str], chunk: Dict) -> int:
    searchable = normalize(
        (chunk.get("question") or "") + " " +
        (chunk.get("answer") or "") + " " +
        " ".join(chunk.get("keywords", []))
    )

    score = 0

    for w in query_words:
        if w in searchable:
            score += 2

    # Category boost
    category = normalize(chunk.get("category", ""))
    if any(w in category for w in query_words):
        score += 3

    return score


# ---------------- Universal Retriever ----------------

def retrieve_chunks(query: str, top_k: int = 3) -> List[Dict]:
    query = normalize(query)
    query_words = query.split()

    all_chunks = load_all_chunks()
    scored = []

    for chunk in all_chunks:
        s = score_chunk(query_words, chunk)
        if s > 0:
            scored.append((s, chunk))

    if not scored:
        return []

    scored.sort(key=lambda x: x[0], reverse=True)

    # ALL / LIST intent → return all relevant unique chunks
    if is_all_intent(query):
        seen = set()
        results = []
        for _, chunk in scored:
            cid = chunk.get("id")
            if cid not in seen:
                seen.add(cid)
                results.append(chunk)
        return results

    # Single fact intent → best match only
    if is_single_fact_intent(query):
        return [scored[0][1]]

    # Default → top K
    return [c for _, c in scored[:top_k]]