// Compile with "g++ binary_check.cpp canvas.cpp -lgmpxx -lgmp -o canvas"
// Make sure to "sudo apt install libgmp-dev"

#include "binary_check.h"
#include <algorithm>
#include <cmath>
#include <gmpxx.h>
#include <iostream>

const int BINARY_CHECK_TRIAL_COUNT = 1000;
mpf_class* factorialMemoize;
mpf_class** binaryCheckMemoize;

mpf_class factorial(int n) {
    if (n == 1) {
        return n;
    }
    if (factorialMemoize[n] == NULL) {
        factorialMemoize[n] = n * factorial(n - 1);
    }
    return factorialMemoize[n];
}

mpf_class combination(int n, int r) {
    if (r == 0 || n == r) {
        return 1;
    }
    
    return factorial(n) \
            / (factorial(r) * factorial(n - r));
}

mpf_class genTree(
        int k, int options, int numBranches, int oldScore, mpf_class oldAttempts, mpf_class oldProb, int depth) {
    if (numBranches == NULL) {
        numBranches = k + 1;
    }
    if (depth == options - 1) {
        numBranches = 1;
    }

    mpf_class EV = 0.0;
    for (int j = 0; j < numBranches; j++) { // `j` is the red number
        int incorrectBefore = k - oldScore; // `i` (except for attempt 1 on the tree)
        int newScore = k - j;
        mpf_class newAttempts;
        mpf_class newProb;
        if (depth == options - 1) {
            newProb = oldProb;
        } else {
            newProb = oldProb * combination(incorrectBefore, incorrectBefore - j) \
                    * pow((float) 1 / (options - depth), incorrectBefore - j) \
                    * pow((float) (options - depth - 1) / (options - depth), j);
        }

        // if we've reached an ending, calculate attempts * total prob and add to EV as before
        if (newScore == k) {
            newAttempts = oldAttempts + 1;
            EV += newAttempts * newProb;
            continue;
        }

        // binary check simulator (don't forget symmetry!)
        int a = std::min(newScore - oldScore, k - (newScore - oldScore));
        int b = k - oldScore;
        if (a == 0 || b == 1) {                               // if we don't need binary check
            newAttempts = oldAttempts + 1;
        } else {
            if (binaryCheckMemoize[b][a] == NULL) {
                if (a == 1 && (b & (b - 1) == 0) && b != 0) { // https://stackoverflow.com/a/57025941
                    binaryCheckMemoize[b][a] = log2(b);
                } else {
                    newAttempts = 0;
                    for (int i = 0; i < BINARY_CHECK_TRIAL_COUNT; i++) {
                        Node tree(a, b, NULL, NULL);
                        newAttempts += tree.runBinaryCheck();
                    }
                    binaryCheckMemoize[b][a] = newAttempts / BINARY_CHECK_TRIAL_COUNT;
                }
            }
            newAttempts = oldAttempts + 1 + binaryCheckMemoize[b][a];
        }

        // recursively call on sub-branches
        // `j + 1` to account for getting 0 more correct next attempt
        EV += genTree(k, options, j + 1, newScore, newAttempts, newProb, depth + 1);
    }

    return EV;
}

int main() {
    int kMin;
    int kMax;
    int options;
    std::cout << "k min (inclusive): ";
    std::cin >> kMin;
    std::cout << "k max (exclusive): ";
    std::cin >> kMax;
    std::cout << "number of options per question: ";
    std::cin >> options;

    factorialMemoize = (mpf_class*) malloc(kMax * sizeof(factorialMemoize[0])); // using `kMax` cause lazy
    for (int i = 0; i < kMax; i++) {
        // "conditional jump or move depends on uninitialized value" there are no memory errors in ba sing se
        // (i dont think im initializing `mpf_class`es right, because there's no memory issues if they're `double`s)
        factorialMemoize[i] = mpf_class(0.0);
    }
    binaryCheckMemoize = (mpf_class**) malloc(kMax * sizeof(binaryCheckMemoize[0]));
    for (int i = 0; i < kMax; i++) {
        binaryCheckMemoize[i] = (mpf_class*) malloc(kMax * sizeof(binaryCheckMemoize[0][0]));
        for (int j = 0; j < kMax; j++) {
            binaryCheckMemoize[i][j] = mpf_class(0.0);
        }
    }

    for (int k = kMin; k < kMax; k++) {
        std::cout << k << " " << genTree(k, options, NULL, 0, 0, 1.0, 0) / k << "\n";
    }

    // free
    for (int i = 0; i < kMax; i++) {
        free(binaryCheckMemoize[i]);
    }
    free(binaryCheckMemoize);
    free(factorialMemoize);
}
