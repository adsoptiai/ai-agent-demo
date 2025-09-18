# AI Agent Demo

這是一個使用 FastAPI + OpenAI API 的小型 AI Agent 範例。
- 提供一個 `/ask` API，輸入問題即可得到回答。
- 部署於 Google Cloud Run。
- 使用 GitHub Actions 自動化 CI/CD。

## 🔧 如何本地運行
```bash
pip install -r requirements.txt
export OPENAI_API_KEY=你的API金鑰
uvicorn app:app --reload
