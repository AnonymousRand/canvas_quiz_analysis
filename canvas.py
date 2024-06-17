import math
from binary_check import Node

max_k = 200
binary_check_trials = 10000
binary_check_memoize = [[-1 for i in range(max_k)] for j in range(max_k)] # using max_k cause lazy

def gen_tree(k, num_branches=None, old_score=0, old_attempts=0, old_prob=1, depth=0):
    if num_branches is None:
        num_branches = k + 1
    if depth == 3:
        num_branches = 1
    
    EV = 0
    for j in range(num_branches):           # j is the red number
        incorrect_before = k - old_score    # i (except for attempt 1 on the tree, which has incorrect_after for i)
        new_score = k - j
        if depth == 3:
            new_prob = old_prob
        else:
            new_prob = old_prob * math.comb(incorrect_before, incorrect_before - j) \
                    * math.pow(1 / (4 - depth), incorrect_before - j) \
                    * math.pow((4 - depth - 1) / (4 - depth), j)
        
        # if we've reached an ending, calculate attempts * total prob and add to expected value as before
        if new_score == k:
            new_attempts = old_attempts + 1
            EV += new_attempts * new_prob
            continue

        # binary check approximator (don't forget symmetry!)
        a = min(new_score - old_score, k - (new_score - old_score))
        b = k - old_score
        # optimize program speed
        if a == 0 or b < 2:                             # if we don't need binary check; avoids error too
            new_attempts = old_attempts + 1
        elif a == 1 and (b & (b - 1) == 0) and b != 0:  # from https://stackoverflow.com/a/57025941
            new_attempts = old_attempts + 1 + math.log2(k - old_score)
        else:
            if binary_check_memoize[b][a] == -1:
                new_attempts = 0
                for _ in range(binary_check_trials):
                    tree = Node(a, b)
                    new_attempts += tree.run_binary_check()
                binary_check_memoize[b][a] = new_attempts / binary_check_trials
            new_attempts = old_attempts + 1 + binary_check_memoize[b][a]

        # recursively call on sub-branches
        # num_branches = j + 1 to account for getting 0 more correct next attempt
        EV += gen_tree(k, j + 1, new_score, new_attempts, new_prob, depth + 1)

    return EV

# main
for k in range(1, max_k):
    print(k, gen_tree(k) / k)
