import random

trials = 10000
questions = 120
choices = 4
questions_at_a_time = 2
attempts = 0

BLANK = -1

def get_score(correct, guess):
    global attempts
    attempts += 1 # increment here

    score = 0
    for i, correct_elem in enumerate(correct):
        if guess[i] == correct_elem:
            score += 1
    return score

for _ in range(trials):
    for question in range(questions // questions_at_a_time):
        correct = []
        for _ in range(questions_at_a_time):
            correct.append(random.randint(0, choices - 1))
        guess = [0] * questions_at_a_time
        one_confirmed = False # if we've already spent an extra turn
                              # verifying which one is right,
                              # don't do it again
        confirmed_guess = BLANK

        # attempt loop
        score = get_score(correct, guess)
        while score != questions_at_a_time:
            # your ai steals people's data, my "ai" is a bunch of ifs
            # (I don't have time to figure out a smarter way)
            if score == 0:
                guess = [g + 1 for g in guess]
                score = get_score(correct, guess)
                continue

            if score == 1:
                if not one_confirmed:    # if we need extra turn
                    one_confirmed = True
                    original_second_guess = guess[1]

                    guess[1] = BLANK
                    score = get_score(correct, guess)
                    if score == 1:       # if we got the first one right
                        confirmed_guess = 0
                        guess[1] = original_second_guess + 1
                    else:                # if we got the second one right
                        confirmed_guess = 1
                        guess[1] = original_second_guess
                        guess[0] += 1

                    score = get_score(correct, guess)
                    continue

                if confirmed_guess == 0:
                    guess[1] += 1
                elif confirmed_guess == 1:
                    guess[0] += 1
                score = get_score(correct, guess)
                continue

print((attempts / trials) / questions)
