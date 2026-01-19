import requests
import json
import hashlib
import re
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path

URL = "https://www.nietbschool.ac.in/student-life"
OUTPUT_FILE = Path("../output/student_life_page.json")


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def generate_hash(data: dict) -> str:
    clean = json.dumps(data, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(clean.encode("utf-8")).hexdigest()


def scrape_student_life():
    response = requests.get(URL, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    for tag in soup(["script", "style", "nav", "footer"]):
        tag.decompose()
    header = soup.find(
        "h2",
        string=lambda x: x and "Student Life at NIET Business School" in x
    )

    title = normalize(header.get_text()) if header else ""

    description_parts = []
    for p in header.find_next_siblings("p", limit=2):
        description_parts.append(normalize(p.get_text()))

    description = " ".join(description_parts)
    facilities = []

    facilities_grid = header.find_next("div", class_="grid")

    if facilities_grid:
        cards = facilities_grid.find_all(
            "div",
            class_=lambda x: x and "rounded-2xl" in x,
            recursive=False
        )

        for card in cards:
            h3 = card.find("h3")
            p = card.find("p")

            if not h3 or not p:
                continue

            facilities.append({
                "title": normalize(h3.get_text()),
                "description": normalize(p.get_text())
            })

    result = {
        "page_type": "student_life_page",
        "source_url": URL,
        "last_scraped": datetime.utcnow().isoformat(),
        "student_life": {
            "title": title,
            "description": description
        },
        "facilities": facilities
    }

    result["content_hash"] = generate_hash(result)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

    print("✅ student_life_page.json scraped correctly (facilities only)")


if __name__ == "__main__":
    scrape_student_life()
