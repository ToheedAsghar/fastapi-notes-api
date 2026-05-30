import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
from notes.storage import get_no_of_notes
from users.models import User # noqa: F401 — needed so Base sees the User model 
from notes.models import Note # noqa: F401 — needed so Base sees the Note model
from notes.router import router as notes_router
from users.router import router as users_router

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Notes API")

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start
    response.headers["X-Process-Time"] = f"{duration:.4f}"
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(notes_router)
app.include_router(users_router)

@app.get("/")
def root():
    return {"message": "Notes API"}

@app.get("/health")
def get_health():
    return {"status": "ok"}
