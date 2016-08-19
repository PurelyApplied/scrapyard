'''Play blackjack!  An impromptu write-up in responce to the reddit
post at
https://www.reddit.com/r/learnpython/comments/4yjjpj/one_week_of_programming_under_my_belt_and_im/'''

# I haven't done anything interesting with the hand reporting, so the
# prints are pretty crude.

# A more interesting game might not use a fresh deck every time.
# Decide on a number of decks to use, and reshuffle after a game if
# you have less than, say, one deck's worth left.

# I use the hell out of list comprehensions.  They're really valuable to know.

# Docstrings are always good.  Use them.

# play() could also return a True/False (or probably a 1, 0, -1) to
# report wins/losses/draws, which you could count in main()

from random import shuffle

def main():
    '''Main loop; prompts for another game after each round.'''
    play_game = True
    while play_game:
        play()
        if not 'y' in input("Play again?\n (y/n) >> ").lower():
            play_game = False


def play():
    '''Play a single round of blackjack.'''
    ## Shuffle up and deal two cards to everyone.
    deck = build_deck()
    player = []
    dealer = []
    hit(player, deck)
    hit(dealer, deck)
    hit(player, deck)
    hit(dealer, deck)
    ## I guess in hindsight you don't know the dealer's "down" card
    ## until later.
    print("You have {} ({}).  The dealer has {} ({}).".format(
        player, hand_value(player),
        dealer, hand_value(dealer)))
    ## Put the input last so it doesn't prompt if the first is false
    ## (Look up logical short circuiting)
    while hand_value(player) <= 21 and 'y' in input("Hit? (y/n) >> "):
        hit(player, deck)
        print("You now have {} ({})".format(player, hand_value(player)))
    ## If you bust out, the dealer doesn't need to do anything.
    if hand_value(player) > 21:
        print("You bust!")
        return
    ## Dealer hits on a 16, stays on 17
    while hand_value(dealer) < 17:
        hit(dealer, deck)
        print("Dealer hits.  He now has {} ({})".format(
            dealer, hand_value(dealer)))
    ## Report the outcome
    print("You have {} ({}).  The dealer has {} ({}).".format(
        player, hand_value(player),
        dealer, hand_value(dealer)))
    if hand_value(dealer) > 21:
        print("The dealer bust!  You win!!")
    elif hand_value(player) > hand_value(dealer):
        print("You beat the dealer!  You win!!")
    elif hand_value(player) == hand_value(dealer):
        print("You push.  It's a tie.")
    else:
        print("The dealer beats you.  You lose.")


def build_deck():
    '''Returns a shuffled deck of cards in the form (value, suit).  Values
    range 1 to 13, suit is a single-character in 'hsdc'

    '''
    print("The deck gets shuffled.")
    d = [(v, s) for v in range(1, 14) for s in 'hcds']
    shuffle(d)
    return d


def hit(hand, deck):
    '''Draw from the deck and add it to the hand'''
    hand.append(deck.pop())


def hand_value(hand):
    '''Computes the value of a blackjack hand.'''
    ace_count = sum(1 for v, _ in hand if v == 1)
    value = sum(min(v, 10) for v, _ in hand)
    while ace_count > 0 and value <= 11:
        value += 10
        ace_count -= 1
    return value
