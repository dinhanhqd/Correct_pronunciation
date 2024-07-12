import eng_to_ipa

class EngPhonemConverter:
    def __init__(self) -> None:
        super().__init__()

    def convertToPhonem(self, sentence: str) -> str:
        phonem_representation = eng_to_ipa.convert(sentence)
        phonem_representation = phonem_representation.replace('*', '')
        return phonem_representation


# Example usage
converter = EngPhonemConverter()
sentence = "Hello, how are you?"
ipa_representation = converter.convertToPhonem(sentence)
print(f"Input Text: {sentence}")
print(f"IPA Transcription: {ipa_representation}")
