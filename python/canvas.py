import math
from binary_check import Node

BINARY_CHECK_TRIAL_COUNT = 1000
binary_check_memoize = [] # not actually needed because python but just for consistency with the C++ version

def gen_tree(k, options, num_branches=None, old_score=0, old_attempts=0, old_prob=1, depth=0):
    if num_branches is None:
        num_branches = k + 1
    if depth == options - 1:
        num_branches = 1
    
    EV = 0
    for j in range(num_branches):           # `j` is the red number
        incorrect_before = k - old_score    # `i` (except for attempt 1 on the tree)
        new_score = k - j
        if depth == options - 1:
            new_prob = old_prob
        else:
            new_prob = old_prob * math.comb(incorrect_before, incorrect_before - j) \
                    * math.pow(1 / (options - depth), incorrect_before - j) \
                    * math.pow((options - depth - 1) / (options - depth), j)
        
        # if we've reached an ending, calculate attempts * total prob and add to EV as before
        if new_score == k:
            new_attempts = old_attempts + 1
            EV += new_attempts * new_prob
            continue

        # binary check simulator (don't forget symmetry!)
        a = min(new_score - old_score, k - (new_score - old_score))
        b = k - old_score
        if a == 0 or b == 1:                                 # if we don't need binary check
            new_attempts = old_attempts + 1
        else:
            if binary_check_memoize[b][a] == 0:
                if a == 1 and (b & (b - 1) == 0) and b != 0: # https://stackoverflow.com/a/57025941
                    binary_check_memoize[b][a] = math.log2(b)
                else:
                    new_attempts = 0
                    for _ in range(BINARY_CHECK_TRIAL_COUNT):
                        tree = Node(a, b)
                        new_attempts += tree.run_binary_check()
                    binary_check_memoize[b][a] = new_attempts / BINARY_CHECK_TRIAL_COUNT
            new_attempts = old_attempts + 1 + binary_check_memoize[b][a]

        # recursively call on sub-branches
        # `j + 1` to account for getting 0 more correct next attempt
        EV += gen_tree(k, options, j + 1, new_score, new_attempts, new_prob, depth + 1)

    return EV

# main
if __name__ == "__main__":
    min_k = int(input("k min (inclusive): "))
    max_k = int(input("k max (exclusive): "))
    options = int(input("number of options per question: "))
    binary_check_memoize = [[0 for i in range(max_k)] for j in range(max_k)] # using `max_k` cause lazy
    for k in range(min_k, max_k):
        print(k, gen_tree(k, options) / k)
