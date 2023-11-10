from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import openai
import os

app = FastAPI()

# 環境変数からOpenAIのAPIキーを取得
openai.api_key = os.getenv('OPENAI_API_KEY')

@app.post('/webhook')
async def webhook(request: Request):
    # Dialogflow CXからのリクエストを解析
    req = await request.json()
    query = req.get('fulfillmentInfo').get('tag')

    # openaiのクライアントを初期化
    client = openai.OpenAI(api_key=openai.api_key)

    # OpenAIのAPIを使用してChatGPTに問い合わせ
    response = await client.chat.completions.create(
        model="gpt-4",  # モデルの指定
        messages=[{"role": "user", "content": query}]
    )

    # OpenAIの応答をDialogflow CXに返す
    messages = response.choices[0].message.content if response.choices else ""
    return JSONResponse({
        "fulfillment_response": {
            "messages": [{
                "text": {
                    "text": [messages]
                }
            }]
        }
    })

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
