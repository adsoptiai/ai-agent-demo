from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import json

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
        
        # 動態導入 OpenAI 以避免初始化問題
        try:
            from openai import OpenAI
        except ImportError as e:
            return {"error": f"OpenAI import failed: {str(e)}"}
        
        # 建立 OpenAI client
        try:
            client = OpenAI(api_key=openai_api_key)
        except Exception as e:
            return {"error": f"OpenAI client initialization failed: {str(e)}"}
        
        # 呼叫 Chat Completions API
        try:
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": q.question}
                ],
                max_tokens=200,
                temperature=0.7
            )
            
            answer = completion.choices[0].message.content
            return {"question": q.question, "answer": answer}
            
        except Exception as e:
            return {"error": f"OpenAI API call failed: {str(e)}"}
    
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/echo")
async def echo(q: Question):
    return {"question": q.question, "echo": f"You said: {q.question}"}

@app.get("/debug")
async def debug_info():
    """Debug endpoint to check installed packages"""
    try:
        import openai
        import pydantic
        import fastapi
        
        return {
            "openai_version": openai.__version__,
            "pydantic_version": pydantic.__version__,
            "fastapi_version": fastapi.__version__,
            "openai_api_key_configured": bool(os.getenv("OPENAI_API_KEY"))
        }
    except Exception as e:
        return {"error": f"Debug info failed: {str(e)}"}
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)