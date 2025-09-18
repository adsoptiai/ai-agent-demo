from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os

# 請先在環境變數設置 OPENAI_API_KEY
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI(title="AI Agent Demo")

class Question(BaseModel):
    question: str

@app.post("/ask")
async def ask_agent(q: Question):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": q.question}],
            max_tokens=200
        )
        answer = response["choices"][0]["message"]["content"]
        return {"question": q.question, "answer": answer}
    except Exception as e:
        return {"error": str(e)}
