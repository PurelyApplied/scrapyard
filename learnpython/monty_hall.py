#%%
from random import shuffle, choice
'''Written on a whim as a "How I'd do it", in response to
https://www.reddit.com/r/learnpython/comments/53w3g1/monty_hall_challenge/
'''

# Prompts are 1-indexed, but everything internal,
#  including if you provide your_choice, is 0-indexed.
def monty_hall(your_choice=None, switch=None,
               reveal_at_start=False, verbose=True):
    '''If your_choice, switch = None, prompts are given.
    If they are provided, (your_choice in (0, 1, 2), switch in (True, False),
    then they take on that value'''
    outcomes = ["goat", "sheep", "new car"]
    shuffle(outcomes)
    if reveal_at_start:
        print("Secret:  the prizes are in this order: {}".format(outcomes))
    if your_choice is None:
        your_choice = int(input("Choose a door!  1, 2, or 3?  >> ")) - 1
    monty_choices = [i for i, o in enumerate(outcomes)
                     if i != your_choice and o != "new car"]
    monty_chooses = choice(monty_choices)
    if verbose:
        print("Monty reveals Door #{}: a {}!".format(
            monty_chooses + 1, outcomes[monty_chooses]))
    if switch == None:
        switch = "y" in input("Do you switch your choice? (y/n) >> ")
    if switch:
        switch_choices = [0, 1, 2]
        switch_choices.remove(monty_chooses)
        switch_choices.remove(your_choice)
        your_choice = switch_choices[0]
        if verbose:
            print("You switch to Door #{}.".format(your_choice + 1))
    if verbose:
        print("The other doors are opened!")
        print("\n".join(
            "Behind Door #{} is: {}".format(i+1, o)
            for i, o in enumerate(outcomes)))
        print("You got a {}!".format(outcomes[your_choice]))
    return outcomes[your_choice] == "new car"
    

def do_many(n=100, initial_choice=0, switch=True):
    wins = sum(monty_hall(initial_choice, switch, False, False)
        for i in range(n))
    print("You won {} out of {} ({}%)".format(wins, n, wins / n * 100))