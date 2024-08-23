import math
from binary_check import Node

BIN_CHECK_TRIAL_COUNT = 1000
bin_check_memoize = [] # not actually needed because python but just for consistency with the C++ version

def gen_tree(k, option_count, branch_count=None, old_score=0, old_attempts=0, old_prob=1.0, depth=0):
    if branch_count is None:
        branch_count = k + 1
    if depth == option_count - 1:
        branch_count = 1
    
    ev = 0
    for j in range(branch_count):        # `j` is the red number
        incorrect_before = k - old_score # `i` (except for attempt 1 on the tree)
        new_score = k - j
        new_attempts = old_attempts
        if depth == option_count - 1:    # if on fourth non-extra attempt
            new_prob = old_prob
        else:
            new_attempts += 1            # remember that fourth attempts are overlapped and do not count
            new_prob = old_prob \
                    * math.comb(incorrect_before, incorrect_before - j) \
                    * math.pow(1 / (option_count - depth), incorrect_before - j) \
                    * math.pow((option_count - depth - 1) / (option_count - depth), j)
        
        # if we've reached an ending, calculate attempts * total prob and add to ev
        if new_score == k:
            ev += new_attempts * new_prob
            continue

        # binary check simulator (don't forget symmetry!)
        a = min(new_score - old_score, k - (new_score - old_score))
        b = k - old_score
        if a != 0 and b != 1: # if we need binary check
            if bin_check_memoize[b][a] is None:
                if a == 1 and (b & (b - 1) == 0) and b != 0:
                    # if single-target and `b` is a power of 2 (no rounding), take shortcut
                    # (https://stackoverflow.com/a/57025941)
                    bin_check_memoize[b][a] = math.log2(b)
                else:
                    bin_check_attempts_total = 0
                    for _ in range(BIN_CHECK_TRIAL_COUNT):
                        tree = Node(a, b)
                        bin_check_attempts_total += tree.run_bin_check()
                    bin_check_memoize[b][a] = bin_check_attempts_total / BIN_CHECK_TRIAL_COUNT
            new_attempts += bin_check_memoize[b][a]

        # recursively call on sub-branches
        # `j + 1` to account for getting 0 more correct next attempt
        ev += gen_tree(k, option_count, j + 1, new_score, new_attempts, new_prob, depth + 1)

    return ev

## Main
if __name__ == "__main__":
    min_k = int(input("k min (inclusive): "))
    max_k = int(input("k max (exclusive): "))
    option_count = int(input("number of option_count per question: "))
    bin_check_memoize = [[None for i in range(max_k)] for j in range(max_k)] # using `max_k` cause lazy

    for k in range(min_k, max_k):
        print(k, gen_tree(k, option_count) / k)
