#include <vector>


class Node {
    public:
        Node(int a, int b, int rootVal, Node* parent);
        ~Node();

        int runBinCheck();

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
        void traverse(int& attemptCount, int& remainingTargets);
};
