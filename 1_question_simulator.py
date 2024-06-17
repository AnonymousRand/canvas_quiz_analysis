import random

trials = 10000
questions = 120
choices = 4
attempts = 0

for _ in range(trials):
    for question in range(questions):
        correct = random.randint(0, choices - 1)
        for guess in range(choices):
            attempts += 1
            if guess == correct:
                break

print((attempts / trials) / questions)
