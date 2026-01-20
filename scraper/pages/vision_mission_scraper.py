from pathlib import Path
import requests
import hashlib
import json
import re
import os
from bs4 import BeautifulSoup
from datetime import datetime

URL = "https://www.nietbschool.ac.in/vision-mission"

BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "vision_mission_page.json"
def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def sha256_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def extract_vision_and_mission(soup: BeautifulSoup):
    vision_text = ""
    mission_list = []
    vision_heading = soup.find(
        "h3",
        string=lambda s: s and s.strip().lower() == "vision"
    )

    if vision_heading:
        vision_card = vision_heading
        for _ in range(5):  
            vision_card = vision_card.parent
            if vision_card.name == "div":
                p = vision_card.find("p")
                if p:
                    vision_text = p.get_text(strip=True)
                    break

    mission_heading = soup.find(
        "h3",
        string=lambda s: s and s.strip().lower() == "mission"
    )

    if mission_heading:
        mission_card = mission_heading
        for _ in range(5):
            mission_card = mission_card.parent
            if mission_card.name == "div":
                paragraphs = mission_card.find_all("p")
                if paragraphs:
                    for p in paragraphs:
                        text = p.get_text(strip=True)
                        if text:
                            mission_list.append(text)
                    break

    return vision_text, mission_list

# MAIN SCRAPER
def scrape_vision_mission_page():
    response = requests.get(URL, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    for tag in soup(["script", "style", "nav", "footer"]):
        tag.decompose()

    vision, mission = extract_vision_and_mission(soup)

    combined_text = normalize(vision + " ".join(mission))
    content_hash = sha256_hash(combined_text)

    result = {
        "page_type": "vision_mission_page",
        "source_url": URL,
        "last_scraped": datetime.utcnow().isoformat(),
        "content_hash": content_hash,
        "data": {
            "vision": vision,
            "mission": mission
        }
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

    print("Vision & Mission page scraped successfully → vision_mission_page.json")

if __name__ == "__main__":
    scrape_vision_mission_page()
