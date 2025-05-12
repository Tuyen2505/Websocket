import socket
import io
from PIL import Image

def stream_image(image_path):
    # Mở ảnh và chuyển thành byte array
    with Image.open(image_path) as img:
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format="JPEG")
        image_data = img_byte_arr.getvalue()

    # Kết nối đến Python socket server
    server_address = ("127.0.0.1", 8888)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect(server_address)
        client.sendall(image_data)  # Gửi dữ liệu ảnh

    print("Image sent.")

# Gọi hàm với đường dẫn ảnh
stream_image("D:/image/Avatar-cute-meo.jpg")
