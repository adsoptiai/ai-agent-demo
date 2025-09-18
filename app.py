from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import json

app = FastAPI(title="AI Agent Demo", version="1.0.0")

# 添加 CORS 中間件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允許所有來源
    allow_credentials=True,
    allow_methods=["*"],  # 允許所有 HTTP 方法
    allow_headers=["*"],  # 允許所有 Headers
)

class Question(BaseModel):
    question: str

@app.get("/")
async def root():
    return {"message": "AI Agent API is running!", "status": "success"}

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
            return {"question": q.question, "answer": answer, "status": "success"}
            
        except Exception as e:
            return {"error": f"OpenAI API call failed: {str(e)}", "status": "error"}
    
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}", "status": "error"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "AI Agent Demo"}

@app.post("/echo")
async def echo(q: Question):
    return {"question": q.question, "echo": f"You said: {q.question}", "status": "success"}

@app.get("/debug")
async def debug_info():
    """Debug endpoint to check installed packages"""
    try:
        import openai
        import pydantic
        import fastapi
        
        return {
            "status": "success",
            "versions": {
                "openai": openai.__version__,
                "pydantic": pydantic.__version__,
                "fastapi": fastapi.__version__
            },
            "environment": {
                "openai_api_key_configured": bool(os.getenv("OPENAI_API_KEY")),
                "port": os.getenv("PORT", "8080")
            }
        }
    except Exception as e:
        return {"error": f"Debug info failed: {str(e)}", "status": "error"}

# 添加一個測試 CORS 的端點
@app.get("/cors-test")
async def cors_test():
    return {
        "message": "CORS is working!",
        "timestamp": "2025-01-20",
        "status": "success"
    }
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)