import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Укажи свой API-ключ OpenAI
OPENAI_API_KEY = "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"
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

@app.route('/', methods=['POST'])
def webhook():
    try:
        # Получаем данные от Алисы
        request_data = request.json
        print(f"Получен запрос: {request_data}")

        # Проверяем структуру запроса
        if not request_data or "session" not in request_data or "request" not in request_data:
            return jsonify({"error": "invalid_request", "message": "Missing keys"}), 400

        # Извлекаем команду пользователя
        user_command = request_data["request"].get("command", "").lower()

        # Отправляем запрос в ChatGPT
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "Ты — помощник Николая."},
                {"role": "user", "content": user_command}
            ]
        }
        gpt_response = requests.post(OPENAI_API_URL, headers=headers, json=payload)
        gpt_response.raise_for_status()

        # Получаем ответ от ChatGPT
        gpt_data = gpt_response.json()
        response_text = gpt_data["choices"][0]["message"]["content"]

        # Формируем ответ для Алисы
        response = {
            "version": "1.0",
            "session": request_data["session"],
            "response": {
                "text": response_text.strip(),
                "end_session": False
            }
        }
        return jsonify(response)

    except Exception as e:
        # Логируем ошибки
        print(f"Ошибка: {e}")
        return jsonify({"error": "internal_error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
