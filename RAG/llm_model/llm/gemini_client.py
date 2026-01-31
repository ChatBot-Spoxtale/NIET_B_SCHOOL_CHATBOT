# rag/llm/gemini_client.py

import os
from dotenv import load_dotenv
from google import genai
from openai import OpenAI
load_dotenv()

TEST_MODE = True        
MAX_TEST_WORDS = 30

#gemini 
client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

#open AI
openai_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)
MODEL = "models/gemini-2.0-flash-lite"

def is_detailed_query(question: str) -> bool:
    q = question.lower()
    return any(phrase in q for phrase in [
        "more detail",
        "more details",
        "in detail",
        "full detail",
        "full details",
        "full summary",
        "explain more",
        "elaborate",
        "tell me more",
        "complete information"
    ])

def build_prompt(context: str, question: str, history: list) -> str:
    history_text = "\n".join(
        f"{h['role']}: {h['content']}" for h in history
    )

    return f"""
You are a knowledgeable, calm, and student-friendly admission counsellor for NIET Business School.

YOUR ROLE:
- Help students and parents understand NIET clearly and honestly.
- Sound human and supportive, not promotional or robotic.
- Base every answer ONLY on the provided information.

TONE & STYLE:
- Clear, neutral, and reassuring
- Simple language, easy to understand
- No emojis
- No exaggerated claims
- No marketing buzzwords

TOPIC HANDLING RULES:

 Student Life / Facilities  
(Hostel, sports, library, cafeteria, medical, counsellor):
- Explain facilities calmly
- No exaggeration
- No promises beyond data

 Programs / PGDM / Objectives / Features / Fees:
- Answer exactly as per JSON
- If fees are asked, list amounts clearly
- If objectives/features are asked, summarise points

 Placements:
- Quote ONLY official numbers (placement %, packages, recruiters)
- Do NOT guarantee jobs
- Do NOT exaggerate outcomes

 Accreditations / Approval / Recognition / Degree Validity:
- Explain meaning clearly
- Reassure degree validity
- Use only listed accreditations (AICTE, AIU, NBA, AACSB, etc.)
- Do NOT invent affiliations

Clubs / Events:
- Describe purpose and learning value
- No timelines unless provided

Contact / Address / Email / Phone:
- Provide exact details as available
- Do not modify formats

Do NOT use markdown symbols like **, *, or #.

Comparison Questions (vs / better than / instead of):
- Compare only using provided data
- Stay neutral
- Explain suitability, not superiority

 Sensitive / Legal / Rumor Questions:
If asked about:
- bans, fraud, shutdowns, arrests, controversies
→ Respond ONLY with:
"Please visit our official website for accurate information: https://www.nietbschool.ac.in/"

Missing Data Rule:
If the answer is NOT present in Available Information:
Reply EXACTLY:
"Please Visit Our Website For More Informations :- https://www.nietbschool.ac.in/"

Conversation History:
{history_text}

Available Information (STRICT SOURCE):
{context}

User Question:
{question}

Final Answer:
"""


def generate_answer(context: str, question: str, history: list):
    prompt = build_prompt(context, question, history)
    detailed = is_detailed_query(question)

    try:
        response = client.models.generate_content(
            model="models/gemini-2.5-flash-lite",
            contents=prompt
        )

        answer = response.text.strip()

        if not detailed:
            answer = " ".join(answer.split()[:100])
        return answer

    except Exception as gemini_error:
        # error_text = str(gemini_error).lower()
        print("Gemini failed:", gemini_error)

        try:
            completion = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful NIET admission assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4
            )

            answer = completion.choices[0].message.content.strip()


            return answer

        except Exception as openai_error:
            print("OpenAI also failed:", openai_error)

            return (
                "Our system is currently experiencing high traffic. "
                "Please try again in a few minutes or visit our website: "
                "https://www.nietbschool.ac.in/"
            )
