# from flask import Flask, request, jsonify, send_from_directory
# from flask_cors import CORS
# import base64
# import os

# app = Flask(__name__)
# CORS(app)

# # Thư mục lưu ảnh
# UPLOAD_FOLDER = 'static/images'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# data = None

# # Đảm bảo thư mục tồn tại
# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)

# def clear_old_images():
#     """Xóa tất cả ảnh cũ trong thư mục lưu trữ."""
#     for filename in os.listdir(UPLOAD_FOLDER):
#         file_path = os.path.join(UPLOAD_FOLDER, filename)
#         if os.path.isfile(file_path):
#             os.remove(file_path)





# import google.generativeai as genai
# import PIL.Image

# # Cấu hình API Key
# genai.configure(api_key="AIzaSyC6h1sGMN1u3QkXBGBtiT2Ej6OOYaYcYWU")

# # Chọn mô hình
# model = genai.GenerativeModel('gemini-2.0-flash-exp')

# def generate_ad_from_image(image_path, prompt):
#     """
#     Gửi ảnh và prompt đến mô hình Gemini để tạo quảng cáo.

#     Args:
#         image_path: Đường dẫn đến file ảnh.
#         prompt: Câu lệnh yêu cầu mô tả và viết quảng cáo.

#     Returns:
#         Văn bản quảng cáo được tạo bởi mô hình.
#     """
#     try:
#         img = PIL.Image.open(image_path)
#     except FileNotFoundError:
#         return "Không tìm thấy file ảnh."

#     response = model.generate_content([prompt, img])
#     return response.text

# # Đường dẫn đến file ảnh của bạn
# image_file_path = "D:/vscode/testsocket/static/images/0.jpg"






# @app.route("/upload", methods=["POST"])
# def upload():
#     global data
#     data = request.json
#     if not data or "image_caption" not in data or "image_detail" not in data:
#         return jsonify({"message": "Dữ liệu không hợp lệ!"}), 400

#     # Xóa ảnh cũ trước khi lưu ảnh mới
#     clear_old_images()

#     urls = {"caption": "", "details": []}

#     # Lưu ảnh caption với tên "0.jpg"
#     caption_base64 = data["image_caption"]
#     caption_filename = "0.jpg"
#     caption_path = os.path.join(app.config['UPLOAD_FOLDER'], caption_filename)
#     with open(caption_path, "wb") as f:
#         f.write(base64.b64decode(caption_base64))
#     urls["caption"] = f"http://localhost:3003/static/images/{caption_filename}"

#     # Lưu ảnh chi tiết theo thứ tự 1, 2, 3...
#     detail_base64_array = data["image_detail"]
#     for i, detail_base64 in enumerate(detail_base64_array, start=1):
#         detail_filename = f"{i}.jpg"
#         detail_path = os.path.join(app.config['UPLOAD_FOLDER'], detail_filename)
#         with open(detail_path, "wb") as f:
#             f.write(base64.b64decode(detail_base64))
#         urls["details"].append(f"http://localhost:3003/static/images/{detail_filename}")

#     return jsonify({
#         "message": "Dữ liệu đã nhận thành công!",
#         "urls": urls
#     })

# @app.route('/static/<path:path>')
# def send_static(path):
#     return send_from_directory(UPLOAD_FOLDER, path)


# @app.route("/", methods=["GET"])
# def get_all_images():
#     try:
#         # Lấy danh sách file theo thứ tự 0, 1, 2...
#         image_files = sorted(
#             [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith('.jpg')],
#             key=lambda x: int(os.path.splitext(x)[0])  # Sắp xếp theo số thứ tự
#         )
        
#         if not image_files:
#             return jsonify({
#                 "name": "",
#                 "link": "",
#                 "caption": "",
#                 "image_detail": []
#             }), 200

#         ad_prompt = f"Mô tả chi tiết sản phẩm trong ảnh và viết một đoạn quảng cáo hấp dẫn. Chỉ trả lời mô tả kiểu dáng và quảng cáo, không cần thêm bất kỳ thông tin nào khác. Tên sản phâm {data['product_name']} và đường dẫn sản phẩm là {data['product_link']} trả về cả đường dẫn để người dùng có thể bấm vào link. Đừng quên thêm hashtag vào quảng cáo."
#         ad_text = generate_ad_from_image(image_file_path, ad_prompt)
#         # Lấy ảnh 0.jpg làm caption
#         caption = ad_text

#         # Lấy các ảnh detail (1.jpg, 2.jpg, ...)
#         detail_urls = [
#             f"https://vegetarian-latvia-beach-fingers.trycloudflare.com/static/images/{filename}"
#             for filename in image_files if filename != "0.jpg"
#         ]

#         return jsonify({
#             "caption": caption,
#             "image_detail": detail_urls,
#         }), 200

#     except Exception as e:
#         return jsonify({
#             "message": f"Lỗi khi lấy danh sách ảnh: {str(e)}"
#         }), 500


# if __name__ == "__main__":
#     print("Server chạy tại http://localhost:3003")
#     app.run(host="0.0.0.0", port=3003, debug=True)


from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import base64
import os
import requests # Thêm import này
import google.generativeai as genai
import PIL.Image

app = Flask(__name__)
CORS(app)

# Thư mục lưu ảnh
UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# --- Phần cấu hình và hàm Gemini AI ---
try:
    genai.configure(api_key="AIzaSyC6h1sGMN1u3QkXBGBtiT2Ej6OOYaYcYWU") # THAY KEY CỦA BẠN
    model = genai.GenerativeModel('gemini-2.0-flash-exp') # Sử dụng model vision
except Exception as e:
    print(f"Lỗi cấu hình hoặc khởi tạo model Gemini: {e}")
    model = None

def generate_ad_from_image(image_path, product_name, product_link):
    """
    Gửi ảnh và thông tin sản phẩm đến mô hình Gemini để tạo quảng cáo.
    """
    if not model:
        return "Lỗi: Không thể khởi tạo mô hình AI."
    if not os.path.exists(image_path):
        return "Lỗi: Không tìm thấy file ảnh để tạo caption."

    try:
        img = PIL.Image.open(image_path)
        # Sử dụng prompt từ code gốc của bạn, nhưng thêm product_name và link
        prompt = f"Mô tả chi tiết sản phẩm trong ảnh và viết một đoạn quảng cáo hấp dẫn. Chỉ trả lời mô tả kiểu dáng và quảng cáo, không cần thêm bất kỳ thông tin nào khác. Tên sản phẩm {product_name} và đường dẫn sản phẩm là {product_link} trả về cả đường dẫn để người dùng có thể bấm vào link. Đừng quên thêm hashtag vào quảng cáo."

        response = model.generate_content([prompt, img])

        # Xử lý response (có thể cần điều chỉnh tùy theo cấu trúc trả về của gemini-pro-vision)
        if hasattr(response, 'text'):
             return response.text
        elif hasattr(response, 'parts') and len(response.parts) > 0 and hasattr(response.parts[0], 'text'):
             return response.parts[0].text # Thử lấy text từ part đầu tiên
        elif hasattr(response, 'prompt_feedback') and response.prompt_feedback.block_reason:
             return f"Lỗi từ Gemini: {response.prompt_feedback.block_reason}"
        else:
             print("Không thể trích xuất text từ response Gemini:", response)
             return "Lỗi: Không nhận được phản hồi hợp lệ từ AI."

    except FileNotFoundError:
        return "Lỗi: Không tìm thấy file ảnh khi tạo caption."
    except Exception as e:
        print(f"Lỗi trong quá trình gọi Gemini API: {e}")
        return f"Lỗi khi tạo nội dung quảng cáo: {e}"
# -----------------------------------

# Biến toàn cục để lưu data từ /upload (giữ lại như code gốc)
# Lưu ý: Biến toàn cục không phải là cách tốt nhất trong môi trường production với nhiều request đồng thời.
# Cân nhắc sử dụng database hoặc cơ chế lưu trữ khác nếu ứng dụng phức tạp hơn.
latest_data = None

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def clear_old_images():
    """Xóa tất cả ảnh cũ trong thư mục lưu trữ."""
    for filename in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

@app.route("/upload", methods=["POST"])
def upload():
    global latest_data # Sử dụng biến toàn cục
    data = request.json
    if not data or "image_caption" not in data or "image_detail" not in data or "product_name" not in data or "product_link" not in data:
        return jsonify({"message": "Dữ liệu không hợp lệ! Thiếu thông tin."}), 400

    # Lưu data nhận được vào biến toàn cục để route '/' có thể sử dụng
    latest_data = data.copy() # Tạo bản sao để tránh thay đổi không mong muốn

    saved_urls = {"caption": "", "details": []}
    try:
        clear_old_images()

        # Lưu ảnh caption
        caption_base64 = data["image_caption"]
        caption_filename = "0.jpg"
        caption_path = os.path.join(app.config['UPLOAD_FOLDER'], caption_filename)
        with open(caption_path, "wb") as f:
            f.write(base64.b64decode(caption_base64))
        # Trả về URL tương đối hoặc đầy đủ tùy bạn muốn React xử lý thế nào
        saved_urls["caption"] = f"/static/images/{caption_filename}"

        # Lưu ảnh chi tiết
        detail_base64_array = data["image_detail"]
        for i, detail_base64 in enumerate(detail_base64_array, start=1):
            detail_filename = f"{i}.jpg"
            detail_path = os.path.join(app.config['UPLOAD_FOLDER'], detail_filename)
            with open(detail_path, "wb") as f:
                f.write(base64.b64decode(detail_base64))
            saved_urls["details"].append(f"/static/images/{detail_filename}")

        # --- Gửi POST trống đến webhook ---
        webhook_url = "http://localhost:5678/webhook/autopost"
        print(f"Đang gửi POST request (không có body) đến {webhook_url}...")
        try:
            response = requests.post(webhook_url, timeout=30) # Không có tham số data hay json
            response.raise_for_status() # Kiểm tra lỗi 4xx/5xx

            if response.status_code == 200:
                print("Webhook trả về 200 OK.")
                # Trả về thông báo thành công và URL ảnh đã lưu
                return jsonify({
                    "message": "Đã đăng bài thành công!", # Thông báo thành công cuối cùng
                    "urls": saved_urls # Vẫn trả về URL như ban đầu
                }), 200
            else:
                # Ít khi xảy ra nếu dùng raise_for_status
                print(f"Webhook trả về status code không mong đợi: {response.status_code}")
                return jsonify({
                    "message": f"Webhook báo hiệu không thành công (mã: {response.status_code})",
                    "urls": saved_urls
                }), 502 # Bad Gateway

        except requests.exceptions.RequestException as e:
            print(f"Lỗi khi gọi webhook {webhook_url}: {e}")
            # Trả về thông báo lỗi cho React, nhưng vẫn kèm URL ảnh đã lưu
            return jsonify({
                "message": f"Ảnh đã lưu nhưng lỗi khi kích hoạt đăng bài: {e}",
                "urls": saved_urls
            }), 500 # Internal Server Error

    except Exception as e:
        print(f"Lỗi trong quá trình xử lý upload: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"message": f"Lỗi server khi xử lý ảnh: {e}"}), 500

# --- Khôi phục route GET / ---
@app.route("/", methods=["GET"])
def get_all_images():
    global latest_data # Sử dụng biến toàn cục
    if not latest_data:
         return jsonify({
            "caption": "Chưa có dữ liệu sản phẩm được tải lên.",
            "image_detail": []
        }), 404 # Not found

    try:
        # Xác định đường dẫn ảnh caption (0.jpg)
        caption_image_path = os.path.join(app.config['UPLOAD_FOLDER'], "0.jpg")

        # Lấy tên và link sản phẩm từ dữ liệu đã lưu
        product_name = latest_data.get("product_name", "Sản phẩm không tên")
        product_link = latest_data.get("product_link", "#")

        # Tạo caption bằng AI (sử dụng ảnh 0.jpg và thông tin sản phẩm)
        print(f"GET /: Đang tạo caption cho '{product_name}' từ {caption_image_path}")
        ad_text = generate_ad_from_image(caption_image_path, product_name, product_link)

        # Lấy danh sách file ảnh chi tiết (1.jpg, 2.jpg, ...)
        image_files = sorted(
            [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith('.jpg') and f != '0.jpg'],
            key=lambda x: int(os.path.splitext(x)[0])
        )

        # Tạo URL đầy đủ cho ảnh chi tiết (Sử dụng URL tương đối hoặc cấu hình base URL)
        base_url = request.host_url.rstrip('/') # Lấy base URL động từ request
        detail_urls = [
            f"{base_url}/static/images/{filename}"
            for filename in image_files
        ]

        return jsonify({
            "caption": ad_text, # Caption do AI tạo ra
            "image_detail": detail_urls, # Danh sách URL ảnh chi tiết
            # Bạn có thể thêm lại tên và link sản phẩm nếu cần
            # "name": product_name,
            # "link": product_link
        }), 200

    except FileNotFoundError:
         return jsonify({"message": "Lỗi: Không tìm thấy ảnh caption (0.jpg) để xử lý."}), 404
    except Exception as e:
        print(f"Lỗi trong route GET /: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"message": f"Lỗi khi lấy dữ liệu và tạo caption: {str(e)}"}), 500

# Route để phục vụ file tĩnh (ảnh)
@app.route('/static/images/<path:filename>')
def send_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    print("Server chạy tại http://localhost:3003")
    app.run(host="0.0.0.0", port=3003, debug=True) # Tắt debug=True trong production