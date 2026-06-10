import os
import httpx
from fastapi import HTTPException
class MentorService():
    def __init__(self):
        self.url = os.getenv("MENTOR_LLM_ENDPOINT")
        self.model = os.getenv("MENTOR_LLM_MODEL")

    async def chat_response(self, chat_messages: list, payload: dict):
        system_prompt = ''
        # implemen function buat bikin sistem prompt chat response terserah kalian
        # CONTOH: system_prompt_chat(payload)

        messages = [
            {"role": "system", "content": system_prompt},
            *chat_messages
        ]

        body = {
            "model": self.model,
            "temperature": 0.7, # Ganti dulu ya
            "messages": messages,
            "max_tokens": 0 # Ganti dulu ya
        }

        try:
            async with httpx.AsyncClient(timeout=60) as client:
                response = await client.post(self.url, json=body)
                response.raise_for_status()
                result = response.json()
        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail="Mentor Tim 5 timeout")

        reply = result.get("content")

        return {
            **result,
            "reply": reply,
            "provider": "sr5",
            "model": self.model,
        }