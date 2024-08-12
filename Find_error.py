from pairs_erro import analyze_words
from pairs_same import process_and_compare_strings
from Sq2ToSq2 import preprocess_string

def compare_strings(string1, string2):
    # So sánh hai chuỗi và lấy các cặp từ tốt nhất
    filtered_best_pairs = process_and_compare_strings(string1, string2)

    # Phân tích các cặp từ
    results = []
    for pair in filtered_best_pairs:
        differences = analyze_words(pair[0], pair[1])
        results.append({
            'pair': pair,
            'spelling_erro': differences
        })

    return results


# Ví dụ sử dụng
#string1 = "hello how are you computer apple yessss"
#string2 = "now far you kom app"
#comparison_results = compare_strings(string1, string2)

#print(comparison_results)

# Create an empty list to store the words from pair[0]
def compute_string3(string1, string2):
    # đưa 2 chuỗi về chữ thường
    string1 = preprocess_string(string1)
    string2 = preprocess_string(string2)
    # Create a list to store words from pair[0]
    comparison_results = compare_strings(string1, string2)
    words_from_pair0 = []

    # Iterate through each result in comparison_results
    for result in comparison_results:
        pair = result['pair']
        # Add pair[0] to the words_from_pair0 list
        words_from_pair0.append(pair[0])

    # Convert string1 to a list of words
    words_in_string1 = string1.split()

    # Remove words that are in words_from_pair0 from words_in_string1
    # Flatten words_from_pair0 to a single list of words
    words_from_pair0_flat = ' '.join(words_from_pair0).split()
    filtered_words = [word for word in words_in_string1 if word not in words_from_pair0_flat]

    # Join the remaining words into a single string
    string3 = ' '.join(filtered_words)

    # Convert string2 to a list of words
    words_in_string2 = set(string2.split())

    # Find words in string3 that are not in string2
    unique_words_in_string3 = set(string3.split()) - words_in_string2

    # Convert the set of unique words back to a list or string if needed
    unique_words_list = list(unique_words_in_string3)
    unique_words_string = ' '.join(unique_words_list)

    # Print the resulting unique words (optional)
    #print(unique_words_string)

    return unique_words_string

string1 = 'hello how are you ok'
string2 = 'how are you'
unique_words = compute_string3( string1, string2)
#print(unique_words)
