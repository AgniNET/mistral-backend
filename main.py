from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import httpx
import os

app = FastAPI()

# 🔐 Store your Mistral API key here
MISTRAL_API_KEY = "w7HMWfLStSFaDftEQALU9fTZG0FBYxHz"

# ✅ Mistral API endpoint (chat completion)
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"

# ⚙️ Default model (you can change based on their docs)
MODEL_NAME = "mistral-small"

@app.post("/ask")
async def ask_mistral(request: Request):
    body = await request.json()
    user_prompt = body.get("prompt")

    if not user_prompt:
        return JSONResponse(status_code=400, content={"error": "Prompt is required"})

    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "user", "content": user_prompt}
        ]
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(MISTRAL_API_URL, headers=headers, json=payload)

        if response.status_code == 200:
            data = response.json()
            answer = data["choices"][0]["message"]["content"]
            return {"answer": answer}
        else:
            return {"error": f"Mistral API error: {response.text}"}

    except Exception as e:
        return {"error": str(e)}
