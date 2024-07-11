import streamlit as st
import numpy as np
import soundfile as sf
import base64
import streamlit as st
import sounddevice as sd
import scipy.io.wavfile as wavfile
from io import BytesIO
import text_to_tp
# Tựa đề cho ứng dụng
st.title('Tìm lỗi sai trong phát âm tiếng Anh')

# Ô nhập dữ liệu văn bản
text_input = st.text_input("Nhập văn bản của bạn:")

sentence = text_input
phonemes = text_to_tp.text_to_phonemes(sentence)
# Nút bấm cho dữ liệu văn bản
if st.button('Chuyển đổi thành phiên âm'):
    st.write('Văn bản gốc:',sentence)
    st.write('Sau khi chuyển đổi:', phonemes)


# Biến để lưu trữ trạng thái ghi âm
is_recording = st.checkbox('Bắt đầu ghi âm')

# Hàm để ghi âm
def record(duration, fs, channels):
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=channels)
    sd.wait()  # Chờ cho đến khi ghi xong
    return recording

# Khi checkbox được chọn, bắt đầu ghi âm
if is_recording:
    st.write("Đang ghi âm...")
    fs = 44100  # Tần số lấy mẫu
    duration = 5  # Thời lượng ghi âm tính bằng giây
    channels = 1  # Số kênh (1 cho mono, 2 cho stereo)

    recording = record(duration, fs, channels)

    # Lưu bản ghi âm vào một file WAV trong bộ nhớ
    wav_io = BytesIO()
    wavfile.write(wav_io, fs, recording)
    wav_io.seek(0)

    # Phát bản ghi âm
    st.audio(wav_io, format='audio/wav')

    # Hiển thị dạng sóng âm thanh
    #st.line_chart(recording)

    # Lưu bản ghi âm vào file
    with open('recorded_audio.wav', 'wb') as f:
        f.write(wav_io.read())

def main():

    st.sidebar.title("CSV File Upload")

    # Tải lên tệp âm thanh
    uploaded_file = st.sidebar.file_uploader("Chọn tệp âm thanh", type=["wav", "mp3"])

    if uploaded_file is not None:
        # Đọc tệp âm thanh
        data, samplerate = sf.read(uploaded_file)

        # Phát âm thanh
        st.audio(uploaded_file)

if __name__ == "__main__":
        main()