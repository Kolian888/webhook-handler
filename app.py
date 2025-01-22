from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
    try:
        # Логируем запрос для отладки
        request_data = request.json
        print(f"Получен запрос: {request_data}")

        # Проверяем, что ключи "session" и "request" есть в данных
        if "session" not in request_data or "request" not in request_data:
            raise KeyError("Отсутствуют обязательные ключи 'session' или 'request'")

        # Получаем команду пользователя
        user_command = request_data["request"].get("command", "").lower()

        # Формируем ответ в зависимости от команды
        if "привет" in user_command:
            response_text = "Привет! Как я могу помочь?"
        elif "пока" in user_command:
            response_text = "До свидания! Хорошего дня!"
        else:
            response_text = "Извините, я не понял вашу команду."

        # Ответ для Алисы
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
        # Обрабатываем ошибку и возвращаем сообщение для отладки
        print(f"Ошибка: {e}")
        return jsonify({"error": "internal_error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
