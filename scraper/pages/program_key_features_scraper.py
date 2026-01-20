from pathlib import Path
import requests
import hashlib
import json
import re
import os
from bs4 import BeautifulSoup
from datetime import datetime

URL = "https://www.nietbschool.ac.in/program#features"

BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "program_key_features.json"

def normalize(text):
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def sha256_hash(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def extract_key_features(soup):
    section = soup.find("section", id="features")
    if not section:
        return []

    features = []

    cards = section.find_all("div", class_="bg-white")

    for card in cards:
        title_tag = card.find("h3")
        desc_tag = card.find("p")

        if not title_tag or not desc_tag:
            continue

        title = title_tag.get_text(strip=True)
        description = desc_tag.get_text(strip=True)

        if title and description:
            features.append({
                "title": title,
                "description": description
            })

    return features

# MAIN SCRAPER 
def scrape_key_features():
    response = requests.get(URL, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "nav", "footer"]):
        tag.decompose()

    key_features = extract_key_features(soup)

    combined_text = normalize(
        " ".join(f["title"] + " " + f["description"] for f in key_features)
    )

    content_hash = sha256_hash(combined_text)

    result = {
        "page_type": "program_key_features",
        "source_url": URL,
        "last_scraped": datetime.utcnow().isoformat(),
        "content_hash": content_hash,
        "data": {
            "key_features": key_features
        }
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

    print("Key Features scraped → program_key_features.json")

if __name__ == "__main__":
    scrape_key_features()
