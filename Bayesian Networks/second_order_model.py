# second_order_model.py
import random
from collections import defaultdict

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
        tokens = ["<START>", "<START>"] + sentence.lower().split() + ["<END>"]
        tokenized.append(tokens)
    return tokenized

def build_second_order_model(tokenized_corpus):
    # Count transitions for triples
    transitions = defaultdict(lambda: defaultdict(int))
    for sentence in tokenized_corpus:
        for i in range(len(sentence) - 2):
            context = (sentence[i], sentence[i+1])
            next_word = sentence[i+2]
            transitions[context][next_word] += 1

    # Construct CPT P(X_t | X_{t-2}, X_{t-1})
    cpt = defaultdict(dict)
    for context, next_words in transitions.items():
        total = sum(next_words.values())
        for next_word, count in next_words.items():
            cpt[context][next_word] = count / total
            
    return cpt

def generate_sentence_2nd_order(cpt):
    context = ("<START>", "<START>")
    sentence = []
    
    while True:
        if context not in cpt:
            break
            
        next_words = list(cpt[context].keys())
        probabilities = list(cpt[context].values())
        next_word = random.choices(next_words, weights=probabilities, k=1)[0]
        
        if next_word == "<END>":
            break
            
        sentence.append(next_word)
        context = (context[1], next_word)
        
    return " ".join(sentence)

if __name__ == "__main__":
    tokenized = tokenize(corpus)
    cpt_2nd_order = build_second_order_model(tokenized)
    
    print("--- Second Order Generation (Sampling) ---")
    for i in range(5):
        print(generate_sentence_2nd_order(cpt_2nd_order))