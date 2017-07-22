import random
import time


def print_guesses_left(guesses_made, guesses_allowed):
    guesses_left = guesses_allowed - guesses_made
    if guesses_left == 1:
        print("You're on your last guess!")
    else:
        print("You have {} guesses left.".format(guesses_left))


def number_game(low=1, high=100, guesses_allowed=10):
    target_number = random.randint(low, high)
    print_greeting(low, high, guesses_allowed)
    guesses_made = 0
    guess = None
    while guesses_made < guesses_allowed and guess != target_number:
        print_guesses_left(guesses_made, guesses_allowed)
        guess = get_guess()
        report_guess(guess, target_number)
        guesses_made += 1
    print_exit(guess, target_number, guesses_made)


def get_guess():
    print("Take a guess!")
    guess = None
    while guess is None:
        str_input = input(">> ").strip()
        try:
            guess = int(str_input)
        except ValueError:
            print("I couldn't interpret that as an integer.  Try again, please.")
    return guess


def print_greeting(low, high, tries):
    print("I am thinking of a number between {} and {}.".format(low, high))
    print("You have {} tries to guess the number correctly.".format(tries))


def report_guess(guess, target_number):
    if guess > target_number:
        print("That's \u2191higher\u2191 than the number I have in mind.")
    elif guess < target_number:
        print("That's \u2193lower\u2193 than the number I have in mind.")
    else:
        print("That's it!")


def print_exit(last_guess, target_number, guesses_made):
    if last_guess == target_number:
        print("Congratulations, you guessed the correct number!")
        time.sleep(0.5)
        print("It only took you, " + str(guesses_made) + " tries!")
        time.sleep(0.5)
    else:
        print("Sorry, that wasn't the number I had in mind.")
        print("I was thinking of {}".format(target_number))


def prompt_for_another_game():
    print("That was fun!")
    print("Would you like to play again?")
    again = 'y' in input("(y/n) >> ").lower()
    return again


if __name__ == "__main__":
    play = True
    while play:
        number_game()
        play = prompt_for_another_game()
        if play:
            print("Alright!  Let's do another!")
        else:
            print("Oh well.  See you around.")
