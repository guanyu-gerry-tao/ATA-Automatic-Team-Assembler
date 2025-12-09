# ATA - Automatic Team Assembler

ATA (Automatic Team Assembler) is an intelligent team formation system based on vector matching algorithms. It automatically forms optimal teams based on students' skills, preferences, and background information.

## 📋 Project Overview

The ATA system converts various student attributes (skill level, ambition, role preferences, teamwork style, work pace, backgrounds, hobbies, etc.) into vector representations and uses a bidirectional matching algorithm (mutual crush score) to find the most suitable team member combinations.

### Key Features

- 🎯 **Intelligent Matching Algorithm**: Bidirectional matching algorithm based on vector similarity
- 👥 **Multi-dimensional Evaluation**: Considers multiple dimensions including skill level, ambition, role, teamwork style, work pace, backgrounds, and hobbies
- 🔄 **Flexible Configuration**: Supports custom team sizes and matching weights
- 💻 **Dual Mode Operation**: Supports both Command Line Interface (CLI) and Web API usage
- 🌐 **Web Frontend**: Provides a user-friendly interface for student information submission and result viewing
- 🐳 **Docker Support**: Containerized deployment, ready to use out of the box

## 🏗️ Project Structure

```
2025-python5001-proj/
├── ATA/                    # Core business logic
│   ├── __init__.py
│   ├── main.py            # CLI main program
│   ├── server.py          # FastAPI web server
│   ├── models.py          # Data models (Student, Team, Course)
│   ├── config.py          # Configuration (attribute options and weights)
│   └── pickle_ops.py      # Data persistence operations
├── FE_Student/            # Frontend interface
│   ├── index.html         # Student information submission page
│   ├── result.html        # Result viewing page
│   └── build.js           # Build script
├── test/                  # Test files
│   ├── test_user.json     # Test data
│   └── test_*.py          # Unit tests
├── data/                  # Data storage directory
│   └── data.pkl          # Serialized course data
├── docker-compose.yml     # Docker Compose configuration
├── Dockerfile             # Docker image build file
├── requirements.txt       # Python dependencies
└── start.sh              # Startup script
```

## 🚀 Quick Start

### Requirements

- Python 3.8+
- Docker and Docker Compose (recommended)
- Node.js (for frontend build, optional)

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Using Docker (Recommended)

1. **Start development environment** (includes API service and CLI console):
   ```bash
   ./start.sh
   ```

2. **Start API service only**:
   ```bash
   docker-compose up -d api
   ```

3. **Run CLI console**:
   ```bash
   docker-compose run --rm console
   ```

### Local Development

1. **Start Web API server**:
   ```bash
   python -m ATA.server
   ```
   The server will start at `http://localhost:8000`

2. **Run CLI console**:
   ```bash
   python -m ATA.main
   ```

## 📖 Usage Guide

### CLI Commands

After starting the CLI, you can use the following commands:

- **S** - Display all current student information
- **T** - Execute team matching (requires team size input)
- **P** - Print team matching results
- **R** - Reset system (delete all students)
- **U** - Clear all team assignments (keep students)
- **D** - Delete a student by email
- **test** - Import test data

### Web API Endpoints

- `GET /` - Health check
- `POST /student_submit` - Submit or update student information
- `GET /check_status?email={email}` - Check if a student has been assigned to a team
- `GET /result?email={email}` - Get team matching results for a student
- `GET /health` - Health check endpoint

### Frontend Usage

1. **Local Development**:
   ```bash
   cd FE_Student
   cp .env_fe .env
   # Edit .env file, set VITE_API_BASE_URL=http://localhost:8000
   node build.js
   # Open index.html in your browser
   ```

2. **Vercel Deployment**:
   - Add environment variable `VITE_API_BASE_URL` in Vercel project settings
   - Code will be automatically built and deployed after commit

## 🔧 Configuration

System configuration is located in `ATA/config.py` and can be customized:

- **Skill Level**: noob, ok, pro
- **Ambition**: just_pass, ambitious
- **Role**: leader, follower
- **Teamwork Style**: online_meeting, offline_meeting, divide_and_conquer
- **Work Pace**: finish_early, finish_late, little_by_little
- **Backgrounds**: Multiple options (Technology/Math, Finance, Consulting, etc.)
- **Hobbies**: Multiple options (Gaming, Outdoor Sports, Travel, etc.)

Each attribute has a corresponding weight used for calculating matching scores.

## 🧮 Matching Algorithm

### Vector Construction

Each student's attributes are converted into two vectors:
- **vector_have**: Represents the student's own attributes
- **vector_want**: Represents the attributes the student wants in teammates

### Matching Strategy

- **Skill Level**: Prefers diversity (wants different skill levels in the team)
- **Ambition**: Prefers matching (wants similar ambition)
- **Role**: Prefers diversity (wants different roles)
- **Teamwork Style**: Prefers matching (wants similar work style)
- **Work Pace**: Prefers matching (wants similar work pace)
- **Backgrounds**: Based on student preference (same or different)
- **Hobbies**: Prefers matching (wants similar hobbies)

### Team Formation Process

1. **Initialization**: Clear all existing team assignments
2. **First Round**: Form team cores (pairs) based on highest mutual crush score
3. **Subsequent Rounds**: Add remaining students to existing teams based on team-student compatibility scores
4. **Completion**: Ensure all students are assigned to teams

## 🧪 Testing

Run tests:

```bash
./run_tests.sh
```

Or run manually:

```bash
python -m pytest test/
```

## 📝 Data Storage

The system stores data in Pickle format in the `data/data.pkl` file. The data includes:
- All student information
- Team assignment results
- Matching score matrices

## 👥 Contributors

- **Guanyu Tao** - [@guanyu-gerry-tao](https://github.com/guanyu-gerry-tao)
- **Yiying Xie** - [@Bestpart-Irene](https://github.com/Bestpart-Irene)

## 🤝 Contributing

Issues and Pull Requests are welcome!

## 📄 License

This project is a course assignment project.

## 📞 Contact

For questions or suggestions, please contact via Issues.

---

**Version**: v1.00
