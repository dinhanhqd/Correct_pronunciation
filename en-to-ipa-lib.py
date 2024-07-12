from pydub import AudioSegment
import speech_recognition as sr
from eng_to_ipa import ipa_list

def process(filepath, chunksize=60000):
    # Load mp3 file
    sound = AudioSegment.from_mp3(filepath)

    # Function to divide audio into chunks
    def divide_chunks(sound, chunksize):
        for i in range(0, len(sound), chunksize):
            yield sound[i:i + chunksize]
    
    chunks = list(divide_chunks(sound, chunksize))
    print(f"{len(chunks)} chunks of {chunksize/1000}s each")

    r = sr.Recognizer()
    string_index = {}

    # Process each chunk
    for index, chunk in enumerate(chunks):
        temp = 'temp.wav'
        chunk.export(temp, format='wav')
        
        # Recognize speech from WAV file
        with sr.AudioFile(temp) as source:
            audio = r.record(source)
        recognized_text = r.recognize_google(audio, language="en-US")
        
        # Convert recognized text to IPA
        ipa_transcription = ipa_list(recognized_text)
        
        # Store results
        string_index[index] = (recognized_text, ipa_transcription)
    
    # Format output
    result = []
    for i in range(len(string_index)):
        result.append(f"Chunk {i+1} - Text: {string_index[i][0]}")
        result.append(f"IPA: {string_index[i][1]}")
    
    return "\n".join(result)

# Example usage
audio_file_name = 'test.mp3'
text_and_ipa = process(audio_file_name)
print(text_and_ipa)
