from typing import Annotated

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from pathlib import Path
import os

from .models import Student

import json

app = FastAPI()

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


@app.post("/student_submit")
async def student_submit(course_code: str, number_of_teaming: int, data: Annotated[str, Form()], request: Request):
    # TODO: if student relogin, clear the old data
    student_data = json.loads(data)
    student = Student(
        student_ip=request.client.host,
        first_name=student_data["first_name"],
        email=student_data["email"],
        skill_level=student_data["skill_level"],
        ambition=student_data["ambition"],
        role=student_data["role"],
        teamwork_style=student_data["teamwork_style"],
        pace=student_data["pace"],
        backgrounds=set(student_data["backgrounds"]),
        backgrounds_preference=student_data["backgrounds_preference"],
        hobbies=set(student_data["hobbies"]),
        project_summary=student_data["project_summary"],
        other_prompts=student_data["other_prompts"]
    )
    try:
        with open(f"ATA/student_data/{course_code}_{number_of_teaming}.json", "r") as f:
            data = json.load(f)
            data[student.first_name] = student.get_json()
            with open(f"ATA/student_data/{course_code}_{number_of_teaming}.json", "w") as f:
                json.dump(data, f, indent=4)
    except FileNotFoundError:
        with open(f"ATA/student_data/{course_code}_{number_of_teaming}.json", "w") as f:
            data = {}
            data[student.first_name] = student.get_json()
            json.dump(data, f, indent=4)

    return {"status": "ok"}


@app.post("/proceed")
def proceed():
    pass  # TODO: after having student's data, use this api to start proceed team matching algorism
    # TODO: make sure it's professor's IP first
    # TODO: then proceed, and IO out the result to memory


@app.get("/result")
def result():
    pass
    # TODO: student with their IP can get result


@app.post("/reset")
def reset():
    pass
    # TODO: professor can reset the system, clear all memory for another start


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

@app.get("/health")
def health():
    return {"status": "ok"}