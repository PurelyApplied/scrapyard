'''Play blackjack!  An impromptu write-up in responce to the reddit
post at
https://www.reddit.com/r/learnpython/comments/4yjjpj/one_week_of_programming_under_my_belt_and_im/'''

from random import shuffle

_number_of_decks = 3
_card_count_reshuffle_trigger = 40

def main():
    '''Main loop; prompts for another game after each round.'''
    play_game = True
    deck = []
    while play_game:
        print()
        if len(deck) <= _card_count_reshuffle_trigger:
            deck = build_deck()
        play(deck)
        if not 'y' in input("Play again?\n(y/n) >> ").lower():
            play_game = False


def play(deck):
    '''Play a single round of blackjack.'''
    ## Shuffle up and deal two cards to everyone.
    player = []
    dealer = []
    hit(player, deck)
    hit(dealer, deck)
    hit(player, deck)
    hit(dealer, deck)
    print("You have", report_hand(player))
    print("The dealer is showing", tuple_card_to_str(dealer[1]))
    ## Put the input last so it doesn't prompt if the first is false
    while (hand_value(player) < 21
           and 'y' in input("Hit on {}? (y/n) >> ".format(hand_value(player)))):
        hit(player, deck)
        print(report_hand(player))
    ## If you bust out, the dealer doesn't need to do anything.
    if hand_value(player) > 21:
        print("You bust!")
        return
    elif hand_value(player) == 21:
        print("WOO!  21!")
    ## Dealer hits on a 16, stays on 17
    print("The dealer reveals his card.")
    print("The dealer has", report_hand(dealer))
    while hand_value(dealer) < 17:
        print("The dealer hits.")
        hit(dealer, deck)
        print(report_hand(dealer))
    ## Report the outcome
    print("You have", report_hand(player))
    print("The dealer has", report_hand(dealer))
    
    if hand_value(dealer) > 21:
        print("The dealer bust!  You win!!")
    elif hand_value(player) > hand_value(dealer):
        print("You beat the dealer!  You win!!")
    elif hand_value(player) == hand_value(dealer):
        print("You push.  A tie.  How boring.")
    else:
        print("The dealer beats you.  You lose.")


def build_deck():
    '''Returns a shuffled deck of cards in the form (value, suit).  Values
    range 1 to 13, suit is a single-character in 'hsdc'.

    '''
    print("The deck gets shuffled.")
    d = [(v, s) for v in range(1, 14) for s in 'hcds'] * _number_of_decks
    shuffle(d)
    return d


def hit(hand, deck, n=1):
    '''Draw from the deck and add it to the hand.'''
    for i in range(n):
        hand.append(deck.pop())
    

def hand_value(hand):
    '''Computes the value of a blackjack hand.'''
    ace_count = sum(1 for v, _ in hand if v == 1)
    value = sum(min(v, 10) for v, _ in hand)
    while ace_count > 0 and value <= 11:
        value += 10
        ace_count -= 1
    return value


def tuple_card_to_str(card):
    v, s = card
    if v == 1:
        v = 'A'
    elif v == 10:
        v = 'T'
    elif v == 11:
        v = 'J'
    elif v == 12:
        v = 'Q'
    elif v == 13:
        v = 'K'
    return "{}{}".format(v, s)

def report_hand(hand):
    report = ", ".join(tuple_card_to_str(c) for c in hand)
    report += " ({})".format(hand_value(hand))
    return report
