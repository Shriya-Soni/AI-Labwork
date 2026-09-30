# AI-Labwork
# Shriya Soni, 2023B4AD0885G

A comprehensive repository containing Python implementations and lab reports for core Artificial Intelligence concepts. These exercises bridge the gap between AI Science (understanding representations and algorithms) and AI Engineering (implementing, testing, and validating LLM-assisted code).

## Repository Structure

*   **`01_Neural_Models/`**
    *   **Topics:** Neural Network Depth, Nonlinear Activations (ReLU, Tanh, Sigmoid), Backpropagation, Binary and Multiclass Classification.
    *   **Description:** Explores why hidden nonlinearities are required to solve the XOR problem. Includes PyTorch implementations demonstrating gradient behavior, weight initialization symmetries, and activation function impacts.

*   **`02_Agents/`**
    *   **Topics:** Goal-Based Agents, Breadth-First Search (BFS), Grid Navigation.
    *   **Description:** Implements a discrete, fully observable warehouse navigation agent that computes shortest, collision-free paths using uninformed search strategies.

*   **`03_Search/`**
    *   **Topics:** A* Search, Heuristics, Uniform Cost Search.
    *   **Description:** Compares A* against blind search (BFS) in complex warehouse routing. Investigates the impact of admissible (Manhattan) and inadmissible (Euclidean, Multiplied) heuristics on state expansion and path optimality.

*   **`04_Logical_Planning/`**
    *   **Topics:** Logical Reasoning, State-Space Planning, Action Preconditions and Effects.
    *   **Description:** Combines logical state transitions with BFS to construct valid action sequences (PickUp, Move, Drop). Includes optional Prolog scripts for independent logical verification of generated plans.

*   **`05_Bayesian_Networks/`**
    *   **Topics:** Autoregressive Language Models, Markov Assumptions, Conditional Probability Tables (CPTs).
    *   **Description:** Builds 1st-order and 2nd-order Markov models from scratch to generate text. Contrasts deterministic (greedy) and probabilistic (sampling) generation, demonstrating how modern language models factorize joint probabilities.

## Tech Stack & Requirements

*   **Language:** Python 3.x
*   **Libraries:** `torch`, `numpy`, built-in `collections` and `heapq`
*   **Optional:** SWI-Prolog (for Lab 04 logical verification)

## Execution Instructions

Each lab directory contains an executable Python script and a detailed markdown report (`README.md`). Navigate to the specific lab folder and run the script to view the algorithmic outputs, transition histories, or generated text.

```bash
# Example
cd 03_Search
python search_agent.py
