// Compile with "g++ binary_check.cpp canvas.cpp -lgmpxx -lgmp -o canvas"
// Make sure to "sudo apt install libgmp-dev"

#include "binary_check.h"
#include <algorithm>
#include <cmath>
#include <iostream>
#include <gmpxx.h>

mpf_class factorial(int n, mpf_class* factorialMemoize) {
    if (n == 1) {
        return n;
    }
    if (factorialMemoize[n] == NULL) {
        factorialMemoize[n] = n * factorial(n - 1, factorialMemoize);
    }
    return factorialMemoize[n];
}

mpf_class combination(int n, int r, mpf_class* factorialMemoize) {
    if (r == 0 || n == r) {
        return 1;
    }
    
    return factorial(n, factorialMemoize) \
            / (factorial(r, factorialMemoize) * factorial(n - r, factorialMemoize));
}

mpf_class genTree(int k, int numBranches, int oldScore, mpf_class oldAttempts, mpf_class oldProb, int depth,
        int binaryCheckTrials, mpf_class* factorialMemoize, mpf_class** binaryCheckMemoize) {
    if (numBranches == NULL) {
        numBranches = k + 1;
    }
    if (depth == 3) {
        numBranches = 1;
    }

    mpf_class EV = 0.0;
    for (int j = 0; j < numBranches; j++) { // j is the red numberpc
        int incorrectBefore = k - oldScore; // i (except for attempt 1 on the tree)
        int newScore = k - j;
        mpf_class newAttempts;
        mpf_class newProb;
        if (depth == 3) {
            newProb = oldProb;
        } else {
            newProb = oldProb * combination(incorrectBefore, incorrectBefore - j, factorialMemoize) \
                    * pow((float) 1 / (4 - depth), incorrectBefore - j) \
                    * pow((float) (4 - depth - 1) / (4 - depth), j);
        }

        // if we've reached an ending, calculate attempts * total prob and add to EV as before
        if (newScore == k) {
            newAttempts = oldAttempts + 1;
            EV += newAttempts * newProb;
            continue;
        }

        // binary check approximator (don't forget symmetry!)
        int a = std::min(newScore - oldScore, k - (newScore - oldScore));
        int b = k - oldScore;
        if (a == 0 || b < 2) {                                // if we don't need binary check
            newAttempts = oldAttempts + 1;
        } else {
            if (binaryCheckMemoize[b][a] == NULL) {
                if (a == 1 && (b & (b - 1) == 0) && b != 0) { // https://stackoverflow.com/a/57025941
                    binaryCheckMemoize[b][a] = log2(b);
                } else {
                    newAttempts = 0;
                    for (int i = 0; i < binaryCheckTrials; i++) {
                        Node tree(a, b, NULL, NULL);
                        newAttempts += tree.runBinaryCheck();
                    }
                    binaryCheckMemoize[b][a] = newAttempts / binaryCheckTrials;
                }
            }
            newAttempts = oldAttempts + 1 + binaryCheckMemoize[b][a];
        }

        // recursively call on sub-branches
        // num_branches = j + 1 to account for getting 0 more correct next attempt
        EV += genTree(k, j + 1, newScore, newAttempts, newProb, depth + 1,
                binaryCheckTrials, factorialMemoize, binaryCheckMemoize);
    }

    return EV;
}

int main() {
    int kMin;
    int kMax;
    int binaryCheckTrials = 1000;
    std::cout << "k min (inclusive): ";
    std::cin >> kMin;
    std::cout << "k max (exclusive): ";
    std::cin >> kMax;

    mpf_class* factorialMemoize = (mpf_class*) malloc(kMax * sizeof(factorialMemoize[0])); // using kMax cause lazy
    for (int i = 0; i < kMax; i++) {
        // "conditional jump or move depends on uninitialized value" there are no memory errors in ba sing se
        // (i dont think im initializing `mpf_class`es right, because there's no memory issues if they're `double`s)
        factorialMemoize[i] = mpf_class(0.0);
    }
    mpf_class** binaryCheckMemoize = (mpf_class**) malloc(kMax * sizeof(binaryCheckMemoize[0]));
    for (int i = 0; i < kMax; i++) {
        binaryCheckMemoize[i] = (mpf_class*) malloc(kMax * sizeof(binaryCheckMemoize[0][0]));
        for (int j = 0; j < kMax; j++) {
            binaryCheckMemoize[i][j] = mpf_class(0.0);
        }
    }

    for (int k = kMin; k < kMax; k++) {
        std::cout << k << " " \
                << genTree(k, NULL, 0, 0, 1.0, 0, binaryCheckTrials, factorialMemoize, binaryCheckMemoize) / k \
                << "\n";
    }

    // free
    for (int i = 0; i < kMax; i++) {
        free(binaryCheckMemoize[i]);
    }
    free(binaryCheckMemoize);
    free(factorialMemoize);
}
