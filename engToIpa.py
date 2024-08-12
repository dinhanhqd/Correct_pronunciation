import eng_to_ipa

def convertToPhonem(sentence: str) -> str:
    """
    Chuyển đổi văn bản thành âm vị bằng cách sử dụng mô hình eng_to_ipa.

    :param sentence: Văn bản tiếng Anh đầu vào.
    :return: Chuỗi âm vị IPA.
    """
    try:
        phonem_representation = eng_to_ipa.convert(sentence)
        # Loại bỏ ký tự '*' nếu có
        phonem_representation = phonem_representation.replace('*', '')
        return phonem_representation
    except Exception as e:
        print(f"Error using eng_to_ipa: {e}")
        return ""

# Chuyển đổi văn bản thành âm vị
sentence = "hello world"
eng_phonem = convertToPhonem(sentence)

#print(f"EngToIPA Phonem: {eng_phonem}")
