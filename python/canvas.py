import math
from binary_check import Node

min_k = int(input("k min (inclusive): "))
max_k = int(input("k max (exclusive): "))
options = int(input("number of options per question: "))
binary_check_trials = 1000
binary_check_memoize = [[0 for i in range(max_k)] for j in range(max_k)] # using max_k cause lazy

def gen_tree(k, options, num_branches=None, old_score=0, old_attempts=0, old_prob=1, depth=0):
    if num_branches is None:
        num_branches = k + 1
    if depth == options - 1:
        num_branches = 1
    
    EV = 0
    for j in range(num_branches):        # j is the red number
        incorrect_before = k - old_score # i (except for attempt 1 on the tree)
        new_score = k - j
        new_attempts = old_attempts
        if depth == options - 1:
            new_prob = old_prob
        else:
            new_attempts += 1            # remember that fourth attempts are overlapped and do not count
            new_prob = old_prob * math.comb(incorrect_before, incorrect_before - j) \
                    * math.pow(1 / (options - depth), incorrect_before - j) \
                    * math.pow((options - depth - 1) / (options - depth), j)
        
        # if we've reached an ending, calculate attempts * total prob and add to EV
        if new_score == k:
            EV += new_attempts * new_prob
            continue

        # binary check simulator (don't forget symmetry!)
        a = min(new_score - old_score, k - (new_score - old_score))
        b = k - old_score
        if a != 0 and b != 1:                                # if we need binary check
            if binary_check_memoize[b][a] == 0:
                if a == 1 and (b & (b - 1) == 0) and b != 0: # shortcut if single-target and b power of 2 (no rounding)
                                                             # https://stackoverflow.com/a/57025941
                    binary_check_memoize[b][a] = math.log2(b)
                else:
                    binary_check_attempts_total = 0
                    for _ in range(binary_check_trials):
                        tree = Node(a, b)
                        binary_check_attempts_total += tree.run_binary_check()
                    binary_check_memoize[b][a] = binary_check_attempts_total / binary_check_trials
            new_attempts += binary_check_memoize[b][a]

        # recursively call on sub-branches
        # num_branches = j + 1 to account for getting 0 more correct next attempt
        EV += gen_tree(k, options, j + 1, new_score, new_attempts, new_prob, depth + 1)

    return EV

# main
for k in range(min_k, max_k):
    print(k, gen_tree(k, options) / k)
