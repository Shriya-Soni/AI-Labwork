% Facts defining the warehouse connectivity
connected(a,b).
connected(b,a).
connected(b,c).
connected(c,b).

% Rule defining valid movement
can_move(X,Y) :- connected(X,Y).
valid_move(X,Y) :- connected(X,Y).

% Task 8: Logical Reasoning Facts and Rules
wet_road.
slippery :- wet_road.
reduce_speed :- slippery.