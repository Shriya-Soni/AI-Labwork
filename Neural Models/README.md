## README: Subjective Answers & Lab Report

### Task 1: Problem Specification

*   **Input Space ($\mathcal{X}$):** $\{0, 1\} \times \{0, 1\}$.
*   **Output Space ($\mathcal{Y}$):** $\{0, 1\}$.
*   **Labeled Examples:** $(0,0) \rightarrow 0$, $(0,1) \rightarrow 1$, $(1,0) \rightarrow 1$, $(1,1) \rightarrow 0$.
*   **Linear Separability:** A single straight decision boundary cannot separate the classes because the points form a cross (X) configuration. No single line can isolate the positive examples $(0,1)$ and $(1,0)$ from the negative examples $(0,0)$ and $(1,1)$.
*   **Linear Model Prediction:** If only a single affine transformation followed by a sigmoid output is trained, it will fail to learn the XOR pattern. The model will likely settle at predicting a probability of roughly $0.5$ for all points, acting as a random guess, or it will draw a line that gets at most two or three points correct.

### Task 2: Design the Intelligent Agent

*   **Necessity of Hidden Nonlinearity:** A stack of affine layers without nonlinear hidden activations collapses into a single affine map. Therefore, nonlinear behavior such as XOR cannot be represented by adding affine-only depth.
*   **Sigmoid and BCE Justification:** A sigmoid output maps any real-valued number into a valid probability between $0$ and $1$. For a binary output, a standard pairing is sigmoid plus binary cross-entropy, which naturally measures the divergence between the true binary labels and the predicted probabilities.
*   **Validation Criteria:** Successful learning is evidenced by (1) a final loss approaching zero, (2) all four predicted labels being thresholded correctly, and (3) gradient nonzero-ness during training to indicate active parameter updates.

### Task 4: Diagnostics & Backpropagation

*   **Part B (Backpropagation Check):** `parameter.grad` represents $\frac{\partial L}{\partial W^{(1)}}$, which is the partial derivative of the scalar loss with respect to each individual weight in the first layer. Because the objective function is computed as a mean loss over the four examples, the total gradient is mathematically the average of the individual example-wise gradients (due to the linearity of differentiation).
*   **Part C (Symmetry Experiment):** When all weights are initialized to zero, the identical hidden units compute the same output and receive the same gradient during backpropagation. Consequently, they undergo the exact same weight updates and remain identical throughout training, failing to learn distinct, useful features.
*   **Part D (Activation Experiment Interpretation):** Activation choice influences optimization: a sigmoid unit can contribute small derivatives (when saturated), while active ReLU units contribute a derivative of exactly 1. In early steps, the sigmoid gradient is smaller due to the smoothing nature of the curve, whereas ReLU has a higher Euclidean norm for active units. Tanh generally avoids the severe vanishing issues of sigmoid by keeping outputs centered around zero, leading to reliable convergence for this tiny dataset.

### Task 5: 3-Class Extension Predictions

1.  **Shape of Final Weight Matrix:** $3 \times 2$. There are 2 incoming features from the hidden layer and 3 output logits.
2.  **Logits per Example:** $3$.
3.  **Why Softmax Sums to One:** Softmax exponentiates each logit (making them strictly positive) and divides by the total sum of all exponentiated logits, naturally yielding a normalized probability distribution summing to 1.
4.  **Logit Gradient $p - y$:** For one-of-K classification, a standard pairing is softmax plus cross-entropy, whose logit gradient is mathematically formulated as $p - y$.
5.  **Shift Invariance (Optional):** Exponentiating large numbers causes floating-point overflow. Because $e^{x_i - c} / \sum e^{x_j - c} = e^{x_i}/ \sum e^{x_j}$, subtracting the maximum logit before exponentiating keeps the highest value at $e^0 = 1$, making implementations numerically stable without altering the probabilities.

### Reflection Questions

1.  **Depth vs. Nonlinearity:** The XOR experiment demonstrates that stacking linear layers simply results in another linear layer. Nonlinearity is the actual mechanism that warps the feature space, allowing a straight decision boundary in the final layer to solve what was a non-linear problem in the input space.
2.  **Learning Signal Evidence:** The fact that the model consistently converges to $4/4$ correct thresholded labels—while driving the loss toward zero—proves the gradient directed the weights toward an optimal solution configuration, rather than just bouncing around randomly.
3.  **Symmetry Failure:** Identical hidden units compute the same output and receive the same gradient. Without initial noise (random weight initialization) to break this symmetry, there is no mechanism for backpropagation to push the two units to compute different halves of the XOR problem.
4.  **Activation Impact:** Scientifically, deep products of Jacobian factors can shrink or grow gradients. Engineering-wise, this is observed by monitoring the gradient norm: ReLU and Tanh provided healthier, larger early gradients, whereas Sigmoid yielded smaller initial gradients, requiring more steps or a higher learning rate to escape initial plateaus.
5.  **Output and Loss Pairing:** The output activation shapes the model's raw numbers into a specific domain (e.g., probabilities), and the loss function must geometrically match that domain to penalize errors effectively. A mismatch (like using MSE for probabilities) leads to poor gradient landscapes.
6.  **LLM Collaboration:** The LLM improved productivity by instantly writing the PyTorch boilerplate for the training loop and network definitions. Human verification was essential for ensuring the correct interpretation of the symmetry failure and confirming the LLM didn't silently change the learning task to make it easier to solve.
7.  **Scaling Tests:** Checking the final loss and prediction metrics scales perfectly. However, printing or extracting exhaustive parameter gradients, or running exhaustive finite-difference gradient checks, becomes far too computationally expensive and unreadable at scale.