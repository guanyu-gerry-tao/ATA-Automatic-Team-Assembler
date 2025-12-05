import pickle
from typing import Annotated

from fastapi import FastAPI, Request, Form

from ATA import pickle_ops
from starlette.middleware.cors import CORSMiddleware
from .models import Student, Course
import json

# FastAPI application instance
app = FastAPI()

# Configure CORS to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    """Root endpoint for health check and API identification.
    
    Returns:
        API name string.
    """
    print("someone visited!")
    return "ATA-Automatic Team Assembler"


@app.post("/student_submit")
async def student_submit(data: Annotated[str, Form()], request: Request):
    """Submit or update student information.
    
    Accepts student data as JSON string in form data. If a student with the same
    email exists, their information is updated. Otherwise, a new student is added.
    
    Args:
        data: JSON string containing student information.
        request: FastAPI request object.
        
    Returns:
        Dictionary with status "ok" on success.
    """
    # Load existing course, or create new one if file doesn't exist
    try:
        course = pickle_ops.load_data()
        if not isinstance(course, Course):
            raise Exception("Loaded data is not a Course instance")
    except Exception:
        course = Course([])
        pickle_ops.save_data(course)
    
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
    )
    # Update existing student or add new one
    course.update_student(student)
    pickle_ops.save_data(course)
    return {"status": "ok"}


@app.get("/check_status")
def check_status(email: str, request: Request):
    """Check if a student has been assigned to a team.
    
    Args:
        email: Student's email address.
        request: FastAPI request object.
        
    Returns:
        Dictionary with status and has_result boolean indicating if student has a team.
    """
    try:
        course = pickle_ops.load_data()
        if not isinstance(course, Course):
            raise Exception("Loaded data is not a Course instance")
    except Exception:
        return {'status': 'error', 'has_result': False, 'message': 'Student not found'}
    
    try:
        student = course.get_student_by_email(email)
        has_result = student.team_id is not None and student.team_id != ""
        return {'status': 'ok', 'has_result': bool(has_result)}
    except ValueError:
        return {'status': 'error', 'has_result': False, 'message': 'Student not found'}


@app.get("/result")
def result(email: str, request: Request):
    """Get team matching results for a student.
    
    Args:
        email: Student's email address.
        request: FastAPI request object.
        
    Returns:
        Dictionary containing team information including teammate names, emails,
        project summaries, and AI suggestions.
    """
    course = pickle_ops.load_data()
    student = course.get_student_by_email(email)
    team_id = student.team_id
    team = course.get_team_by_team_id(team_id)
    teammates_name = [teammate.first_name for teammate in team.students]
    teammates_email = [teammate.email for teammate in team.students]
    teammates_proj_summary = [teammate.project_summary for teammate in team.students]
    ai_suggestion = getattr(team, 'AI_suggestion', None) or ""
    pickle_ops.save_data(course)
    return {
        'status': 'ok',
        'teammates_name': teammates_name,
        'teammates_email': teammates_email,
        'teammates_proj_summary': teammates_proj_summary,
        'ai_suggestion': ai_suggestion
    }


@app.get("/health")
def health():
    """Health check endpoint for monitoring and load balancers.
    
    Returns:
        Dictionary with status "ok".
    """
    return {"status": "ok"}