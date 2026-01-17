import requests
import hashlib
import json
import re
import os
from bs4 import BeautifulSoup
from datetime import datetime

URL = "https://www.nietbschool.ac.in/peos"
OUTPUT_FILE = "../output/peos_page.json"

os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def sha256_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def extract_peos(soup: BeautifulSoup):
    peos = []

    peos_section = soup.find("section", id="peos")
    if not peos_section:
        return peos

    cards = peos_section.find_all("div", class_=lambda c: c and "rounded-2xl" in c)

    for card in cards:
        code_span = card.find("span", string=lambda s: s and s.strip().startswith("PEO"))
        code = code_span.get_text(strip=True) if code_span else ""

        p = card.find("p")
        if not p:
            continue

        text = p.get_text(" ", strip=True)

        text = re.sub(r"^PEO\d+:\s*", "", text)

        if code and text:
            peos.append({
                "code": code,
                "description": text
            })

    return peos

# MAIN SCRAPER
def scrape_peos_page():
    response = requests.get(URL, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "nav", "footer"]):
        tag.decompose()

    peos = extract_peos(soup)

    combined_text = normalize(" ".join(p["description"] for p in peos))
    content_hash = sha256_hash(combined_text)

    result = {
        "page_type": "program_educational_objectives",
        "source_url": URL,
        "last_scraped": datetime.utcnow().isoformat(),
        "content_hash": content_hash,
        "data": {
            "peos": peos
        }
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

    print("PEOs page scraped successfully → peos_page.json")

if __name__ == "__main__":
    scrape_peos_page()
