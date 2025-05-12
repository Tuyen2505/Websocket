import asyncio
import websockets
import json
import base64

async def send_image(websocket):
    with open("D:/image/result/result.png", "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode("utf-8")

    response = {
        "status": "success",
        "image": img_base64
    }
    print(f"📤 Đang gửi ảnh, dung lượng: {len(img_base64)} bytes")
    
    await websocket.send(json.dumps(response))

async def server(websocket):
    async for message in websocket:
        print("📩 Nhận dữ liệu từ client:", message)
        await send_image(websocket)

async def main():
    async with websockets.serve(server, "localhost", 8765):
        print("✅ WebSocket server đang chạy trên ws://localhost:8765")
        await asyncio.Future()  # Chạy vô hạn

# Chạy server với asyncio.run()
if __name__ == "__main__":
    asyncio.run(main())
