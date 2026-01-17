import requests
import hashlib
import json
import re
import os
from bs4 import BeautifulSoup
from datetime import datetime

URL = "https://www.nietbschool.ac.in/about"
OUTPUT_FILE = "../output/about_page.json"

os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def sha256_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def extract_overview(soup: BeautifulSoup) -> str:

    overview_section = soup.find("section", id="overview")
    if not overview_section:
        return ""

    paragraphs = overview_section.find_all("p")

    overview_text = [
        p.get_text(strip=True)
        for p in paragraphs
        if p.get_text(strip=True)
    ]

    return " ".join(overview_text)

# MAIN SCRAPER
def scrape_about_page():
    response = requests.get(URL, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "nav", "footer"]):
        tag.decompose()

    college_overview = extract_overview(soup)

    content_hash = sha256_hash(normalize(college_overview))

    result = {
        "page_type": "about_page",
        "source_url": URL,
        "last_scraped": datetime.utcnow().isoformat(),
        "content_hash": content_hash,
        "data": {
            "college_overview": college_overview
        }
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

    print("About page (overview only) scraped successfully → about_page.json")

if __name__ == "__main__":
    scrape_about_page()
