import math
from binary_check import Node


BIN_CHECK_TRIAL_COUNT = 1000
bin_check_memoize = []


def gen_tree(k, option_count, branch_count=None, old_score=0, old_attempt_count=0, old_prob=1.0, depth=0):
    if branch_count is None:
        branch_count = k + 1
    if depth == option_count - 1:
        branch_count = 1
    
    ev = 0
    for j in range(branch_count):        # `j` is the red number
        incorrect_before = k - old_score # `i` (except for attempt 1 on the tree)
        new_score = k - j
        new_attempt_count = old_attempt_count
        if depth == option_count - 1:
            # if on fourth non-extra attempt
            new_prob = old_prob
        else:
            new_attempt_count += 1       # remember that fourth attempts are overlapped and do not count
            new_prob = old_prob \
                    * math.comb(incorrect_before, incorrect_before - j) \
                    * math.pow(1 / (option_count - depth), incorrect_before - j) \
                    * math.pow((option_count - depth - 1) / (option_count - depth), j)
        
        # if we've reached an ending, calculate attempts * total prob and add to ev
        if new_score == k:
            ev += new_attempt_count * new_prob
            continue

        # binary check simulator (don't forget symmetry!)
        a = min(new_score - old_score, k - (new_score - old_score))
        b = k - old_score
        # if we need binary check
        if a != 0 and b != 1:
            if bin_check_memoize[a][b] is None:
                if a == 1 and (b & (b - 1) == 0) and b != 0:
                    # if single-target and `b` is a power of 2 (no rounding), take shortcut
                    # (https://stackoverflow.com/a/57025941)
                    bin_check_memoize[a][b] = math.log2(b)
                else:
                    bin_check_total_attempt_count = 0
                    for _ in range(BIN_CHECK_TRIAL_COUNT):
                        tree = Node(a, b)
                        bin_check_total_attempt_count += tree.run_bin_check()
                    bin_check_memoize[a][b] = bin_check_total_attempt_count / BIN_CHECK_TRIAL_COUNT
            new_attempt_count += bin_check_memoize[a][b]

        # recursively call on sub-branches
        # `j + 1` to account for getting 0 more correct next attempt
        ev += gen_tree(k, option_count, j + 1, new_score, new_attempt_count, new_prob, depth + 1)

    return ev


if __name__ == "__main__":
    min_k = int(input("k min (inclusive): "))
    max_k = int(input("k max (exclusive): "))
    option_count = int(input("number of options per question: "))
    bin_check_memoize = [[None for i in range(max_k)] for j in range(max_k)] # using `max_k` cause lazy

    for k in range(min_k, max_k):
        print(k, gen_tree(k, option_count) / k)
