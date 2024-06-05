book = "books/frankenstein.txt"
word_count = 0

def sort_on(dict):
    return dict["count"]

def count_words(text):
    return len(text.split())

def count_characters(text):
    result = {}
    lowered_text = text.lower()
    for char in lowered_text:
        if char not in result:
            result[char] = 1
        else:
            result[char] += 1
    return result

def gen_report(book, word_count, character_count):
    list_dict = []

    print(f"--- Begin report of { book } ---")
    print(f"{word_count} words found in the document\n")
    
    for char in character_count:
        if char.isalpha():
            list_dict.append({"character": char, "count": character_count[char]})
    list_dict.sort(reverse=True, key=sort_on)

    for item in list_dict:
        print(f"The '{ item['character'] }' character was found { item['count'] } times")
    print("--- End report ---")




def main():        
    results = ""
    with open(book) as f:
        results = f.read()
    word_count = count_words(results)
    character_count = count_characters(results)
    gen_report(book, word_count, character_count)

main()