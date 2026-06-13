from fastapi import APIRouter
from src.mentor_service import MentorService
from schema.mentor_schema import MentorRequest

router = APIRouter(prefix="/pilihan_ganda", tags=["Mentor Pilihan Ganda Evaluasi Service"])

@router.post
async def chat(request: MentorRequest):
    return await MentorService().pilgan_evaluation(
        chat_messages=[m.model_dump() for m in request.chat_messages],
        payload=request.payload.model_dump()
    )