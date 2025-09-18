from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import os

app = FastAPI(title="AI Agent Demo", version="1.0.0")

# 設定 OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

class Question(BaseModel):
    question: str

@app.get("/")
async def root():
    return {"message": "AI Agent API is running!"}

@app.post("/ask")
async def ask_agent(q: Question):
    try:
        if not openai.api_key:
            return {"error": "OpenAI API key not configured"}
        
        # 使用新版本的 OpenAI API
        from openai import OpenAI
        client = OpenAI(api_key=openai.api_key)
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": q.question}],
            max_tokens=200
        )
        
        answer = response.choices[0].message.content
        return {"question": q.question, "answer": answer}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)