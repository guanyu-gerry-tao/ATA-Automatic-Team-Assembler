from typing import Annotated

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from pathlib import Path

from .models import Student

import json

app = FastAPI()

phase = 0
prof_ip = None

@app.post("/phase")
def set_phase(set_phase: int):
    global phase
    phase = set_phase
    return {"status": "ok"}

@app.get("/prof_login", response_class=HTMLResponse)
def prof_login(request: Request):
    global prof_ip
    if not prof_ip:
        prof_ip = request.client.host
    if request.client.host == prof_ip:
        dashboard = Path("../FE_dashboard/index.html").read_text(encoding="utf-8")
        return dashboard
    else:
        return "The professor has already logged in."

@app.get("/")
def read_root():
    print("someone visited!")
    return {"Hello": "World"}

@app.post("/student_phase0")
async def student_phase0(data: Annotated[Student, Form()]):
    pass


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

@app.get("/health")
def health():
    return {"status": "ok"}