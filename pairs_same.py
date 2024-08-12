import re
import Levenshtein
import numpy as np
from scipy.optimize import linear_sum_assignment

def preprocess_string(s):
    # Chuyển chuỗi thành chữ thường và xóa ký tự đặc biệt
    s = s.lower()
    s = re.sub(r'[^\w\s]', '', s)  # Xóa ký tự đặc biệt
    return s

def create_similarity_matrix(list1, list2):
    # Tạo ma trận độ tương đồng
    matrix = np.zeros((len(list1), len(list2)))

    for i, word1 in enumerate(list1):
        for j, word2 in enumerate(list2):
            # Tính khoảng cách Levenshtein và chuyển đổi thành độ tương đồng
            distance = Levenshtein.distance(word1, word2)
            max_len = max(len(word1), len(word2))
            similarity = 1 - (distance / max_len)  # Chuyển khoảng cách thành độ tương đồng
            matrix[i, j] = similarity

    return matrix

def find_best_word_pairs(matrix):
    # Tìm ánh xạ tối ưu cho ma trận độ tương đồng
    cost_matrix = 1 - matrix  # Chuyển đổi độ tương đồng thành chi phí
    row_ind, col_ind = linear_sum_assignment(cost_matrix)  # Tìm ánh xạ tối ưu cho chi phí
    return list(zip(row_ind, col_ind))

def get_pairs(list1, list2, pairs):
    # Lấy các cặp từ tương ứng
    return [(list1[i], list2[j]) for i, j in pairs]

def best_pairs_same(best_pairs):
    # Loại trừ các cặp giống nhau hoàn toàn
    return [pair for pair in best_pairs if pair[0] != pair[1]]

def process_and_compare_strings(string1, string2):
    # Xử lý chuỗi
    processed_string1 = preprocess_string(string1)
    processed_string2 = preprocess_string(string2)

    # Tạo danh sách từ
    words1 = processed_string1.split()
    words2 = processed_string2.split()

    # Tạo ma trận độ tương đồng
    similarity_matrix = create_similarity_matrix(words1, words2)

    # Tìm các cặp từ với độ tương đồng cao nhất
    pairs = find_best_word_pairs(similarity_matrix)
    best_pairs = get_pairs(words1, words2, pairs)

    # Loại bỏ các cặp từ giống nhau hoàn toàn
    best_pairs_filtered = best_pairs_same(best_pairs)

    return best_pairs_filtered

# Ví dụ sử dụng
string1 = "ok ok how , are!"
string2 = "yes ok low ,far and now  !"

# Gọi hàm tổng hợp
filtered_best_pairs = process_and_compare_strings(string1, string2)

# In kết quả
#for pair in filtered_best_pairs:
    #print(f"Cặp từ: '{pair[0]}' và '{pair[1]}'")

#print(filtered_best_pairs)
