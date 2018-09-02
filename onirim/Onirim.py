import sfml as sf
from time import sleep
from pprint import pprint
from enum import Enum
import random
# import logging

if __name__=="__main__":
    print("Updating etags...")
    import os
    os.system('etags Onirim.py')
    if "Onirim.pyc" in os.listdir():
        print("purging Onirim.pyc...")
        os.system('rm Onirim.pyc')

COLOR = Enum("color",
             ["red", "blue", "green", "brown", 'rainbow', "oni"])

def colors_match(color1, color2):
    if (color1 == color2
        or COLOR.rainbow in (color1, color2)):
        return True


CARD_TYPE = Enum("card_type",
                 ["sun", "moon", "key", "door", "nightmare",
                  "glyph", "lost", "tower", "happy", "deadend", "denizen"])

CARD_TYPE = Enum("card_type",
                 ["sun", "moon", "key", "door", "nightmare",
                  "glyph", "lost", "tower", "happy", "deadend", "denizen"])

DENIZEN_TYPES = Enum("denizen",
                     ['Architect',
                      'Hammer Bird',
                      'Cyclobot',
                      'Chromatic Chaos',
                      'Squirrel Spies',
                      'Mirror',
                      'Harpoon Hunter',
                      'Repentant Treasure Keeper'])

TOWER_SIDE = Enum("side",
                  ["sun", "moon", "both", "none"])

EXPANSION = Enum("expansion",
                 ["spells",
                  "glyphs",
                  "catchers",
                  "towers",
                  "happy",
                  "cross",
                  "oni",
                  "incubus"])

EXPANSION_LONG_NAME = Enum("expansion_long",
                           ["The Book of Steps Lost and Found",
                            "The Glyphs",
                            "The Dreamcatchers",
                            "The Towers",
                            "Happy Dreams and Dark Premonitions",
                            "Crossroads and Dead Ends",
                            "The Door to the Oniverse",
                            "The Little Incubus"])


# Spells: + can cast spells, + door goal order requirements.  If door not next, to limbo
# -- Paradoxical Prophecy, 5 (6): Examine bottom 5 of deck, one to top, rest to bottom
# -- Parallel Planning, 7 (9): Swap two goal cards
# -- Powerful Punishment, 10 (12): Escape a nightmare

# Glyphs: + one door / two glyphs of each color, + goals if needed
# Incantation: reveal top 5 cards.  If one is a door, claim it.  Cards to bottom in any order.

# Dreamcatchers

# Towers: + 12 tower cards, need one tower of each color
# Towers *cannot* chare symbols with neighbors
# "Scout": Top 3/4/5 cards, rearrange, return to top
# Nightmare discards tower of choice, only if remaining cards yield legal arrangement.
# -- False Destruction: No lost tower, nightmare to limbo instead of discard
# -- Power of Alignment: when victory condition met, protected from nightmare
# -- -- Variant: Scatter the Ruins: there is no power of alignment

# Happy: + 4 happy dreams, + 8 dark premonitions
# Happy dreams:
#  (a) remove one Dark Premonition
#  (b) reveal top 7, discarding any, return to top in order of choice
#  (c) find any card of your choice.
# then discard
# Normal: 4 Dark Prem, Med: 5, Hard 6

# Crossroads: 10 deadends, 3/2/1 rainbow.
#  May discard rainbow key to unlock any door
#  Deadends cannot be played or discarded (as an action; Nightmare etc okay).
#  Nightmare "burn top 5" option limbos dead ends
# + phase 1 option: Trigger an Escape
# Escape:
#   discard your entire hand.  Draw a new hand.
# Variant: rainbow only as second of trio.

# Door to oni
# + 16 (8x2) denizens, +1 door, +1 goal as needed
# Oni door is any color.
# When denizen drawn:
# (a) Rally!
# -- -- Choose a card from your hand and discard it.  No rally limit

def exp_long_name(exp):
    return EXPANSION_LONG_NAME(exp.value).name


EVENTS = Enum("stack_event", [
    # Card acquisition
    "new_hand",
    "draw_card",
    # Modes of play
    "play_to_path",
    "check_for_path_trio",
    "discover_door",
    "play_to_towers",
    "cast_spell",
    # Sepcial draws
    "door_drawn",
    "nightmare_drawn",
    "happy_dream_drawn",
    "denizen_drawn",
    # Nightmare results
    "discard_hand",
    "destroy_tower",
    "limbo_a_door",
    # Card management
    "check_limbo",
    "shuffle_deck",
    "empty_dreamcatcher",
    # Control
    "deck_empty",
    "idle",
    "exit"
])


class OnirimStack:
    def __init__(self):
        self.container = []
        
    def __repr__(self):
        return "<OnirimStack>"

    def __bool__(self):
        return bool(self.container)
        
    def pop(self, pos=0):
        return self.container.pop(pos)

    def add_event(self, tag, *args):
        self.container.append((tag, args))

               
class OnirimGameEventHandler:
    def __init__(self, expansions):
        self.res_map = self.get_resolution_map()

    def __repr__(self):
        return "<OnirimGameEventHandler>"

    def resolve_stack(self):
        item, args = stack.pop()
        f = self.res_map(item, None)
        if f:
            f(*args)

    # # Card acquisition
    # "new_hand",
    # "draw_card",
    # # Modes of play
    # "play_to_path",
    # "check_for_path_trio",
    # "discover_door",
    # "play_to_towers",
    # "cast_spell",
    # # Sepcial draws
    # "door_drawn",
    # "nightmare_drawn",
    # "happy_dream_drawn",
    # "denizen_drawn",
    # # Nightmare results
    # "discard_hand",
    # "destroy_tower",
    # "limbo_a_door",
    # # Card management
    # "check_limbo",
    # "shuffle_deck",
    # "empty_dreamcatcher",
    # # Control
    # "exit"

    def get_resolution_map(self):
        return {
            # EVENTS.idle : lambda : EVENTS.idle,
            EVENTS.check_for_path_trio : self.detect_trio,
            EVENTS.new_hand : lambda : self.draw_new_card(True),
            EVENTS.draw_card : lambda : self.draw_new_card(False),
            EVENTS.check_limbo : self.check_and_resolve_limbo,
            EVENTS.nightmare_drawn : self.resolve_nightmare,
            EVENTS.door_drawn : self.resolve_drawn_door,
            EVENTS.discover_door : self.discover_door,
            EVENTS.play_to_path : self.attempt_play_card_to_path
        }
        
    def detect_trio(self):
        # Get a free door if you have three consecutive colors, not to
        # be duplicated if you do, say, 4 in a row, of course.
        if not self.path:
            return
        last_card_color = self.path.last().color
        color_count = 1
        while (color_count + 1 < len(self.path)):
            this_card_color = self.path.get(-(color_count + 1)).color
            if colors_match(this_card_color, last_card_color):
                color_count += 1
            else:
                break
            if last_card_color == COLOR.rainbow:
                last_card_color = this_card_color
        self.debug.log("Color run: {}".format(color_count))
        if color_count and color_count % 3 == 0:
            return (EVENTS.discover_door, last_card_color)
        pass
        # Something like [red red rainbow blue blue] will trigger
        # twice.

    def resolve_drawn_door(self, door_card):
        self.debug.log("A door is drawn!")
        print("Door:", door_card)
        if self.player.has_key_for(door_card):
            print("TODO!")

    def discover_door(self, color):
        # pass Need to make sure looking for a door is needed?  Third
        # time through red won't need a new red door maybe.
        self.debug.log("Looking for a {} door...".format(color))
        door_found = False
        while not door_found:
            card = self.deck.pull_card()
            if not card:
                return EVENTS.deck_empty
            self.debug.log("Pulled a {}".format(card))
            door_found = (card.type == CARD_TYPE.door and card.color == color)
            if not door_found:
                self.debug.log("Sent to limbo")
                self.limbo.append(card)
        self.unlocked_doors.append(card)
        return EVENTS.check_limbo

    def resolve_nightmare(self, card):
        self.debug.log("TODO: resolve nightmare")
        pass

    def draw_new_card(self, new_hand=False):
        card = self.deck.pull_card()
        redraw_event = EVENTS.new_hand if new_hand else EVENTS.draw_card 
        if not card:
            self.debug.log("The deck is empty!")
            return 
            # pass: sent You Lose to stack if playerhand is empty
        self.debug.log("You drew {}.".format(card))
        if card.can_be_drawn(new_hand=new_hand):
            self.player.hand.append(card)
        else:
            if new_hand:
                self.debug.log("Card not valid for new hand.")
                self.debug.log("Card sent to limbo.")
                self.limbo.append(card)
                return (redraw_event)
            else:
                if card.type == CARD_TYPE.nightmare:
                    return ((EVENTS.nightmare_drawn, card), redraw_event)
                if card.type == CARD_TYPE.door:
                    return ((EVENTS.door_drawn, card), redraw_event)
        # Continue drawing?
        if len(self.player.hand) < 5:
            return EVENTS.new_hand if new_hand else EVENTS.draw_card
        else:
            return EVENTS.check_limbo

    def attempt_play_card_to_path(self, index):
        print("Get play hand index", index)
        card_to_play = self.player.hand.get(index)
        print("Card to play:", card_to_play)
        if not card_to_play.type in (
                CARD_TYPE.sun,
                CARD_TYPE.moon,
                CARD_TYPE.key,
                CARD_TYPE.glyph ):
            print("Invalid card type.")
            return
        last_card = self.path.last()
        if not last_card:
            print("No card yet in path.")
        else:
            print("Last card in path:", last_card)
            # You can't play the same type twice in a row
            card_to_play = self.player.hand.get(index)
            print("Card to play:", last_card)
            if last_card.type == card_to_play.type:
                self.debug.log("You can't play two of the same type in a row.")
                return
        # Path open for play:
        self.player.hand.pop(index)
        self.path.append(card_to_play)
        return (EVENTS.draw_card, EVENTS.check_for_path_trio)

    def draw(self):
        self.window.clear()
        peek = CardPile(font=self.font,
                        pos=(800, 300),
                        header="Top deck",
                        pile=self.deck.cards)
        for item in (self.terminal,
                     self.path,
                     self.player,
                     self.debug,
                     self.discard,
                     self.limbo,
                     self.unlocked_doors,
                     peek):
            self.window.draw(item)
        
        self.window.display()
        
    def process_game_events(self):
        if not self.stack:
            return
        tag, args = self.stack.pop()
        f = self.res_map.get(tag, None)
        self.debug.log(">> Process game event: {} ; {}".format(tag, args))
        if not f:
            self.debug.log(">> Event does not have associated function!!")
        if tag == EVENTS.exit:
            self.window.close()
            self.running = False
            return
        if f:
            new_item = f(*args)
            if new_item:
                if hasattr(new_item, "__iter__"):
                    print("Multiadd to stack!")
                    for item in new_item:
                        if hasattr(item, "__iter__"):
                            self.stack.add_event(*item)
                        else:
                            self.stack.add_event(item)
                else:
                    self.stack.add_event(new_item)
    
class Onirim(OnirimGameEventHandler):
    def __init__(self, expansions=()):
        OnirimGameEventHandler.__init__(self, expansions)
        # SFML framework
        self.window = sf.RenderWindow(sf.VideoMode(1280, 720),"Onirim");
        self.window.framerate_limit = 30
        self.font = sf.Font.from_file('resource/freefont/FreeMono.ttf')
        # Control
        self.stack = OnirimStack()
        self.stack.add_event(EVENTS.new_hand)
        self.running = True
        self.terminal = Terminal(self.font)
        self.debug = Terminal(self.font, char_size=16, pos=(0, 500),
                              lines=10, print_on_log=True)
        # Game core
        self.deck = OnirimDeck(expansions)
        self.player = OnirimPlayer(font=self.font)
        self.path = CardPile(font=self.font,
                             pos=(600, 0),
                             header="Path")
        self.discard = CardPile(font=self.font,
                                pos=(600, 500),
                                draw_last=1,
                                header="Discards")
        self.limbo = CardPile(font=self.font,
                              pos=(600, 300),
                              draw_last=1,
                              header="Limbo")
        self.unlocked_doors = CardPile(font=self.font,
                                       header="Unlocked doors",
                                       draw_last = 100,
                                       pos=(800, 500))
        # Expansions
        self.tower_playfield = []
        self.dream_catchers = [CardPile(font=self.font, draw_last=1)
                               for i in range(4)]
        self.door_order = None
        self.banished   = []
        self.incubus_state = None

        # temp:
        self.last_command = ""

    def __repr__(self):
        return "<Onirim>"

    def parse_command(self):
        command = self.terminal.get_last_line().strip("> ")
        if command == "":
            command = self.last_command
        else:
            self.last_command = command
        # print("Parsing command:", command)
        args = command.split()
        if "play" in args:
            if (len(args) == 2
                and args[0].lower() == "play"
                and args[1].isnumeric()
                and 0 < int(args[1]) <= 5):
                self.stack.add_event(EVENTS.play_to_path, int(args[1]) - 1)
        elif "discard" in args:
            if (len(args) == 2
                and args[0].lower() == "discard"
                and args[1].isnumeric()
                and 0 < int(args[1]) <= 5):
                self.stack.add_event(EVENTS.discard_card, int(args[1]) - 1)
        elif "exit" in command:
            self.stack.add_event(EVENTS.exit)
        else:
            self.terminal.log("Unknown command.")
            self.terminal.log("> ")
            
    def process_window_events(self):
        for event in self.window.events:
            if event is sf.CloseEvent:
                self.window.close()
                return
                # should use isinstance
            if type(event) is sf.TextEvent:
                self.terminal.enter_char(event.unicode)
            elif (type(event) is sf.KeyEvent
                  and event.pressed):
                if event.code is sf.Keyboard.ESCAPE:
                    self.window.close()
                    return
                if event.code == sf.Keyboard.RETURN:
                    self.parse_command()
                    if not self.terminal.get_last_line() == "> ":
                        self.terminal.log("> ")

    def process_events(self):
        self.process_window_events()
        self.process_game_events()

    def play(self):
        self.terminal.log("You begin to dream...")
        self.terminal.log("> ")
        while self.running:
            try:
                self.draw()
                self.process_events()
            except KeyboardInterrupt:
                playing = "y" in input("Keep playing? (y/n) >> ")

    def check_and_resolve_limbo(self):
        self.debug.log("Checking limbo...")
        if not self.limbo:
            self.debug.log("Limbo empty.")
            return
        self.debug.log("Limbo nonempty.  Shuffling into deck")
        self.deck.extend(self.limbo)
        self.limbo.empty()
        self.deck.shuffle()


class Terminal(sf.Drawable):
    def __init__(self, font, char_size=16, pos=(0,0), color=sf.Color.RED,
                 lines=5, print_on_log=False):
        sf.Drawable.__init__(self)
        self.history = [""]
        self.position = pos
        self.color = color
        self.font = font
        self.char_size = char_size
        self.lines_drawn = lines
        self.also_console_on_log = print_on_log

    def __repr__(self):
        return "<Terminal>"

    def enter_char(self, char):
        # Perform backspace
        if char == 8:
            self.backspace()
        # ignore newlines
        elif char == 13:
            None
        # type anything else
        else:
            self.type_char(chr(char))
                        
    def draw(self, target, states):
        text = "\n".join(self.history[-self.lines_drawn:])
        sftext = sf.Text(string=text,
                         font=self.font, character_size=self.char_size)
        sftext.color = self.color
        sftext.position = self.position
        target.draw(sftext, states)

    def log(self, s):
        self.history.append(s)
        if self.also_console_on_log:
            print(s)

    def type_char(self, s):
        self.history[-1] += s

    def backspace(self):
        self.history[-1] = self.history[-1][:-1]

    def get_last_line(self):
        return self.history[-1]


class OnirimPlayer(sf.Drawable):
    def __init__(self, font, char_size=16, pos=(0,300), color=sf.Color.RED):
        sf.Drawable.__init__(self)
        self.hand = CardPile()
        self.font = font
        self.char_size = char_size
        self.pos = pos
        self.color = color
        
    def __repr__(self):
        return "<OnirimPlayer>"

    def has_key_for(self, door):
        key_pos = [i for i in range(5)
                   if self.hand[i].type == CARD_TYPE.key
                   and colors_match(self.hand[i].color, door.color)]
        print("You could use positions:", key_pos)
        pass

    def draw(self, target, states):
        text = "Your cards:\n"
        text += "\n".join("{}: {} {}".format(p + 1, c.color.name, c.type.name)
                          for p, c in enumerate(self.hand))
        sftext = sf.Text(string=text, font=self.font)
        sftext.position = (0, 300)
        sftext.color = sf.Color.RED
        target.draw(sftext)


class CardPile(sf.Drawable):
    def __init__(self, pile=None, header="", font=None,
                 draw_last=5, char_size=16, pos=(0,0), color=sf.Color.RED):
        self.pile = [] if not pile else pile
        self.font = font
        self.char_size = char_size
        self.pos = pos
        self.color = color
        self.head = header
        self.draw_last = draw_last

    def __repr__(self):
        return "<CardPile>"

    def __getitem__(self, p):
        return self.pile[p]

    def __bool__(self):
        return bool(self.pile)

    def __len__(self):
        return len(self.pile)

    def empty(self):
        self.pile = []

    def append(self, c):
        self.pile.append(c)

    def pop(self, pos=0):
        return self.pile.pop(pos)

    def last(self):
        return None if not self.pile else self.pile[-1]

    def get(self, pos):
        return self.pile[pos] if pos < len(self.pile) else None

    def draw(self, target, states):
        if not self.font:
            return
        text = self.head + ("\n" if self.head else "")
        text += "\n".join("{}: {}".format(p + 1, c)
                          for p, c in list(enumerate(self.pile))[-self.draw_last:])
        sftext = sf.Text(string=text, font=self.font)
        sftext.position = self.pos
        sftext.color = self.color
        target.draw(sftext)

        
####################
## Begin card classes

_card_types = {CARD_TYPE.sun,
               CARD_TYPE.moon,
               CARD_TYPE.key,
               CARD_TYPE.door,
               CARD_TYPE.nightmare,
               CARD_TYPE.glyph,
               CARD_TYPE.lost,
               CARD_TYPE.tower,
               CARD_TYPE.happy,
               CARD_TYPE.deadend,
               CARD_TYPE.denizen }

class Card:
    '''Base class for cards.'''
    _instance_counter = 0
    _can_be_drawn = { CARD_TYPE.sun,
                      CARD_TYPE.moon,
                      CARD_TYPE.key,
                      CARD_TYPE.glyph,
                      CARD_TYPE.tower }
    

    _skipped_on_new_hand = { CARD_TYPE.nightmare }
    
    def __init__(self, type=None, color=None):
        assert type in CARD_TYPE, "Invalid Card type."
        self.type = type
        self.color = color
        self.instance = Card._instance_counter
        Card._instance_counter += 1

    def __repr__(self):
        return "<Card: {}>".format(self.type)

    def __str__(self):
        return "{}{}".format(
            self.color.name + " " if self.color else "",
            self.type.name)

    def long_name(self):
        return "Card (instance {:<5d}) ; {:20s} ; {:13s}".format(
            self.instance,
            self.type,
            self.color if self.color else "None")

    def play(self):
        pass

    def discard(self):
        pass

    def can_be_drawn(self, new_hand=False):
        return (
            self.type in self._can_be_drawn
            and ( not new_hand 
                  or not self.type in self._skipped_on_new_hand ))

##########    
## Base deck clases:
class SunCard(Card):
    def __init__(self, color):
        super().__init__(CARD_TYPE.sun, color)

class MoonCard(Card):
    def __init__(self, color):
        super().__init__(CARD_TYPE.moon, color)

class KeyCard(Card):
    def __init__(self, color):
        super().__init__(CARD_TYPE.key, color)

class DoorCard(Card):
    def __init__(self, color):
        super().__init__(CARD_TYPE.door, color)

class NightmareCard(Card):
    def __init__(self):
        super().__init__(CARD_TYPE.nightmare)


##########
## Expansion classes
class GlyphCard(Card):
    def __init__(self, color):
        super().__init__(CARD_TYPE.glyph, color)

    def play(self):
        pass

    def discard(self):
        pass


class TowerCard(Card):
    def __init__(self, color, value, left, right):
        super().__init__(CARD_TYPE.tower, color)
        self.value = value
        self.left = left
        self.right = right

    def __str__(self):
        return super().__str__() + "; L {} R {}".format(self.left, self.right)

    def play(self):
        pass

    def discard(self):
        pass


class DeadendCard(Card):
    def __init__(self):
        super().__init__(CARD_TYPE.deadend)

    def play(self):
        pass

    def discard(self):
        pass

class HappyCard(Card):
    def __init__(self):
        super().__init__(CARD_TYPE.happy)
        
class LostCard(Card):
    def __init__(self):
        super().__init__(CARD_TYPE.lost)

class DenizenCard(Card):
    def __init__(self, deni_type):
        super().__init__(CARD_TYPE.denizen)
        self.deni_type = deni_type
        # 'Architect', # You may play the same symbol back-to-back
        
    def __str__(self):
        return super().__str__() + "; {}".format(self.deni_type)
        # 'Hammer Bird', # Discard the last card played in your
        # Labyrinth row, along with all cards matching the same color
        
        # 'Cyclobot', # Trade one location card in your hand with one
        # from the discard pile.
        
        # 'Chromatic Chaos', # Change the color of a door.  Goal cards
        # are not "fooled".  Essentially, change a key or a trio into
        # another color
        
        # 'Squirrel Spies', # Look at the top 5 cards of the deck ;
        # return in the order of your choice
        
        # 'Mirror', # put a nightmare you just drew into a Limbo pile
        # without resolving it
        
        # 'Harpoon Hunter', # Reveal the top 5 cards, discarding all
        # nightmares.  Return the remaining cards at the bottom of the
        # deck in the order of your choosing.
        
        # 'Repentant Treasure Keeper', # Hide a card under this card ;
        # this card is protected from nightmares / escapes / dark
        # permonitions.

## End card classes
####################

class OnirimDeck:
    def __init__(self, build_with_expansions=(), shuffle=True):
        
        self.cards = []
        self.add_base_deck()
        if EXPANSION.glyphs in build_with_expansions:
            self.add_glyph_deck()
        # if EXPANSION.catchers in build_with_expansions:
        #     pass
        if EXPANSION.towers in build_with_expansions:
            self.add_tower_deck()
        # if EXPANSION.happy in build_with_expansions:
        #     pass
        if EXPANSION.cross in build_with_expansions:
            self.add_crossroads_deck()
        # if EXPANSION.oni in build_with_expansions:
        #     pass
        # self.add_happy_deck()
        # self.add_lost_dreams_deck()
        # self.add_denizens()
        random.shuffle(self.cards)
        pass

    def __repr__(self):
        return "<OnirimDeck>"

    def extend(self, L):
        self.cards.extend(L)

    def shuffle(self):
        random.shuffle(self.cards)

    def pull_card(self):
        return self.cards.pop() if self.cards else None

    def peek(self, n=1):
        return self.cards[:n]

    def add_base_deck(self):
        # 2 of each door
        # 16/15/14/13 red/blue/green/brown locations;
        # -- 3 keys, 4 moons, 9/8/7/6 suns for red/blue/green/brown
        # 10 nightmares
        doors  = [DoorCard(c)
                  for c in COLOR for i in range(2)]
        keys   = [KeyCard(c)
                  for c in COLOR for i in range(3)]
        moons  = [MoonCard(c)
                  for c in COLOR for i in range(4)]
        suns   = []
        for quant, col in zip([9,8,7,6], COLOR):
            suns.extend(SunCard(col)
                        for i in range(quant))
        nightmares = [NightmareCard()
                      for i in range(10)]

        self.cards += doors + moons + keys + suns + nightmares

        
    def add_glyph_deck(self):
        # 2 glyphs of each color
        # 1 door of each color
        glyphs= [GlyphCard(c)
                 for c in COLOR for i in range(2)]
        doors = [DoorCard(c)
                 for c in COLOR]
        self.cards += glyphs + doors

    def add_tower_deck(self):
        # Complicated, but 12 towers.
        self.cards += [
            TowerCard(COLOR.red, 3, TOWER_SIDE.both, TOWER_SIDE.moon),
            TowerCard(COLOR.red, 4, TOWER_SIDE.sun, TOWER_SIDE.moon),
            TowerCard(COLOR.red, 5, TOWER_SIDE.none, TOWER_SIDE.moon),
            TowerCard(COLOR.blue, 3, TOWER_SIDE.moon, TOWER_SIDE.both),
            TowerCard(COLOR.blue, 4, TOWER_SIDE.moon, TOWER_SIDE.moon),
            TowerCard(COLOR.blue, 5, TOWER_SIDE.moon, TOWER_SIDE.none),
            TowerCard(COLOR.green, 3, TOWER_SIDE.sun, TOWER_SIDE.both),
            TowerCard(COLOR.green, 4, TOWER_SIDE.sun, TOWER_SIDE.sun),
            TowerCard(COLOR.green, 5, TOWER_SIDE.sun, TOWER_SIDE.none),
            TowerCard(COLOR.brown, 3, TOWER_SIDE.both, TOWER_SIDE.sun),
            TowerCard(COLOR.brown, 4, TOWER_SIDE.moon, TOWER_SIDE.sun),
            TowerCard(COLOR.brown, 5, TOWER_SIDE.none, TOWER_SIDE.sun)
        ]

    def add_happy_deck(self):
        self.cards += [HappyCard()
                      for i in range(4)]
        
    def add_crossroads_deck(self):
        self.cards += (
            [DeadendCard() for i in range(10)]
            + [SunCard(COLOR.rainbow) for i in range(3)]
            + [MoonCard(COLOR.rainbow) for i in range(2)]
            + [KeyCard(COLOR.rainbow)]
        )
        
        
    def add_lost_dreams_deck(self):
        # 4 lost dreams  (or is it 8?)
        self.cards += [LostCard() for i in range(4)]

    def add_denizens(self):
        self.cards += [DenizenCard(d)
                      for d in DENIZEN_TYPES
                      for i in range(2)]
        self.cards += [DoorCard(COLOR.oni)]


def butts():
    x = {k:v for k,v in sf.Keyboard.__dict__.items() if isinstance(v, int)}
    pprint(sorted(x.items(), key=lambda y : y[1]))

def go():
    Onirim().play()
if __name__=="__main__":
    # if "y" in input("Run Onirim().play()? (y/n) >> "):
        go()
