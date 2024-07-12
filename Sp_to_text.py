import locale

# Đặt mã hóa mặc định là UTF-8
locale.getpreferredencoding = lambda: "UTF-8"

# Import các thư viện cần thiết
import whisper
from pydub import AudioSegment

# Tải mô hình Whisper
model = whisper.load_model("tiny")

# Đường dẫn tới tệp âm thanh của bạn
audio_path = "test.mp3"

# Chuyển đổi âm thanh thành văn bản
def sp_to_tx(audio):
    resutl = model.transcribe(audio)
    return resutl["text"]

result_aidio = model.transcribe(audio_path)

# In ra kết quả
#print(result_aidio["text"])