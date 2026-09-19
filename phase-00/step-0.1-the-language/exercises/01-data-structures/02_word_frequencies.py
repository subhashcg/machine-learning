from collections import Counter

def word_frequencies(text):
    counter = {}
    for word in text.lower().split():
        if word in counter:
            counter[word] += 1
        else:
            counter[word] = 1
    return counter

def word_frequencies_counter(text):
    return Counter(text.lower().split())

if __name__ == "__main__":
    print(word_frequencies("my name is subhash and my son is Aditya"))
    print(word_frequencies_counter("my name is subhash and my son is Aditya"))