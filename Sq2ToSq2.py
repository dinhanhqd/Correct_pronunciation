import re
from score import Score_result
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

def compare_words(string1, string2):
    """
    So sánh hai chuỗi từ đầu vào và trả về danh sách các từ trong chuỗi đầu tiên.
    Các từ khác biệt giữa hai chuỗi sẽ được trả về dưới dạng JSON.

    :param string1: Chuỗi đầu tiên.
    :param string2: Chuỗi thứ hai.
    :return: Danh sách các từ khác biệt dưới dạng JSON.
    """
    # Tiền xử lý chuỗi
    processed_string1 = preprocess_string(string1)
    processed_string2 = preprocess_string(string2)

    # Tách chuỗi thành các từ
    words1 = processed_string1.split()
    words2 = processed_string2.split()

    # Chuyển danh sách từ thành tập hợp để dễ so sánh
    set_words2 = set(words2)

    # Lọc các từ chỉ có trong chuỗi đầu tiên
    different_words = [word for word in words1 if word not in set_words2]

    return different_words


