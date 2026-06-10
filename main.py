from fastapi import FastAPI
from routers import mentor_chat, mentor_essay_evaluasi, mentor_pilgan_evaluasi

app = FastAPI()

app.include_router(mentor_chat.router)
app.include_router(mentor_pilgan_evaluasi.router)
app.include_router(mentor_essay_evaluasi.router)

@app.get("/")
def root():
    return {"message": "Backend Tim 5"}