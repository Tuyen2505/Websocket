from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Biến toàn cục để lưu tin nhắn mới nhất
latest_text = None  
ALLOWED_USERS = {5982446232}
TELEGRAM_BOT_TOKEN = "7962908225:AAGnoPTdw6dIuPt6C1uiSG0cIU-EoalM768"  # Thay thế bằng token thực tế

def send_message(chat_id, text):
    """Gửi tin nhắn phản hồi đến người dùng Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(url, json=payload)

@app.route("/telegram-webhook", methods=["POST"])
def telegram_webhook():
    global latest_text  # Khai báo biến toàn cục
    data = request.get_json()
    print(f"📩 Nhận tin nhắn từ Telegram: {data}")

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        latest_text = data["message"]["text"]  # Lưu tin nhắn vào biến toàn cục
        print(f"💬 Tin nhắn nhận được: {latest_text}")

        # Gửi phản hồi đến người dùng
        response_text = f"Bạn vừa nhắn: {latest_text}"
        send_message(chat_id, response_text)

    return jsonify({"status": "ok"}), 200

@app.route("/get-latest-message", methods=["GET"])
def get_latest_message():
    """API để lấy tin nhắn mới nhất"""
    return jsonify({"latest_text": latest_text}), 200

if __name__ == "__main__":
    app.run(port=6868)
