import httpx
from fastapi import HTTPException
from core.config import settings
from .system_prompts import (
    system_prompt_materi,
    system_prompt_pilgan,
    system_prompt_essay,
)

STOP_TOKENS = ["user", "\nuser", "<|im_end|>", "User:"]

class MentorService():
    def __init__(self):
        self.url = settings.MENTOR_LLM_ENDPOINT
        self.model = settings.MENTOR_LLM_MODEL

    async def _call_llm(self, system_prompt: str, chat_messages: list) -> dict:
        """
        Internal method untuk call LLM endpoint.
        Gaperlu diubah kecuali ada perubahan pada LLM API contract.
        """
        messages = [
            {"role": "system", "content": system_prompt},
            *chat_messages
        ]
        body = {
            "model": self.model,
            "temperature": 0.7,
            "messages": messages,
            "max_tokens": 0,
            "stop": STOP_TOKENS,
            "frequency_penalty": 1.2,
            "presence_penalty": 1.2,
        }
        try:
            async with httpx.AsyncClient(timeout=60) as client:
                response = await client.post(self.url, json=body)
                response.raise_for_status()
                result = response.json()
        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail="Mentor Tim 5 timeout")
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=502, detail=f"LLM endpoint error: {e.response.status_code}")
        except httpx.RequestError:
            raise HTTPException(status_code=502, detail="Tidak bisa reach LLM endpoint")

        return {
            **result,
            "reply": result["choices"][0]["message"]["content"],
            "provider": "sr5",
            "model": self.model,
        }

    """
    Handler untuk endpoint POST /mentor_api/*.

    Tim 5:
    1. Buat function system_prompt_chat(payload) di file terpisah (misalnya system_prompts/prompts_apalah.py)
    2. Function itu terima payload dict dan return string system prompt
    3. Ganti string kosong di bawah dengan pemanggilan function tersebut

    Contoh:
        system_prompt = system_prompt_chat(payload)

    payload berisi konteks siswa: siswa_id, sesi_id, materi, atp, level,
    message terakhir siswa, context (emosi, bacaan, dll).
    Gunakan field-field ini untuk menyusun system prompt yang relevan.
    atau gunakan payload untuk konteks soal, jawaban siswa, dan level kesulitan.
    """

    async def chat_response(self, chat_messages: list, payload: dict):
        system_prompt = system_prompt_materi(payload)
        return await self._call_llm(system_prompt, chat_messages)

    async def pilgan_evaluation(self, chat_messages: list, payload: dict):
        system_prompt = system_prompt_pilgan(payload)
        return await self._call_llm(system_prompt, chat_messages)

    async def essay_evaluation(self, chat_messages: list, payload: dict):
        system_prompt = system_prompt_essay(payload)
        return await self._call_llm(system_prompt, chat_messages)