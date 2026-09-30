class Action:
    def __init__(self, name, pos_pre=None, neg_pre=None, pos_eff=None, neg_eff=None):
        self.name = name
        self.pos_pre = pos_pre if pos_pre else set()
        self.neg_pre = neg_pre if neg_pre else set()
        self.pos_eff = pos_eff if pos_eff else set()
        self.neg_eff = neg_eff if neg_eff else set()

    def is_applicable(self, state):
        # Action is applicable if ALL positive preconditions are in the state
        # AND NO negative preconditions are in the state
        return self.pos_pre.issubset(state) and not self.neg_pre.intersection(state)

    def apply(self, state):
        # 1. Remove negative effects
        new_state = state.difference(self.neg_eff)
        # 2. Add positive effects
        new_state = new_state.union(self.pos_eff)
        return frozenset(new_state)

def bfs_planner(initial_state, goal_state, actions):
    """
    Finds the shortest sequence of actions to transition from initial_state to goal_state.
    Returns (plan_action_names, state_history) or None if no plan exists.
    """
    # Frontier stores tuples of (current_state, plan_so_far, state_history)
    frontier = [(frozenset(initial_state), [], [frozenset(initial_state)])]
    visited = {frozenset(initial_state)}

    while frontier:
        current_state, plan, history = frontier.pop(0)

        # Check if the goal is satisfied
        if goal_state.issubset(current_state):
            return plan, history

        # Search over alternatives: Generate successor states
        for action in actions:
            if action.is_applicable(current_state):
                successor_state = action.apply(current_state)
                
                if successor_state not in visited:
                    visited.add(successor_state)
                    frontier.append(
                        (successor_state, plan + [action.name], history + [successor_state])
                    )
    
    return None, None # No plan found

# ==========================================
# WAREHOUSE DOMAIN DEFINITION
# ==========================================

# Actions definition
actions = [
    Action("Move(A, B)", pos_pre={"At(Robot, A)"}, pos_eff={"At(Robot, B)"}, neg_eff={"At(Robot, A)"}),
    Action("Move(B, A)", pos_pre={"At(Robot, B)"}, pos_eff={"At(Robot, A)"}, neg_eff={"At(Robot, B)"}),
    Action("Move(B, C)", pos_pre={"At(Robot, B)"}, pos_eff={"At(Robot, C)"}, neg_eff={"At(Robot, B)"}),
    Action("Move(C, B)", pos_pre={"At(Robot, C)"}, pos_eff={"At(Robot, B)"}, neg_eff={"At(Robot, C)"}),
    
    Action("PickUp(Package, A)", pos_pre={"At(Robot, A)", "At(Package, A)"}, pos_eff={"Holding(Package)"}, neg_eff={"At(Package, A)"}),
    Action("PickUp(Package, B)", pos_pre={"At(Robot, B)", "At(Package, B)"}, pos_eff={"Holding(Package)"}, neg_eff={"At(Package, B)"}),
    Action("PickUp(Package, C)", pos_pre={"At(Robot, C)", "At(Package, C)"}, pos_eff={"Holding(Package)"}, neg_eff={"At(Package, C)"}),
    
    Action("Drop(Package, A)", pos_pre={"At(Robot, A)", "Holding(Package)"}, pos_eff={"At(Package, A)"}, neg_eff={"Holding(Package)"}),
    Action("Drop(Package, B)", pos_pre={"At(Robot, B)", "Holding(Package)"}, pos_eff={"At(Package, B)"}, neg_eff={"Holding(Package)"}),
    Action("Drop(Package, C)", pos_pre={"At(Robot, C)", "Holding(Package)"}, pos_eff={"At(Package, C)"}, neg_eff={"Holding(Package)"})
]

# ==========================================
# TESTING SCRIPT
# ==========================================
if __name__ == "__main__":
    print("--- Test A: Solvable Problem ---")
    initial_A = {"At(Robot, A)", "At(Package, A)"}
    goal_A = {"At(Package, C)"}
    plan_A, history_A = bfs_planner(initial_A, goal_A, actions)
    print(f"Goal: {goal_A}")
    if plan_A is not None:
        print(f"Plan found: {plan_A}")
        for i, s in enumerate(history_A):
            print(f"S_{i}: {set(s)}")
    else:
        print("No plan found.")

    print("\n--- Test B: Impossible Problem ---")
    # Remove PickUp actions to make it impossible
    actions_no_pickup = [a for a in actions if not a.name.startswith("PickUp")]
    plan_B, history_B = bfs_planner(initial_A, goal_A, actions_no_pickup)
    print(f"Goal: {goal_A}")
    if plan_B is not None:
        print(f"Plan found: {plan_B}")
    else:
        print("No plan found.")

    print("\n--- Test C: Irrelevant Actions ---")
    # Goal is package at C, robot starts at A, package at A
    # The planner should not stop just because the robot moves to C.
    plan_C, _ = bfs_planner(initial_A, goal_A, actions)
    print("If irrelevant actions trick the planner, it might just output ['Move(A, B)', 'Move(B, C)'].")
    print(f"Actual plan found: {plan_C}")
    valid = "Drop(Package, C)" in plan_C
    print(f"Is plan valid (did it actually drop the package)? {valid}")