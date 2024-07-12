import streamlit as st
import numpy as np
import soundfile as sf
import sounddevice as sd
import scipy.io.wavfile as wavfile
from io import BytesIO
import text_to_tp
import Sp_to_text
from pydub import AudioSegment
import Finding_fault

def main():
    st.sidebar.title("CSV File Upload")

    # Tải lên tệp âm thanh
    uploaded_file = st.sidebar.file_uploader("Chọn tệp âm thanh", type=["wav", "mp3"], key="sidebar_uploader")

    if uploaded_file is not None:
        # Đọc tệp âm thanh
        audio = AudioSegment.from_file(BytesIO(uploaded_file.read()),
                                       format="mp3" if uploaded_file.name.endswith(".mp3") else "wav")
        audio_path = "uploaded_audio.wav"
        audio.export(audio_path, format="wav")

        # Phát âm thanh
        st.audio(audio_path)

        return audio_path

# Tựa đề cho ứng dụng
st.title('Tìm lỗi sai trong phát âm tiếng Anh')

# Ô nhập dữ liệu văn bản
text_input = st.text_input("Nhập văn bản của bạn:")

# Sử dụng cột để đặt các nút bấm cùng hàng
col1, col2 = st.columns(2)

with col1:
    if st.button('Xác nhận'):
        st.session_state['sentence'] = text_input
        st.session_state['phonemes'] = text_to_tp.text_to_phonemes(text_input)
        st.session_state['confirm_clicked'] = True

with col2:
    if st.button('Chuẩn đoán phát âm'):
        uploaded_audio_path = main()
        if uploaded_audio_path:
            transcribed_text = Sp_to_text.sp_to_tx(uploaded_audio_path)
            err_count, total_count, false_acceptance, detection_accuracy, incorrect_words = Finding_fault.finding_fault(transcribed_text, st.session_state.get('sentence', ''))
            st.session_state['transcribed_text'] = transcribed_text
            st.session_state['err_count'] = err_count
            st.session_state['total_count'] = total_count
            st.session_state['false_acceptance'] = false_acceptance
            st.session_state['detection_accuracy'] = detection_accuracy
            st.session_state['incorrect_words'] = incorrect_words
            st.session_state['sp_to_text_clicked'] = True
        else:
            st.session_state['sp_to_text_clicked'] = False

# Hiển thị kết quả cho nút "Xác nhận"
if st.session_state.get('confirm_clicked', False):
    st.write('Văn bản:', st.session_state['sentence'])
    # st.write('Sau khi chuyển đổi:', st.session_state['phonemes'])

# Hiển thị kết quả cho nút "spTOtext"
if st.session_state.get('sp_to_text_clicked', False):
    st.write("Số phiên âm lỗi:", st.session_state['err_count'])
    st.write("Tổng số phiên âm:", st.session_state['total_count'])
    st.write("từ bị sai:",','.join(st.session_state['false_acceptance']))
    st.write("Độ chính xác:", st.session_state['detection_accuracy'])
    st.write("Phiêm âm đúng là :", ', '.join(st.session_state['incorrect_words']))

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

    # Lưu bản ghi âm vào file
    with open('recorded_audio.wav', 'wb') as f:
        f.write(wav_io.read())

if __name__ == "__main__":
    main()
