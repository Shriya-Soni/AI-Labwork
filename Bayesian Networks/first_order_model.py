# first_order_model.py
import random
from collections import defaultdict

# Part III: Build a Small Language Dataset
corpus = [
    "the cat sat on the mat",
    "the cat sat on the rug",
    "the dog sat on the mat",
    "the dog ran to the park",
    "the cat ran to the park",
    "the dog sat on the rug"
]

def tokenize(corpus):
    tokenized = []
    for sentence in corpus:
        tokens = ["<START>"] + sentence.lower().split() + ["<END>"]
        tokenized.append(tokens)
    return tokenized

def build_first_order_model(tokenized_corpus):
    # Count transitions
    transitions = defaultdict(lambda: defaultdict(int))
    for sentence in tokenized_corpus:
        for i in range(len(sentence) - 1):
            current_word = sentence[i]
            next_word = sentence[i+1]
            transitions[current_word][next_word] += 1

    # Construct conditional probability table P(X_t | X_{t-1})
    cpt = defaultdict(dict)
    for current_word, next_words in transitions.items():
        total_transitions = sum(next_words.values())
        for next_word, count in next_words.items():
            cpt[current_word][next_word] = count / total_transitions
            
    return cpt

def test_probabilities(cpt):
    # Part VII: Test the Probability Model
    print("--- Probability Normalisation Test ---")
    for word, next_words in cpt.items():
        total = sum(next_words.values())
        print(f"{word}: {total:.4f}")
    print("--------------------------------------\n")

def get_most_probable_next(cpt, current_word):
    if current_word not in cpt:
        return None
    return max(cpt[current_word], key=cpt[current_word].get)

def generate_sentence(cpt, mode="sampling"):
    current_word = "<START>"
    sentence = []
    
    while True:
        if current_word not in cpt:
            break
            
        if mode == "greedy":
            next_word = get_most_probable_next(cpt, current_word)
        else: # sampling
            next_words = list(cpt[current_word].keys())
            probabilities = list(cpt[current_word].values())
            next_word = random.choices(next_words, weights=probabilities, k=1)[0]
            
        if next_word == "<END>":
            break
            
        sentence.append(next_word)
        current_word = next_word
        
    return " ".join(sentence)

if __name__ == "__main__":
    tokenized = tokenize(corpus)
    cpt_1st_order = build_first_order_model(tokenized)
    
    test_probabilities(cpt_1st_order)
    
    print("--- Most Probable Next Words ---")
    for w in ["the", "cat", "dog", "sat", "ran"]:
        print(f"P(w | {w}) -> argmax: {get_most_probable_next(cpt_1st_order, w)}")
        
    print("\n--- Generation: Greedy ---")
    for i in range(5):
        print(generate_sentence(cpt_1st_order, mode="greedy"))
        
    print("\n--- Generation: Sampling ---")
    for i in range(5):
        print(generate_sentence(cpt_1st_order, mode="sampling"))