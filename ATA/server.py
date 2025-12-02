import pickle
from typing import Annotated

from fastapi import FastAPI, Request, Form


from ATA import pickle_ops

# for CORS
from starlette.middleware.cors import CORSMiddleware

# load models
from .models import Student

# for load config
import json


# # variable to store professor's IP'
# prof_email = input("Please enter professor's email: ")
# prof_passcode = input("Please create professor's passcode: ")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    print("someone visited!")
    return "ATA-Automatic Team Assembler"


@app.post("/student_submit")
async def student_submit(data: Annotated[str, Form()], request: Request):
    course = pickle_ops.load_data()
    student_data = json.loads(data)
    student = Student(
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
        other_prompts=student_data["other_prompts"],
    )
    course.add_students([student])
    pickle_ops.save_data(course)
    return {"status": "ok"}


# @app.post("/proceed")
# def proceed(email: str, passcode: str, max_size, request: Request):
#     pass  # TODO: after having student's data, use this api to start proceed team matching algorithm
#     # TODO: make sure it's professor's IP first
#     # TODO: then proceed, and IO out the result to memory
#     if request.client.host != prof_ip:
#         return "Only professor can proceed"
#     course.team_matching(max_size=max_size)
#     return {"status": "ok"}


@app.get("/result")
def result(email: str, request: Request):
    course = pickle_ops.load_data()
    student = course.get_student_by_email(email)
    team_id = student.team_id
    team = course.get_team_by_team_id(team_id)
    teammates_name = [teammate.first_name for teammate in team.students]
    teammates_proj_summary = [teammate.project_summary for teammate in team.students]
    pickle_ops.save_data(course)
    return {'status': 'ok', 'teammates_name': teammates_name, 'teammates_proj_summary': teammates_proj_summary}


# @app.post("/reset")
# def reset(email: str, passcode: str, request: Request):
#     if email == prof_email and passcode == prof_passcode:
#         global course
#         course = Course()
#         return "Data has been reset. If you want to clear professor's email and passcode, please restart the server."
#     else:
#         return "Only professor can reset the data"


@app.get("/health")
def health():
    return {"status": "ok"}