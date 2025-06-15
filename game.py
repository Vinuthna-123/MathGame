import random
import operator
import time
import os

operators = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
}

score_file = "high_scores.txt"

def get_user_input(prompt):
    while True:
        response = input(prompt)
        if response.lower() == "hint":
            return "hint"
        try:
            return float(response)
        except ValueError:
            print("Invalid input! Enter a number or type 'hint'.")

def generate_problem():
    num_1 = random.randint(1, 10)
    num_2 = random.randint(1, 10)
    operation = random.choice(list(operators.keys()))
    if operation == '/' and num_2 == 0:
        num_2 = random.randint(1, 10)
    answer = round(operators[operation](num_1, num_2), 2)
    print(f"\nWhat is {num_1} {operation} {num_2}?")
    return answer

def save_score(name, score):
    with open(score_file, "a") as file:
        file.write(f"{name},{score}\n")

def display_high_scores(current_name=None, current_score=None):
    print("\n High Scores:")
    if not os.path.exists(score_file):
        print("No scores yet. Be the first to score!")
        return

    with open(score_file, "r") as file:
        lines = file.readlines()

    scores = []
    for line in lines:
        try:
            name, scr = line.strip().split(",")
            scores.append((name, int(scr)))
        except:
            continue

    top_scores = sorted(scores, key=lambda x: x[1], reverse=True)[:5]

    for i, (name, scr) in enumerate(top_scores, 1):
        mark = " <= You" if name == current_name and scr == current_score else ""
        print(f"{i}. {name}: {scr}{mark}")

def game():
    print(" Welcome to the Math Game!")
    name = input("Enter your name: ").strip()
    score = 0
    lives = 3
    hint_used = False

    print("You have 3 lives. Type 'hint' once per game to get help.")
    print("Answer within 10 seconds for each question.\n")

    while lives > 0:
        correct_answer = generate_problem()
        start_time = time.time()
        response = get_user_input("Your answer (or type 'hint'): ")

        if response == "hint":
            if not hint_used:
                hint_used = True
                print(f"Hint: The answer is approximately {round(correct_answer, 1)}")
                continue
            else:
                print("Hint already used.")
                continue

        time_taken = time.time() - start_time

        if time_taken > 10:
            print(" Time's up! You lost a life.")
            lives -= 1
        elif abs(response - correct_answer) < 0.01:
            print(" Correct!")
            score += 1
        else:
            print(f" Incorrect. The correct answer was {correct_answer}")
            lives -= 1

        print(f"Lives remaining: {lives}")

    print(f"\n🎉 Game Over, {name}!")
    print(f"Your final score: {score}")

    # Save and show scores
    save_score(name, score)
    display_high_scores(current_name=name, current_score=score)

game()
