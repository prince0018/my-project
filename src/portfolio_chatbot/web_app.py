from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from portfolio_chatbot.chatbot import ChatTurn, PortfolioChatbot
from portfolio_chatbot.chroma_index import describe_chroma_collection
from portfolio_chatbot.config import PROJECT_ROOT


FRONTEND_PATH = PROJECT_ROOT / "frontend"

app = FastAPI(title="Portfolio Chatbot")
app.mount("/assets", StaticFiles(directory=FRONTEND_PATH / "assets"), name="assets")


class ChatMessage(BaseModel):
    question: str = Field(min_length=1)
    answer: str = Field(min_length=1)


class ChatRequest(BaseModel):
    question: str = Field(min_length=1)
    history: list[ChatMessage] = Field(default_factory=list)


class ChatResponse(BaseModel):
    answer: str
    sources: list[str]


@app.get("/")
def index() -> FileResponse:
    return FileResponse(FRONTEND_PATH / "index.html")


@app.get("/api/status")
def status() -> dict[str, str | int]:
    return describe_chroma_collection()


@app.post("/api/chat")
def chat(request: ChatRequest) -> ChatResponse:
    chatbot = PortfolioChatbot()
    history = [ChatTurn(question=item.question, answer=item.answer) for item in request.history]

    try:
        response = chatbot.ask(request.question, history=history)
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    return ChatResponse(answer=response.answer, sources=response.sources)
