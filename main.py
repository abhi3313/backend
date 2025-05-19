import re
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pdfminer.high_level import extract_text
import tempfile

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def load_skills_from_file(filename="skill.txt"):
    with open(filename, "r") as f:
        skills = {line.strip() for line in f.readlines() if line.strip()}
    return skills

SKILL_KEYWORDS = load_skills_from_file()

@app.post("/upload/")
async def upload_resume(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    text = extract_text(tmp_path)

    pattern = r'\b(' + '|'.join(re.escape(skill) for skill in SKILL_KEYWORDS) + r')\b'

    found_skills = set(re.findall(pattern, text, re.IGNORECASE))

    return {"skills": list(found_skills)}
