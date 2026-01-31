from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional, Union

from llm_model.chat import chat

from router.callback_router import router as callback_router
from constant.is_sensitive import is_sensitive_query
from constant.sensitive_redirect import SENSITIVE_REDIRECT_RESPONSE
from constant.is_sensitive import is_safety_confirmation_query
from constant.sensitive_redirect import POSITIVE_SENSITIVE_RESPONSE

app = FastAPI(title="NIET Course RAG Bot API")

app.include_router(callback_router, prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str
class Action(BaseModel):
    type: str
    label: str
    url: Optional[str] = None
class SensitiveRedirectResponse(BaseModel):
    type: str = "sensitive_redirect"
    text: str
    actions: List[Action]

class PositiveSensitiveResponse(BaseModel):
    type: str = "positive_sensitive"
    text: str
    details: List[str]
    actions: List[Action]
    
class NormalChatResponse(BaseModel):
    type: str = "normal"
    answer: str



@app.post(
    "/chat",
    response_model=Union[
        NormalChatResponse,
        SensitiveRedirectResponse,
        PositiveSensitiveResponse
    ]
)
def chat_endpoint(payload: ChatRequest):

    question = payload.question.lower()

    try:
        if is_sensitive_query(payload.question):
            if is_safety_confirmation_query(payload.question):
                return POSITIVE_SENSITIVE_RESPONSE
            return SENSITIVE_REDIRECT_RESPONSE

        answer = chat(question)
        return {
            "type": "normal",
            "answer": answer
        }

    except Exception as e:
        print("Chat error:", e)
        return {
            "type": "normal",
            "answer": (
                "Our system is currently experiencing high traffic. "
                "Please try again in a few minutes or visit our website: "
                "https://www.nietbschool.ac.in/"
            )
        }

@app.get("/")
def root():
    return {"status": "RAG API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8060, reload=True)
