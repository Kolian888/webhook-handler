import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# URL для перенаправления запросов (например, сервер Леночки)
LENOCHKA_API_URL = "https://your-api-url.com/process_request"

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

        # Перенаправляем запрос ко мне через API
        payload = {"command": user_command, "user_id": request_data["session"]["user_id"]}
        response_from_me = requests.post(LENOCHKA_API_URL, json=payload)
        response_from_me.raise_for_status()  # Проверяем успешность запроса

        # Получаем обработанный ответ от API
        response_text = response_from_me.json().get("response", "Извините, я пока не могу ответить на этот запрос.")

        # Формируем ответ для Алисы
        response = {
            "version": "1.0",
            "session": request_data["session"],
            "response": {
                "text": response_text,
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
