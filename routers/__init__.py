from fastapi import APIRouter
from . import mentor_chat, mentor_essay_evaluasi, mentor_pilgan_evaluasi

api_router = APIRouter(prefix="/mentor_api")
api_router.include_router(mentor_chat.router)
api_router.include_router(mentor_pilgan_evaluasi.router)
api_router.include_router(mentor_essay_evaluasi.router)