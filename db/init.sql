-- Schema aligned with ATA.models.Student, Team, Course
-- Drop existing tables (optional, uncomment if needed)
-- DROP TABLE IF EXISTS students CASCADE;
-- DROP TABLE IF EXISTS teams CASCADE;
-- DROP TABLE IF EXISTS course CASCADE;

CREATE TABLE courses (
    id SERIAL PRIMARY KEY,
    semester SMALLINT NOT NULL,
    course_code TEXT NOT NULL,
    team_size INTEGER NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE teams (
    id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES courses(id) ON DELETE SET NULL,
    name TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    team_id INTEGER REFERENCES teams(id) ON DELETE SET NULL,
    course_id INTEGER REFERENCES courses(id) ON DELETE SET NULL,
    student_ip TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    first_name TEXT NOT NULL,
    skill_level SMALLINT,            -- index into CONFIG["skill_level"]["choices"]
    ambition SMALLINT,               -- may be NULL for no preference
    role SMALLINT,                   -- may be NULL for no preference
    teamwork_style SMALLINT,         -- may be NULL for no preference
    pace SMALLINT,                   -- may be NULL for no preference
    backgrounds INTEGER[] DEFAULT '{}',          -- set of indices
    backgrounds_preference SMALLINT,             -- 0 = same, 1 = different, NULL = no pref
    hobbies INTEGER[] DEFAULT '{}',              -- set of indices
    project_summary TEXT,
    other_prompts TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes to speed up lookups
CREATE INDEX IF NOT EXISTS idx_students_course ON students(course_id);
CREATE INDEX IF NOT EXISTS idx_students_team ON students(team_id);
CREATE INDEX IF NOT EXISTS idx_teams_course ON teams(course_id);
