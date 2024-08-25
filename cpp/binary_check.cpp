/**
 * Compile with `g++ binary_check.cpp -o binary_check`.
 */

#include "binary_check.h"
#include <iostream>
#include <random>
#include <unordered_set>

Node::Node(int a, int b, int rootVal, Node* parent) {
    this->a = a;
    this->b = b;
    if (rootVal == NULL) {
        rootVal = b;
    }
    this->rootVal = rootVal;
    this->parent = parent;

    this->left = NULL;
    this->right = NULL;
    this->crossed = false;
    this->correct = false;

    if (rootVal > 1) {
        int leftVal = (int) (rootVal / 2); // totally necessary cast
        int rightVal = rootVal - leftVal;
        this->left = new Node(a, b, leftVal, this);
        this->right = new Node(a, b, rightVal, this);
    } else if (rootVal == 1 && parent != NULL) {
        parent->leaves.push_back(this);
    }

    // sync leaves information all the way up to tree root
    if (parent != NULL) {
        parent->leaves.insert(parent->leaves.end(), this->leaves.begin(), this->leaves.end());
    }

    // if root, generate correct answers
    if (parent == NULL) {
        std::random_device r; // srand() by time did not seem to seed well, so here we are
        std::default_random_engine e1(r());
        std::uniform_int_distribution<int> rng(0, b - 1);

        std::unordered_set<int> answers;
        while (answers.size() < a) {
            answers.insert(rng(e1));
        }
        for (const int answer : answers) {
            this->leaves[answer]->correct = true;
        }
    }
}

Node::~Node() {
    if (this->left != NULL) {
        delete this->left;
    }
    if (this->right != NULL) {
        delete this->right;
    }
}

int Node::getScore() {
    int score = 0;
    for (const Node* leaf : this->leaves) {
        if (leaf->correct) {
            score++;
        }
    }
    return score;
}

void Node::traverse(int& attempts, int& remainingTargets) {
    // terminate recursion if we've found all
    if (remainingTargets == 0) {
        return;
    }

    // visit node and slaughter sibling
    if (!this->crossed) {
        attempts++;
        if (this->parent != NULL) {
            this->parent->right->crossed = true;
        }
    }

    // if leaf node; if no attempts += 1, then this is functionally a deduction
    if (this->rootVal == 1) {
        if (this->correct) {
            remainingTargets--;
        }
        return;
    }

    // if score is 0, skip entire subtree ("flip")
    if (this->getScore() == 0) {
        return;
    }

    // recursively check left and right children
    if (this->left != NULL) {
        this->left->traverse(attempts, remainingTargets);
        if (remainingTargets == 0) {
            return;
        }
    }
    if (this->right != NULL) {
        this->right->traverse(attempts, remainingTargets);
        if (remainingTargets == 0) {
            return;
        }
    }
}

int Node::runBinCheck() {
    int attempts = 0;
    int remainingTargets = this->a;

    // recursively check left and right children, and keep "global" values for these 2 values
    this->left->traverse(attempts, remainingTargets);
    this->right->traverse(attempts, remainingTargets);

    return attempts;
}

// int main() {
//     int TRIAL_COUNT = 10000;
//     int bMax = 10;
//     int** attempts = (int**) calloc(bMax, sizeof(attempts[0]));
//     for (int i = 0; i < bMax; i++) {
//         attempts[i] = (int*) calloc(bMax, sizeof(attempts[0][0]));
//     }
// 
//     for (int i = 0; i < TRIAL_COUNT; i++) {
//         for (int b = 0; b < bMax; b++) {
//             for (int a = 0; a < b; a++) {
//                 Node tree(a + 1, b + 1, NULL, NULL);
//                 attempts[b][a] += tree.runBinCheck();
//             }
//         }
//     }
// 
//     for (int b = 0; b < bMax; b++) {
//         for (int a = 0; a < b; a++) {
//             std::cout << a + 1 << " out of " << b + 1 << ": " << attempts[b][a] / double(TRIAL_COUNT) << " attempts\n";
//         }
//         std::cout << "\n";
//     }
// 
//     // free
//     for (int i = 0; i < bMax; i++) {
//         free(attempts[i]);
//     }
//     free(attempts);
// }
