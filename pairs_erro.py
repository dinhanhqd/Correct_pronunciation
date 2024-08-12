import nltk
from nltk.corpus import cmudict

# Tải từ điển CMU Pronouncing Dictionary
nltk.download('cmudict')
d = cmudict.dict()

def get_syllables_from_index(word):
    """
    Trả về một danh sách các âm tiết cùng với chữ cái tương ứng của chúng.
    Chỉ lấy cách phát âm đầu tiên của từ.
    """
    word = word.lower()
    syllable_data = []

    if word in d:
        pronunciations = d[word]

        # Chỉ lấy cách phát âm đầu tiên
        if pronunciations:
            pronunciation = pronunciations[0]
            syllables = []
            syllable = []
            syllable_letters_map = []
            word_letters = list(word)
            index = 0

            for phoneme in pronunciation:
                syllable.append(phoneme)
                # Nếu phoneme kết thúc bằng số, đó là một âm tiết
                if phoneme[-1].isdigit():
                    syllables.append(' '.join(syllable))
                    syllable_letters = []
                    for phoneme in syllable:
                        if phoneme[-1].isdigit():
                            # Tìm các chữ cái tương ứng với âm tiết
                            syllable_letters.append(''.join(word_letters[index:index + len(phoneme)]))
                            index += len(phoneme)  # Di chuyển chỉ số theo chiều dài phoneme
                    syllable_letters_map.append({'syllable': ' '.join(syllable), 'letters': ''.join(syllable_letters)})
                    syllable = []

            if syllable:
                syllables.append(' '.join(syllable))

            # Lưu âm tiết và chữ cái tương ứng vào danh sách
            syllable_data.append({'pronunciation': 1, 'syllables': syllable_letters_map})

    #else:
        #print(f"Từ '{word}' không có trong từ điển.")

    return syllable_data

def convert_to_key_value_pairs(syllable_data):
    """
    Chuyển đổi dữ liệu âm tiết thành các cặp key và value.
    """
    key_value_pairs = []

    for pronunciation in syllable_data:
        pronun_key = f"Phát âm {pronunciation['pronunciation']}"
        for syllable_info in pronunciation['syllables']:
            syllable_key = syllable_info['syllable']
            letters_value = syllable_info['letters']
            key_value_pairs.append((syllable_key, letters_value))

    return key_value_pairs

def compare_key_value_pairs(pairs1, pairs2):
    """
    So sánh hai danh sách các cặp key và value và trả về các cặp key và value khác biệt.
    """
    dict1 = dict(pairs1)
    dict2 = dict(pairs2)

    only_in_first = {k: dict1[k] for k in dict1 if k not in dict2}
    #only_in_second = {k: dict2[k] for k in dict2 if k not in dict1}

    return list(only_in_first.items()) #+ list(only_in_second.items())

def analyze_words(word1, word2):
    """
    Tổng hợp các bước phân tích âm tiết, chuyển đổi và so sánh cho hai từ.
    """
    # Lấy dữ liệu âm tiết từ từ điển cho hai từ
    syllable_data1 = get_syllables_from_index(word1)
    syllable_data2 = get_syllables_from_index(word2)

    # Chuyển đổi dữ liệu thành các cặp key và value
    key_value_pairs1 = convert_to_key_value_pairs(syllable_data1)
    key_value_pairs2 = convert_to_key_value_pairs(syllable_data2)

    # So sánh các cặp key và value
    differences = compare_key_value_pairs(key_value_pairs1, key_value_pairs2)

    return differences

# Ví dụ kiểm tra với hai từ
word1 = 'computer'
word2 = 'com'

# Phân tích và in ra các cặp khác biệt
differences = analyze_words(word1, word2)
#for key, value in differences:
    #print(f"{key}: {value}")

#print(differences)
