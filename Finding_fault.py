import Align
import Sp_to_text
import text_to_tp
import string
import streamlit as st

# Đường dẫn tới tệp âm thanh của bạn
audio_path = "test.mp3"

# Chuyển đổi âm thanh thành văn bản
result = Sp_to_text.sp_to_tx(audio_path)

# Văn bản mẫu để so sánh (ví dụ)
reference_text = "It's late now. Are you skill up? What are you thinking, or worrying about? Do you still remember your dream? Is it getting closer or further?"


def preprocess_string(s):
    # Chuyển về chữ thường
    s = s.lower()

    # Loại bỏ dấu câu và giữ lại dấu cách
    s_without_punctuation = ''.join(char if char not in string.punctuation else ' ' for char in s)

    # Loại bỏ dấu cách thừa
    s_without_punctuation = ' '.join(s_without_punctuation.split())

    return s_without_punctuation


def find_differences(str1, str2):
    # Tiền xử lý chuỗi
    str1 = preprocess_string(str1)
    str2 = preprocess_string(str2)

    words1 = str1.split()
    words2 = str2.split()

    differences = [word for word in words1 if word not in words2]

    return differences


def finding_fault(reference_text, result):
    # Chuyển đổi các chuỗi thành các chuỗi âm vị để so sánh
    seq1 = text_to_tp.text_to_phonemes(reference_text)
    seq2 = text_to_tp.text_to_phonemes(result)

    # Tính toán số lượng insertions, deletions, substitutions và độ chính xác
    err_count, total_count, additional_data = Align.Correct_Rate(seq1, seq2)
    detection_accuracy = Align.Accuracy(seq1, seq2)

    # Tìm các từ bị sai trong seq2 so với seq1
    aligned_seq1, aligned_seq2 = Align.Align(seq1, seq2)  # Giả sử hàm này tồn tại

    incorrect_words = []
    for i in range(len(aligned_seq1)):
        if aligned_seq1[i] != aligned_seq2[i]:
            incorrect_words.append(aligned_seq2[i])

    false_acceptance = find_differences(reference_text, result)

    # Trả về các giá trị cần thiết
    return err_count, total_count, false_acceptance, detection_accuracy, incorrect_words


# Gọi hàm và gán kết quả trả về cho các biến tương ứng
err_count, total_count, false_acceptance, detection_accuracy, incorrect_words = finding_fault(reference_text, result)

# In kết quả (hoặc sử dụng như bạn muốn, ví dụ như lưu vào session state)
print("Number of errors:", err_count)
print("Total count of words:", total_count)
print("False acceptance words:", false_acceptance)
print("Detection accuracy:", detection_accuracy)
print("Incorrect words in seq2 compared to seq1:", incorrect_words)

# Lưu false_acceptance vào session state của Streamlit
st.session_state['false_acceptance'] = false_acceptance
