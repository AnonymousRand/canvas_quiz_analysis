import random

TRIAL_COUNT = 10000
QUESTION_COUNT = 120
OPTION_COUNT = 4
attemptCount = 0

for _ in range(TRIAL_COUNT):
    for question in range(QUESTION_COUNT):
        correct = random.randint(0, OPTION_COUNT - 1)
        for guess in range(OPTION_COUNT - 1): # -1 for last attempt skip
            attemptCount += 1
            if guess == correct:
                break

print((attemptCount / TRIAL_COUNT) / QUESTION_COUNT)
