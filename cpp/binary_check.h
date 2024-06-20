#include <vector>

class Node {
    private:
        int a;
        int b;
        int rootVal;
        bool crossed;
        bool correct;

        Node* left;
        Node* right;
        Node* parent;
        std::vector<Node*> leaves;

        int getScore();
        void traverse(int& attempts, int& remainingTargets);

    public:
        Node(int a, int b, int rootVal, Node* parent);
        ~Node();
        int runBinaryCheck();
};
