# Import các thư viện cần thiết
import whisper
from pydub import AudioSegment

# Tải mô hình Whisper
model = whisper.load_model("tiny")

# Đường dẫn tới tệp âm thanh của bạn
audio_path = "test.mp3"

# Chuyển đổi âm thanh thành văn bản với chỉ định ngôn ngữ
def sp_to_tx(audio):
    result = model.transcribe(audio, language="en")
    return result["text"]

result_audio = sp_to_tx(audio_path)

# In ra kết quả
print(result_audio)
