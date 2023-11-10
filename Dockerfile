# 基本イメージとしてPythonの公式イメージを使用
FROM python:3.9

# 作業ディレクトリの設定
WORKDIR /app

# 必要なPythonライブラリをインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのコードをコピー
COPY . .

# ポート8080でアプリケーションを実行
EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
