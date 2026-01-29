import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
CHUNK_DIR = BASE_DIR / "data_chunk"

def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)

    synonyms = {
        "informations": "information",
        "details": "detail",
        "clubs": "club",
        "placements": "placement",
        "fees": "fee",
        "hostels": "hostel",
        "sports facilities": "sports",
        "library facilities": "library",
        "medical facilities": "medical",
        "all": "all",
        "complete": "all",
        "list": "all",
    }

    for k, v in synonyms.items():
        text = text.replace(k, v)

    return text.strip()


def load_all_chunks():
    all_chunks = []

    for file in CHUNK_DIR.glob("*_chunks.json"):
        try:
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    all_chunks.extend(data)
        except Exception as e:
            print(f"Failed to load {file.name}: {e}")

    return all_chunks


def is_all_intent(query: str) -> bool:
    return any(w in query for w in ["all", "complete", "full", "list"])


def keyword_overlap_score(query_words, text):
    return sum(1 for w in query_words if w in text)



def retrieve_chunks(query: str, top_k: int = 3):
    query = normalize(query)
    query_words = query.split()
    chunks = load_all_chunks()

    scored_chunks = []

    for chunk in chunks:
        searchable = normalize(
            chunk.get("question", "") + " " +
            chunk.get("answer", "") + " " +
            " ".join(chunk.get("keywords", []))
        )

        score = keyword_overlap_score(query_words, searchable)

        if any(w in searchable for w in query_words):
            score += 2

        if score > 0:
            scored_chunks.append((score, chunk))

    scored_chunks.sort(key=lambda x: x[0], reverse=True)

    if not scored_chunks:
        return []

    if is_all_intent(query):
        seen = set()
        unique_chunks = []
        for _, chunk in scored_chunks:
            cid = chunk.get("id")
            if cid not in seen:
                seen.add(cid)
                unique_chunks.append(chunk)
        return unique_chunks

    return [chunk for _, chunk in scored_chunks[:top_k]]
