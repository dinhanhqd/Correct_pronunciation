from dash import html
from Find_error import compare_strings, compute_string3
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

def highlight_errors(string1, string2):
    string1 = preprocess_string(string1)
    string2 = preprocess_string(string2)
    # So sánh chuỗi để lấy các lỗi chính tả
    spelling_errors = compare_strings(string1, string2)
    #print(spelling_errors)
    # Tạo danh sách các tuple chứa cặp pair[0] và spelling_erro[1]
    pair_and_errors = [(error['pair'][0], [pair[1] for pair in error['spelling_erro']]) for error in spelling_errors]

    # Tạo một từ điển để lưu các phần cần bôi đỏ cho từng từ
    highlight_parts = {}
    for word, error_parts in pair_and_errors:
        highlight_parts[word] = error_parts

    # Lấy danh sách các từ lỗi từ compute_string3
    wordErro = compute_string3(string1, string2)

    # Tạo tập hợp các từ lỗi để dễ kiểm tra
    wordErro_set = set(wordErro.split())  # Chia từ lỗi thành danh sách và tạo tập hợp

    words = string1.split()
    result = []

    for word in words:
        if word in highlight_parts or word in wordErro_set:
            temp_result = []
            if word in wordErro_set:
                # Bôi đỏ toàn bộ từ nếu nó nằm trong wordErro_set
                temp_result.append(html.Span(word, style={'color': 'red'}))
            else:
                # Bôi đỏ các phần của từ từ highlight_parts
                parts_to_highlight = highlight_parts.get(word, [])
                i = 0
                while i < len(word):
                    highlighted = False
                    for part in parts_to_highlight:
                        if word[i:i + len(part)] == part:
                            temp_result.append(html.Span(word[i:i + len(part)], style={'color': 'red'}))
                            i += len(part) - 1
                            highlighted = True
                            break
                    if not highlighted:
                        temp_result.append(html.Span(word[i]))
                    i += 1
            result.extend(temp_result)
        else:
            result.append(html.Span(word))

        # Thêm dấu cách giữa các từ
        result.append(html.Span(' '))

    result.append(html.Br())
    return result

# Ví dụ sử dụng hàm
string1 = "Hello how are you computer apple"
string2 = " now far you kom app"
highlighted_output = highlight_errors(string1, string2)
#print(highlighted_output)
