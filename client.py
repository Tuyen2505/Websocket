import socket
import cv2
import numpy as np

# Đường dẫn đến file ảnh
image_path = r"D:\image\Screenshot 2025-03-01 133510.png"

# Đọc ảnh từ file
frame = cv2.imread(image_path)

# Kiểm tra xem ảnh có được đọc thành công không
if frame is None:
    print("Không thể đọc ảnh. Hãy kiểm tra lại đường dẫn!")
    exit()

# Kết nối tới server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("127.0.0.1", 8765))

# Mã hóa ảnh thành bytes
_, img_encoded = cv2.imencode(".jpg", frame)
img_bytes = img_encoded.tobytes()
img_size = len(img_bytes)

# Gửi kích thước ảnh (4 byte) + dữ liệu ảnh
client_socket.sendall(img_size.to_bytes(4, byteorder="big") + img_bytes)

print("Ảnh đã được gửi thành công!")

# Đóng kết nối
client_socket.close()

# import websockets
# import asyncio
# import json

# async def send_image_to_comfyui():
#     async with websockets.connect("ws://127.0.0.1:8188/ws") as websocket:
#         image_path = "D:/image/Avatar-cute-meo.jpg"  # Đường dẫn file ảnh

#         prompt = {
#             "prompt": {
#                 "name": "image_input",
#                 "nodes": {
#                     "1": {"type": "LoadImage", "inputs": {"image": image_path}},
#                     "2": {"type": "ImagePreview", "inputs": {"image": ["1", 0]}},
#                 },
#                 "connections": [["1", "image", "2", "image"]],
#             }
#         }

#         await websocket.send(json.dumps(prompt))
        
#         # Nhận phản hồi từ ComfyUI
#         while True:
#             response = await websocket.recv()
#             print("Response from ComfyUI:", response)

# asyncio.run(send_image_to_comfyui())


