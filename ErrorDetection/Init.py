from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List, Dict
import re
import uvicorn

app = FastAPI(title="API connection")


class TextRequest(BaseModel):
    text: str


class Correction(BaseModel):
    type: str
    original: str
    suggestion: str
    start: int
    end: int

class TextResponse(BaseModel):
    original_text: str
    corrected_text: str
    corrections: List[Correction]


COMMON_MISTAKES = {
    "ввиде": "в виде",
    "зделать": "сделать",
    "придти": "прийти",
    "инжинер": "инженер"
}


def detect_and_correct(text: str) -> Dict:
    corrections = []
    corrected_text = text
    offset = 0  

    for mistake, correction in COMMON_MISTAKES.items():
        for match in re.finditer(rf'\b{mistake}\b', text):
            start = match.start() + offset
            end = match.end() + offset

            corrections.append({
                "type": "spelling",
                "original": mistake,
                "suggestion": correction,
                "start": start,
                "end": end
            })

           
            corrected_text = corrected_text[:start] + correction + corrected_text[end:]
            offset += len(correction) - len(mistake)

    return {
        "original_text": text,
        "corrected_text": corrected_text,
        "corrections": corrections
    }


@app.post("/check", response_model=TextResponse)
async def check_text(request: TextRequest):
    result = detect_and_correct(request.text)
    return result

# === Запуск сервера ===
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)