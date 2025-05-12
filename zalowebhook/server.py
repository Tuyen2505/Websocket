import json
from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # Cho phép tất cả origin kết nối WebSocket

@app.route("/")
def index():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="zalo-platform-site-verification" content="VO6b5Fh-ApWhmR00eUmcFbRTXmcwgrPGCpKv" />
        <title>WebSocket Zalo OA</title>
    </head>
    <body>
        <h2>WebSocket Client</h2>
        <button onclick="connectWebSocket()">Kết nối WebSocket</button>
        <ul id="messages"></ul>

        <script>
            function connectWebSocket() {
                let socket = io("http://localhost:6868");
                socket.on("message", function(data) {
                    let msgList = document.getElementById("messages");
                    let newItem = document.createElement("li");
                    newItem.textContent = data;
                    msgList.appendChild(newItem);
                });
            }
        </script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.5.4/socket.io.js"></script>
    </body>
    </html>
    """

@app.route("/zalo-webhook", methods=["POST"])
def zalo_webhook():
    """
    Nhận tin nhắn từ Zalo OA và gửi qua WebSocket
    """
    data = request.get_json()
    print(f"Nhận webhook: {json.dumps(data, indent=2)}")

    # Gửi dữ liệu đến tất cả client đang kết nối WebSocket
    socketio.emit("message", json.dumps(data))

    return jsonify({"status": "received"}), 200

@socketio.on("connect")
def handle_connect():
    print("Client WebSocket đã kết nối!")

@socketio.on("disconnect")
def handle_disconnect():
    print("Client WebSocket đã ngắt kết nối!")

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=6868, debug=True)
