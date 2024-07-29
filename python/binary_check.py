import math
import random

class Node:
    def __init__(self, a, b, root_val=None, parent=None):
        self.a = a
        self.b = b
        if root_val is None:
            root_val = b
        self.root_val = root_val
        self.parent = parent

        self.left = None
        self.right = None
        self.leaves = []
        self.crossed = False
        self.correct = False

        if root_val > 1:
            left_val = root_val // 2
            right_val = root_val - left_val
            self.left = Node(a, b, left_val, self)
            self.right = Node(a, b, right_val, self)
        elif root_val == 1 and parent is not None:
            parent.leaves.append(self)

        ## Sync leaves information all the way up to tree root
        if parent is not None:
            parent.leaves += self.leaves

        ## Root: generate correct answers
        if parent is None:
            answers = random.sample(range(b), a)
            for i in answers:
                self.leaves[i].correct = True

    def get_score(self):
        score = 0
        for leaf in self.leaves:
            if leaf.correct:
                score += 1
        return score

    def traverse(self, attempts, remaining_targets):
        ## Terminate recursion if we've found all
        if remaining_targets == 0:
            return attempts, 0

        ## Visit node and poison sibling like an ancient Chinese prince
        if not self.crossed:
            attempts += 1
            if self.parent is not None:
                self.parent.right.crossed = True

        ## If leaf node; if no attempts += 1, then this is functionally a deduction
        if self.root_val == 1:
            if self.correct:
                return attempts, remaining_targets - 1
            else:
                return attempts, remaining_targets

        ## If score is 0, skip entire subtree ("flip")
        if self.get_score() == 0:
            return attempts, remaining_targets

        ## Recursively check left and right children
        if self.left is not None:
            attempts, remaining_targets = self.left.traverse(attempts, remaining_targets)
            if remaining_targets == 0:
                return attempts, remaining_targets
        if self.right is not None:
            attempts, remaining_targets = self.right.traverse(attempts, remaining_targets)
            if remaining_targets == 0:
                return attempts, remaining_targets

        return attempts, remaining_targets

    def run_binary_check(self):
        attempts = 0
        remaining_targets = self.a

        ## Recursively check left and right children, and keep "global" values for these 2 values
        attempts, remaining_targets = self.left.traverse(attempts, remaining_targets)
        attempts, remaining_targets = self.right.traverse(attempts, remaining_targets)

        return attempts

## Main
if __name__ == "__main__":
    trials = 10000
    max_b = 10
    attempts = [[0 for i in range(max_b)] for j in range(max_b)]

    for _ in range(trials):
        for b in range(max_b):
            for a in range(b):
                tree = Node(a + 1, b + 1)
                attempts[b][a] += tree.run_binary_check()

    for b in range(max_b):
        for a in range(b):
            print(f"{a + 1} out of {b + 1}: {attempts[b][a] / trials} attempts")
        print()
