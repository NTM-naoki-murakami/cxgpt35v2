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

    # OpenAIのAPIを使用してChatGPTに問い合わせ（新しいAPIメソッドを使用）
    response = await openai.ChatCompletion.create(
        model="gpt-4",  # モデルの指定（gpt-4や他のモデル）
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": query},
        ]
    )

    # OpenAIの応答をDialogflow CXに返す
    return JSONResponse({
        "fulfillment_response": {
            "messages": [{
                "text": {
                    "text": [response.choices[0].message['content']]
                }
            }]
        }
    })

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
