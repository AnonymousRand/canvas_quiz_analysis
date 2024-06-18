#include <unordered_set>
#include <vector>

class Node {
    public: // who needs data hiding and getters and setters
        int a;
        int b;
        int rootVal;
        bool crossed;
        bool correct;

        Node* left;
        Node* right;
        Node* parent;
        std::vector<Node*> leaves;

        Node(int a, int b, int rootVal, Node* parent);
        ~Node();
        int getScore();
        void traverse(int& attempts, int& remainingTargets);
        int runBinaryCheck();
};