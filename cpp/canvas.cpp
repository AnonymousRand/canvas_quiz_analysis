/**
 * Compile with `g++ binary_check.cpp canvas.cpp -lgmpxx -lgmp -o canvas`
 * Make sure to `sudo apt install libgmp-dev`
 */

#include "binary_check.h"
#include <algorithm>
#include <cmath>
#include <gmpxx.h>
#include <iostream>

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

mpf_class genTree(int k, int options, int numBranches, int oldScore, mpf_class oldAttempts, mpf_class oldProb,
        int depth, int trialCount, mpf_class* factorialMemoize, mpf_class** binCheckMemoize) {
    if (numBranches == NULL) {
        numBranches = k + 1;
    }
    if (depth == options - 1) {
        numBranches = 1;
    }

    mpf_class EV = 0.0;
    for (int j = 0; j < numBranches; j++) { // j is the red number
        int incorrectBefore = k - oldScore; // i (except for attempt 1 on the tree)
        int newScore = k - j;
        mpf_class newAttempts = oldAttempts;
        mpf_class newProb;
        if (depth == options - 1) {         // if on fourth non-extra attempt
            newProb = oldProb;
        } else {
            newAttempts++;                  // remember that fourth attempts are overlapped and do not count
            newProb = oldProb \
                    * combination(incorrectBefore, incorrectBefore - j, factorialMemoize) \
                    * pow((float) 1 / (options - depth), incorrectBefore - j) \
                    * pow((float) (options - depth - 1) / (options - depth), j);
        }

        // if we've reached an ending, calculate attempts * total prob and add to EV
        if (newScore == k) {
            EV += newAttempts * newProb;
            continue;
        }

        // binary check simulator (don't forget symmetry!)
        int a = std::min(newScore - oldScore, k - (newScore - oldScore));
        int b = k - oldScore;
        if (a != 0 && b != 1) { // if we need binary check
            if (binCheckMemoize[b][a] == NULL) {
                // shortcut if single-target and `b` is a power of 2 (no rounding)
                // (https://stackoverflow.com/a/57025941)
                if (a == 1 && (b & (b - 1) == 0) && b != 0) {
                    binCheckMemoize[b][a] = log2(b);
                } else {
                    int binCheckAttemptsTotal = 0;
                    for (int i = 0; i < trialCount; i++) {
                        Node tree(a, b, NULL, NULL);
                        binCheckAttemptsTotal += tree.runBinCheck();
                    }
                    binCheckMemoize[b][a] = (float) binCheckAttemptsTotal / trialCount;
                }
            }
            newAttempts += binCheckMemoize[b][a];
        }

        // recursively call on sub-branches
        // (num_branches = j + 1 to account for getting 0 more correct next attempt)
        EV += genTree(k, options, j + 1, newScore, newAttempts, newProb, depth + 1,
                trialCount, factorialMemoize, binCheckMemoize);
    }

    return EV;
}

int main() {
    int kMin;
    int kMax;
    int options;
    int trialCount = 1000;
    std::cout << "k min (inclusive): ";
    std::cin >> kMin;
    std::cout << "k max (exclusive): ";
    std::cin >> kMax;
    std::cout << "number of options per question: ";
    std::cin >> options;

    mpf_class* factorialMemoize = (mpf_class*) malloc(kMax * sizeof(factorialMemoize[0])); // using kMax cause lazy
    for (int i = 0; i < kMax; i++) {
        // "conditional jump or move depends on uninitialized value" there are no memory errors in ba sing se
        // (i dont think im initializing `mpf_class`es right, because there are no memory issues if they're doubles)
        factorialMemoize[i] = mpf_class(0.0);
    }
    mpf_class** binCheckMemoize = (mpf_class**) malloc(kMax * sizeof(binCheckMemoize[0]));
    for (int i = 0; i < kMax; i++) {
        binCheckMemoize[i] = (mpf_class*) malloc(kMax * sizeof(binCheckMemoize[0][0]));
        for (int j = 0; j < kMax; j++) {
            binCheckMemoize[i][j] = mpf_class(0.0);
        }
    }

    for (int k = kMin; k < kMax; k++) {
        std::cout << k << " " \
                << genTree(k, options, NULL, 0, 0, 1.0, 0, trialCount, factorialMemoize, binCheckMemoize) / k \
                << "\n";
    }

    for (int i = 0; i < kMax; i++) {
        free(binCheckMemoize[i]);
    }
    free(binCheckMemoize);
    free(factorialMemoize);
}
