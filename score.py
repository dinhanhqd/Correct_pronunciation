import nltk
from nltk.corpus import cmudict
import re

def preprocess_string(s):
    """
    Tiền xử lý chuỗi bằng cách chuyển thành chữ thường và xóa ký tự đặc biệt.
    :param s: Chuỗi đầu vào.
    :return: Chuỗi đã được tiền xử lý.
    """
    # Chuyển thành chữ thường
    s = s.lower()
    # Xóa ký tự đặc biệt (giữ lại chữ cái, số và khoảng trắng)
    s = re.sub(r'[^\w\s]', '', s)
    return s

# Khởi tạo từ điển âm tiết
d = cmudict.dict()

def count_syllables(word):
    """ Đếm số âm tiết trong một từ """
    word = word.lower()
    if word in d:
        syllables = [len(list(y for y in x if y[-1].isdigit())) for x in d[word]]
        return max(syllables)
    else:
        # Nếu từ không có trong từ điển, tính là 1 âm tiết
        return 1

def Score_result(text1, text2):
    """ Tính tổng số âm tiết của chuỗi 1 và số âm tiết trong chuỗi 2 giống với chuỗi 1 """
    text1 = preprocess_string(text1)
    text2 = preprocess_string(text2)

    words1 = text1.split()
    words2 = text2.split()

    syllables1 = [count_syllables(word) for word in words1]
    syllables2 = [count_syllables(word) for word in words2]

    # Tính tổng số âm tiết của chuỗi 1
    total_syllables_text1 = sum(syllables1)

    # Tạo từ điển với số âm tiết của từng từ trong text1
    syllable_dict1 = dict(zip(words1, syllables1))

    # Tính số âm tiết trong text2 giống với text1
    matching_syllables = 0
    for word in words2:
        syllables_word2 = count_syllables(word)
        if word in syllable_dict1 and syllables_word2 == syllable_dict1[word]:
            matching_syllables += syllables_word2

    return matching_syllables,total_syllables_text1

# Ví dụ sử dụng
text1 = "hello how are you?"
text2 = "Hello how far you"

#score = Score_result(text1,text2)
#print(score)
