import nltk
from nltk.tokenize import word_tokenize
import pronouncing

# Tải dữ liệu từ nltk (chỉ cần thực hiện một lần)
nltk.download('punkt')

def text_to_phonemes(sentence):
    # Tokenize câu thành các từ
    words = word_tokenize(sentence)

    # Tạo danh sách lưu trữ các âm vị của từng từ
    phonemes = []

    # Lặp qua từng từ trong câu và lấy âm vị của từ đó
    for word in words:
        # Lấy danh sách các âm vị của từ (có thể có nhiều phiên âm)
        word_phonemes = pronouncing.phones_for_word(word)

        # Lựa chọn phiên âm đầu tiên (nếu có)
        if word_phonemes:
            phoneme = word_phonemes[0]
            phonemes.append(phoneme)
        else:
            phonemes.append("UNKNOWN")  # hoặc có thể sử dụng từ khóa để biểu thị từ không biết

    return phonemes