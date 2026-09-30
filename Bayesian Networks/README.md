# Bayesian Networks and Autoregressive Language Models - Lab Report

## Part I: From Probability to Language
**Question 1:** Why is this decomposition useful for generating text?
The autoregressive decomposition is useful because it allows an autoregressive language model to estimate these conditional probabilities and use them to predict the next word or token sequentially[cite: 5]. This factorisation applies the chain-rule to break down the complex joint probability into a sequence of simpler next-word predictions[cite: 5].

## Part II: A Bayesian Network for Text
**Question 2:** What independence assumption is being made by this network?
*   The first-order Markov language model makes the assumption that each word depends only on the immediately preceding word[cite: 5]. 
*   In probability notation, this assumption is expressed as calculating $P(X_t \vert{} X_{t-1})$ rather than relying on the entire history $P(X_t \vert{} X_1, ..., X_{t-1})$[cite: 5].

## Part IV: Constructing the Conditional Probability Table
**Question 3:** Construct the conditional probability distribution $P(next word \vert{} current word)$ for at least the following words:
Using the equation $P(w_j \vert{} w_i) = \frac{C(w_i, w_j)}{\sum_k C(w_i, w_k)}$[cite: 5] on the provided dataset:
*   **the**: cat (3/12), dog (3/12), mat (2/12), rug (2/12), park (2/12)
*   **cat**: sat (2/3), ran (1/3)
*   **dog**: sat (2/3), ran (1/3)
*   **sat**: on (4/4)
*   **ran**: to (2/2)
Zero-probability transitions include $P(dog \vert{} cat)$, $P(mat \vert{} sat)$, and any other word pairing not explicitly observed in the 6 training sentences.

## Part VI: Inspect the LLM-Generated Code
**Question 4:** Where in the program are the transition counts stored?
They are stored in a nested dictionary named `transitions` which counts occurrences between consecutive tokens.

**Question 5:** Where is $P(X_t \vert{} X_{t-1})$ computed?
It is computed in the loop that divides the individual word transition count by the total sum of outgoing transitions, directly implementing $P(w_j \vert{} w_i) = \frac{C(w_i, w_j)}{\sum_k C(w_i, w_k)}$[cite: 5].

**Question 6:** How does the program choose the next word?
*   In greedy generation mode, the program always chooses $arg \max_w P(w \vert{} w_{previous})$[cite: 5]. 
*   In sampling mode, the program generates text by repeatedly sampling from a conditional distribution[cite: 5]. 
*   The difference is that greedy always picks the highest-probability path (deterministic), while sampling draws proportionally to the probabilities, allowing for varied outputs.

**Question 7:** What happens if the program encounters a word for which no transition has been observed?
The program will halt or raise an error (like a `KeyError` in Python) because it cannot sample from an empty or non-existent conditional probability distribution.

## Part VII: Test the Probability Model
**Question 8:** If one of the totals is 0.87, what does this tell you about the implementation?
If a total is 0.87, it tells us that the implementation is mathematically incorrect. A correct probabilistic program must satisfy the property that for every current word $w$, $\sum_v P(v \vert{} w) = 1$[cite: 5]. 

## Part VIII: Predicting the Next Word
**Question 9:** Are the most probable predictions always the same as the words that you would personally expect? What does this tell you about the difference between a probability model and human linguistic expectations?
No. The most probable next word according to the model is simply $arg \max_w P(w \vert{} the)$[cite: 5] based strictly on the tiny 6-sentence dataset. A probability model strictly represents the statistical patterns of its training data, whereas human linguistic expectations draw on vast semantic understanding and real-world grammar.

## Part X: Deterministic vs Probabilistic Generation
**Question 10:** Compare the two sets of generated sentences. Which mode produces more variation? Why?
*   Mode B (Sampling) produces more variation.
*   Mode A (Greedy) generates the exact same sequence every time because it will always choose $arg \max_w P(w \vert{} w_{previous})$[cite: 5]. 
*   Sampling allows for variation because it samples from $P(w \vert{} w_{previous})$, allowing lower-probability words to be chosen occasionally[cite: 5].

## Part XI & XIII: Comparing the Two Models
**Question 11:** How does the second-order model differ from the first-order model?
1.  The graph structure changes to $X_{t-2} \rightarrow X_t \leftarrow X_{t-1}$[cite: 5].
2.  The conditional probability table estimates $P(X_t \vert{} X_{t-2}, X_{t-1})$ instead of $P(X_t \vert{} X_{t-1})$[cite: 5].
3.  The amount of context available for prediction increases to two prior words instead of just one.
4.  The amount of data needed increases significantly due to the exponentially larger number of possible word triples compared to pairs.

**Question 12:** Why does increasing the amount of context potentially improve prediction? Why can it simultaneously make the model harder to estimate from limited data?
Increasing context improves prediction by restricting the possible valid next words based on a longer history. However, it makes estimation harder from limited data because expanding to $P(X_t \vert{} X_{t-2}, X_{t-1})$ drastically increases the size of the conditional probability table, leading to data sparsity where many context combinations have zero observed counts.

## Part XV: Reflection on the Role of the LLM
**Question 13:** Why is Approach B preferable when constructing an intelligent system?
*   Approach B is preferable because the LLM is a tool for constructing the intelligent system, not a replacement for understanding the system[cite: 5]. 
*   Providing a behavioural specification forces the engineer to explicitly define the intended probabilistic model[cite: 5].
*   It ensures the developer understands the representation, tests probabilistic invariants, and properly distinguishes the theoretical model from its implementation[cite: 5].

## Final Question: What Did the Bayesian Network Add?
**Question 14:** What did thinking of the language model as a Bayesian network give you?
Thinking of the language model as a Bayesian network provided:
*   A representation of dependencies, clearly showing how each variable relies on previous ones[cite: 5].
*   A factorisation of the joint distribution, simplifying $P(X_1, ..., X_T)$ using the chain rule[cite: 5].
*   A way to reason about independence assumptions, such as assuming $P(X_t \vert{} X_1, ..., X_{t-1}) \approx P(X_t \vert{} X_{t-1})$ in a first-order Markov model[cite: 5].