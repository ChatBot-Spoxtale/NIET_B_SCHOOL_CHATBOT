import json
from pathlib import Path
from typing import List, Dict


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_DIR / "data" / "contact_data.json"
OUTPUT_PATH = BASE_DIR / "data_chunk" / "contact_chunks.json"


def chunk_contact_page(data: dict):
    """
    Convert Contact page JSON into RAG chunks
    Format: id, question, answer, keywords
    """

    chunks = []

    contact = data.get("get_in_touch", {})

    # ---------- Main Campus Address ----------
    main_campus = contact.get("main_campus", {})
    if main_campus:
        address = " ".join(main_campus.get("address", []))

        chunks.append({
            "id": "contact_0",
            "question": "What is the main campus address of NIET Business School?",
            "answer": address,
            "keywords": [
                "main campus",
                "address",
                "niet business school",
                "greater noida",
                "uttar pradesh"
            ]
        })

    # ---------- Remote Admission Office ----------
    remote_office = contact.get("remote_admission_office", {})
    if remote_office:
        address = " ".join(remote_office.get("address", []))

        chunks.append({
            "id": "contact_1",
            "question": "Where is the remote admission office of NIET Business School located?",
            "answer": address,
            "keywords": [
                "remote admission office",
                "admission office",
                "kolkata",
                "west bengal",
                "niet business school"
            ]
        })

    # ---------- Admission Helpline ----------
    helplines = contact.get("admission_helpline", [])
    if helplines:
        unique_numbers = list(dict.fromkeys(helplines))  # remove duplicates
        chunks.append({
            "id": "contact_2",
            "question": "What are the admission helpline numbers of NIET Business School?",
            "answer": ", ".join(unique_numbers),
            "keywords": [
                "admission helpline",
                "contact number",
                "phone",
                "admission support",
                "niet business school"
            ]
        })

    # ---------- Admission Email ----------
    email = contact.get("email")
    if email:
        chunks.append({
            "id": "contact_3",
            "question": "What is the admission email address of NIET Business School?",
            "answer": email,
            "keywords": [
                "admission email",
                "contact email",
                "email address",
                "niet business school"
            ]
        })

    return chunks

def save_chunks():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    chunks = chunk_contact_page(data)

    OUTPUT_PATH.parent.mkdir(exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)

    print(f"Program chunks saved ({len(chunks)})")

if __name__ == "__main__":
    save_chunks() 