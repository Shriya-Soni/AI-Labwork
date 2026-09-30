## README: Logical Reasoning for Planning

### Task 0: Understand the Planning Problem

**(a) What is the initial state I?**
$I = \{At(Robot, A), At(Package, A)\}$[cite: 4].

**(b) What is the goal G?**
$G = \{At(Package, C)\}$[cite: 4].

**(c) List the actions available to the robot.**
The robot can `Move` between connected locations (e.g., A to B, B to C), `PickUp` the package when both are at the same location, and `Drop` the package at its current location[cite: 4].

**(d) For each action, identify its preconditions and effects.**
*   **Move(A, B):**
    *   Preconditions: $At(Robot, A)$[cite: 4]
    *   Effects: $-At(Robot, A)$, $At(Robot, B)$[cite: 4]
*   **PickUp(Package, A):**
    *   Preconditions: $At(Robot, A)$, $At(Package, A)$[cite: 4]
    *   Effects: $-At(Package, A)$, $Holding(Package)$[cite: 4]
*   **Drop(Package, C):**
    *   Preconditions: $At(Robot, C)$, $Holding(Package)$[cite: 4]
    *   Effects: $-Holding(Package)$, $At(Package, C)$[cite: 4]

**Are the actions initially applicable?**
*   `PickUp(Package, A)` **IS** applicable because its preconditions ($At(Robot, A)$ and $At(Package, A)$) are both satisfied in the initial state $I$.
*   `Drop(Package, C)` **IS NOT** applicable because its preconditions ($At(Robot, C)$ and $Holding(Package)$) are not present in the initial state $I$.

### Task 1: Construct a Plan by Hand

| State | Facts |
| :--- | :--- |
| $S_0$ | $At(Robot, A)$, $At(Package, A)$ |
| $S_1$ (after `PickUp(Package, A)`) | $At(Robot, A)$, $Holding(Package)$ |
| $S_2$ (after `Move(A, B)`) | $At(Robot, B)$, $Holding(Package)$ |
| $S_3$ (after `Move(B, C)`) | $At(Robot, C)$, $Holding(Package)$ |
| $S_4$ (after `Drop(Package, C)`) | $At(Robot, C)$, $At(Package, C)$ |

*This sequence results in a state $S_4$ where $S_4 \models G$.*

### Task 4: Logic and Search

**Where each is used:**
*   **Logical reasoning** determines whether $S \models Preconditions(a)$[cite: 4] to filter applicable actions, and mathematically calculates the successor state by applying positive and negative effects.
*   **Search** explores alternative valid sequences (e.g., using a BFS queue) to find the shortest path of logical transitions that leads to the goal.

**Flowchart Completion:**
Current state $\rightarrow$ Check action preconditions $\rightarrow$ **Applicable?** $\rightarrow$ Generate successor state $\rightarrow$ Search over alternatives $\rightarrow$ Goal?

### Task 5: LLM Verification vs. Independent Execution

**(a) or (b)?** You should trust **(b) the independently executed state transitions** more.
An LLM generates natural language explanations based on probabilistic word association; it might output a plausible-sounding hallucination where it falsely claims a precondition is met. Independent execution relies on deterministic Boolean logic, proving mathematically whether a state transition is valid or invalid. A generated explanation is not the same as an independent verification[cite: 4].

### Task 6 & 7: Prolog as a Logical Verifier (Optional)

**(a) Why does Prolog return true for can_move(a,b)?**
Because `connected(a,b)` is explicitly defined as a fact in the knowledge base, satisfying the rule.

**(b) Why does it not establish can_move(a,c)?**
Because there is no fact `connected(a,c)` defined, so the inference engine cannot satisfy the right side of the rule.

**(c) Relationship between Prolog and Logical Implication:**
The Prolog rule `can_move(X,Y) :- connected(X,Y).` perfectly mirrors the logical implication $Connected(X,Y) \rightarrow CanMove(X,Y)$[cite: 4].

**Task 7 Challenge:** 
Querying `?- valid_move(a,c).` returns `false` because the action proposed by the Python planner is not logically supported by the warehouse knowledge base. This demonstrates using Prolog as an independent verifier for a generated candidate action.

### Task 8: Connect Prolog to Logical Reasoning

**Why the query succeeds:**
Prolog searches backward from the query `?- reduce_speed.`. It finds the rule `reduce_speed :- slippery.` meaning it must now prove `slippery`. It finds the rule `slippery :- wet_road.` meaning it must now prove `wet_road`. It finds `wet_road.` as an established fact, concluding the chain as true.

**Logical Sequence:**
$Wet\_Road \rightarrow Slippery \rightarrow Reduce\_Speed \rightarrow Conclusion$.

### 5. Reflection Questions

1.  **Why specify preconditions/effects first?** It anchors the LLM to a strict logical framework, preventing it from hallucinating arbitrary state transitions or "magic" actions.
2.  **Error example:** The robot might try to execute `Drop(Package, C)` while it is still at Location A, or it might try to `PickUp` a package it is already holding.
3.  **"Looks reasonable" vs Valid:** A generated plan might look semantically correct to a human (e.g., "Move A to B, Move B to C, Drop Package") but fail logically if the crucial "PickUp" step was omitted.
4.  **LLM Contribution:** The LLM provided the boilerplate Python engineering (classes, sets, BFS queue logic) needed to execute the search algorithm.
5.  **Independent Verification:** I had to verify that the final plan actually achieved the specific goal state through mathematically sound logical state updates, rather than just trusting the LLM's printout.
6.  **Where is logic used?** In the `is_applicable` and `apply` methods, where set operations verify preconditions and update the state facts.
7.  **Relation to Search:** Planning *is* a search problem where the "graph nodes" are discrete logical states of the world, and the "edges" are the logically applicable actions that transition between them.