from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os

app = FastAPI(title="AI Agent Demo", version="1.0.0")

class Question(BaseModel):
    question: str

@app.get("/")
async def root():
    return {"message": "AI Agent API is running!"}

@app.post("/ask")
async def ask_agent(q: Question):
    try:
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            return {"error": "OpenAI API key not configured"}
        
        # 使用正確的 OpenAI v1+ API
        from openai import OpenAI
        
        client = OpenAI(api_key=openai_api_key)
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": q.question}],
            max_tokens=200
        )
        
        answer = response.choices[0].message.content
        return {"question": q.question, "answer": answer}
    
    except ImportError:
        return {"error": "OpenAI package not properly installed"}
    except Exception as e:
        return {"error": f"OpenAI API error: {str(e)}"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# 添加一個不需要 OpenAI 的測試端點
@app.post("/echo")
async def echo(q: Question):
    return {"question": q.question, "echo": f"You said: {q.question}"}
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)