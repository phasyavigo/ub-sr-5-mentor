from pydantic import BaseModel
from typing import Any


class Context(BaseModel):
    emosi: str
    progress: Any | None
    publish_id: str
    content_bundle_id: str
    bundle_id: str
    bacaan: str

class Payload(BaseModel):
    siswa_id: str
    sesi_id: str
    mapel_id: str
    elemen_id: str
    elemen_label: str
    materi: str
    materi_id: str
    atp: list[str]
    level: str
    message: str
    context: Context
    mentorMode: str

class ChatMessage(BaseModel):
    role: str
    content: str

class MentorRequest(BaseModel):
    chat_messages: list[ChatMessage]
    payload: Payload