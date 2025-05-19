import asyncio
import websockets
import json
import os
import base64
import aiohttp

# Định nghĩa các thư mục lưu trữ
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SAVE_DIR_IMAGE1 = os.path.join(BASE_DIR, "received_images_from_client")
SAVE_DIR_IMAGE2 = os.path.join(BASE_DIR, "person_images_for_comfyui")
SAVE_DIR_RESULT = os.path.join(BASE_DIR, "result_images_from_comfyui")
os.makedirs(SAVE_DIR_IMAGE1, exist_ok=True)
os.makedirs(SAVE_DIR_IMAGE2, exist_ok=True)
os.makedirs(SAVE_DIR_RESULT, exist_ok=True)

# URL đích để gửi yêu cầu HTTP đến ComfyUI
target_url = "http://127.0.0.1:8188/prompt"

# Danh sách các client WebSocket đang kết nối
connected_clients = set()

# Xử lý kết nối từ client React (WebSocket 8765)
async def handle_client(websocket):
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                
                # Lưu ảnh image1 từ dữ liệu base64
                image1_data = base64.b64decode(data["image1"].split(",")[1])
                with open(os.path.join(SAVE_DIR_IMAGE1, "image1.png"), "wb") as f:
                    f.write(image1_data)

                # Lưu ảnh image2 từ dữ liệu base64
                image2_data = base64.b64decode(data["image2"].split(",")[1])
                with open(os.path.join(SAVE_DIR_IMAGE2, "image2.png"), "wb") as f:
                    f.write(image2_data)

                # Gửi phản hồi thành công
                await websocket.send(json.dumps({"status": "success", "message": "Dữ liệu đã được xử lý"}))

                # Gửi yêu cầu đến ComfyUI
                async with aiohttp.ClientSession() as session:
                    async with session.post(target_url, json=data["jsonData"]) as response:
                        response_text = await response.text()
                        print(f"Phản hồi từ ComfyUI: {response_text}")

            except Exception as e:
                print(f"Lỗi xử lý message: {e}")
                await websocket.send(json.dumps({"status": "error", "message": str(e)}))
    except websockets.exceptions.ConnectionClosedOK:
        print("Client đã ngắt kết nối")
    finally:
        connected_clients.remove(websocket)

# Xử lý kết nối từ ComfyUI (WebSocket 8766)
async def handle_comfyui(websocket):
    try:
        while True:
            raw_data = await websocket.recv()
            data = json.loads(raw_data)

            # Lưu ảnh kết quả
            image_data = base64.b64decode(data["image"])
            file_path = os.path.join(SAVE_DIR_RESULT, "result.png")
            with open(file_path, "wb") as f:
                f.write(image_data)
            print(f"✅ Đã lưu ảnh: {file_path}")

            # Gửi ảnh đến các client React
            for client in connected_clients.copy():
                try:
                    await client.send(json.dumps({"image": data["image"], "status": "completed"}))
                    print("✅ Đã gửi ảnh đến client")
                except Exception as e:
                    print(f"❌ Lỗi gửi ảnh: {e}")
                    connected_clients.remove(client)
    except Exception as e:
        print(f"❌ Lỗi kết nối ComfyUI: {e}")

# Khởi động server
async def start_servers():
    server_react = await websockets.serve(handle_client, "localhost", 8765, max_size=10**8)
    server_comfyui = await websockets.serve(handle_comfyui, "localhost", 8766, max_size=10**8)
    print("Server đang chạy trên cổng 8765 và 8766...")
    await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(start_servers())