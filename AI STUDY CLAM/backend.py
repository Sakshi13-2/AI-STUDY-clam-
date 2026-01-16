from fastapi import FastAPI
from pydantic import BaseModel
import random

app = FastAPI()

class StudentFear(BaseModel):
    subject: str
    total_chapters: int
    days_left: int
    current_mood: int # 1 (Calm) to 10 (Panicked)

@app.post("/generate_plan")
def generate_plan(input_data: StudentFear):
    # Logic: Break chapters into 20-minute "Micro-Tasks"
    # Usually 1 chapter = 4 micro-tasks
    total_micro_tasks = input_data.total_chapters * 4
    tasks_per_day = round(total_micro_tasks / max(input_data.days_left, 1), 1)
    
    # Calculate Readiness Score: Higher when tasks per day are < 5
    readiness = max(10, 100 - (tasks_per_day * 8))
    
    # NLP-style Encouragement messages based on mood
    messages = [
        "You're not behind; you're just at the beginning. Let's start small.",
        "Your brain learns best when it's not stressed. Focus only on the next step.",
        "Forget the exam for a moment. Can you give me just 15 minutes for one task?"
    ]
    
    return {
        "readiness_score": f"{int(readiness)}%",
        "message": random.choice(messages),
        "tasks_per_day": tasks_per_day,
        "micro_goals": [
            f"Read 3 key pages of {input_data.subject}",
            "Write down 5 keywords you remember",
            "Explain one concept out loud to yourself"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)