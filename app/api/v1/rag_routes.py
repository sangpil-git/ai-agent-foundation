# app/api/v1/rag_routes.py
from fastapi import APIRouter
from pydantic import BaseModel

from app.rag.rag_pipeline import simple_rag_answer

router = APIRouter(prefix="/rag", tags=["rag"])


class RagQuery(BaseModel):
    question: str


@router.post("/query")
def rag_query(body: RagQuery):
    answer = simple_rag_answer(body.question)
    return {"question": body.question, "answer": answer}
