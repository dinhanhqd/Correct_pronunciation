from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import logging
import os
import tempfile
from spToText import sp_to_tx
from engToIpa import convertToPhonem
from Sq2ToSq2 import compare_words
from score import Score_result

app = FastAPI()

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cho phép tất cả các nguồn gốc, thay đổi theo nhu cầu
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả các phương thức
    allow_headers=["*"],  # Cho phép tất cả các tiêu đề
)

# Cấu hình ghi log
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Định nghĩa lớp dữ liệu cho yêu cầu API
class TextData(BaseModel):
    text1: str
    text2: str

@app.post("/convert-text-to-ipa")
async def convert_text_to_ipa(data: TextData):
    try:
        # Ghi log thông tin nhận được
        logger.info(f"Nhận dữ liệu: {data.json()}")

        # Sử dụng text từ TextData
        ipa_result = convertToPhonem(data.text1)
        logger.info(f"Kết quả IPA: {ipa_result}")
        return {"ipa": ipa_result}
    except Exception as e:
        # Ghi log lỗi và trả về mã lỗi 500
        logger.error(f"Lỗi trong convert_text_to_ipa: {str(e)}")
        return JSONResponse(status_code=500, content={"message": str(e)})

@app.post("/check-button")
async def check_button(data: TextData):
    try:
        # Ghi log dữ liệu nhận được
        logger.info(f"Nhận dữ liệu: {data.json()}")

        # So sánh từ
        check_button_result = compare_words(data.text1, data.text2)
        logger.info(f"Kết quả so sánh: {check_button_result}")

        # Tính điểm
        score = Score_result(data.text1, data.text2)
        logger.info(f"Điểm số: {score}")

        return {"check_button": check_button_result, "score_result": score}

    except Exception as e:
        # Ghi log lỗi
        logger.error(f"Lỗi trong compare_words: {str(e)}")
        # Trả về phản hồi JSON với thông điệp lỗi
        return JSONResponse(status_code=500, content={"message": "Lỗi nội bộ của máy chủ"})

@app.post("/upload-audio")
async def upload_audio(file: UploadFile = File(...)):
    try:
        # Định nghĩa đường dẫn lưu tệp văn bản
        text_file_location = f"uploaded_audio/text_output.txt"
        os.makedirs(os.path.dirname(text_file_location), exist_ok=True)

        # Lưu tệp âm thanh vào thư mục cụ thể
        file_location = f"uploaded_audio/{file.filename}"
        os.makedirs(os.path.dirname(file_location), exist_ok=True)

        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())

        # Chuyển đổi âm thanh thành văn bản
        text_audio = sp_to_tx(file_location)

        # Lưu văn bản vào tệp văn bản
        with open(text_file_location, "w") as text_file:
            text_file.write(text_audio)

        # In ra đường dẫn tệp văn bản cho kiểm tra
        logger.info(f"Tạo tệp văn bản tại: {text_file_location}")
        return {"text": text_audio}

    except Exception as e:
        logger.error(f"Lỗi trong upload_audio: {str(e)}")
        return JSONResponse(status_code=500, content={"message": str(e)})

@app.get("/get-temp-file-content")
async def get_temp_file_content():
    try:
        # Đọc nội dung của tệp tạm và trả về
        temp_files = [f for f in os.listdir('uploaded_audio') if f.endswith('.txt') and os.path.isfile(os.path.join('uploaded_audio', f))]
        if temp_files:
            temp_file_path = os.path.join('uploaded_audio', temp_files[0])  # Chọn tệp tạm đầu tiên
            with open(temp_file_path, "r") as temp_file:
                temp_file_content = temp_file.read()
            return {"text": temp_file_content}
        else:
            return JSONResponse(status_code=404, content={"message": "Tệp tạm không tìm thấy"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})

@app.on_event("shutdown")
def shutdown_event():
    # Xóa tất cả các tệp tạm khi server tắt
    temp_files = [f for f in os.listdir('.') if f.endswith('.txt') and os.path.isfile(f)]
    for temp_file in temp_files:
        os.remove(temp_file)
        logger.info(f"Đã xóa tệp tạm: {temp_file}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
