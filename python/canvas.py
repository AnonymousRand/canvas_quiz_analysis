import math
from binary_check import Node

BIN_CHECK_TRIAL_COUNT = 1000
bin_check_memoize = [] # not actually needed because python; just for consistency with the C++ version

def gen_tree(k, option_count, branch_count=None, score_old=0, attempt_count_old=0, prob_old=1.0, depth=0):
    if branch_count is None:
        branch_count = k + 1
    if depth == option_count - 1:
        branch_count = 1
    
    ev = 0
    for j in range(branch_count):        # `j` is the red number
        incorrect_before = k - score_old # `i` (except for attempt 1 on the tree)
        score_new = k - j
        attempt_count_new = attempt_count_old
        if depth == option_count - 1:    # if on fourth non-extra attempt
            prob_new = prob_old
        else:
            attempt_count_new += 1       # remember that fourth attempts are overlapped and do not count
            prob_new = prob_old \
                    * math.comb(incorrect_before, incorrect_before - j) \
                    * math.pow(1 / (option_count - depth), incorrect_before - j) \
                    * math.pow((option_count - depth - 1) / (option_count - depth), j)
        
        # if we've reached an ending, calculate attempts * total prob and add to ev
        if score_new == k:
            ev += attempt_count_new * prob_new
            continue

        # binary check simulator (don't forget symmetry!)
        a = min(score_new - score_old, k - (score_new - score_old))
        b = k - score_old
        if a != 0 and b != 1: # if we need binary check
            if bin_check_memoize[b][a] is None:
                if a == 1 and (b & (b - 1) == 0) and b != 0:
                    # if single-target and `b` is a power of 2 (no rounding), take shortcut
                    # (https://stackoverflow.com/a/57025941)
                    bin_check_memoize[b][a] = math.log2(b)
                else:
                    bin_check_attempt_count_total = 0
                    for _ in range(BIN_CHECK_TRIAL_COUNT):
                        tree = Node(a, b)
                        bin_check_attempt_count_total += tree.run_bin_check()
                    bin_check_memoize[b][a] = bin_check_attempt_count_total / BIN_CHECK_TRIAL_COUNT
            attempt_count_new += bin_check_memoize[b][a]

        # recursively call on sub-branches
        # `j + 1` to account for getting 0 more correct next attempt
        ev += gen_tree(k, option_count, j + 1, score_new, attempt_count_new, prob_new, depth + 1)

    return ev

if __name__ == "__main__":
    min_k = int(input("k min (inclusive): "))
    max_k = int(input("k max (exclusive): "))
    option_count = int(input("number of options per question: "))
    bin_check_memoize = [[None for i in range(max_k)] for j in range(max_k)] # using `max_k` cause lazy

    for k in range(min_k, max_k):
        print(k, gen_tree(k, option_count) / k)
