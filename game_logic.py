import random

COLORS = ["Red", "Green", "Blue", "Yellow"]
NUMBERS = list(range(0, 10))
ACTIONS = ["Skip", "Reverse", "Draw Two"]
WILDS = ["Wild", "Wild Draw Four"]

class Card:
    def __init__(self, color, value):
        self.color = color
        self.value = value
    def __str__(self):
        return f"{self.color} {self.value}" if self.color else self.value
    
class Deck:
    def __init__(self):
        self.cards = []
        for color in COLORS:
            for n in NUMBERS:
                self.cards.append(Card(color, n))
                if n != 0:
                    self.cards.append(Card(color, n))
            for a in ACTIONS:
                self.cards.extend([Card(color, a), Card(color, a)])
        for w in WILDS:
            self.cards.extend([Card(None, w) for _ in range(4)])
        random.shuffle(self.cards)

def card_str(card):
    color, value = card
    return f"{color} {value}" if color else str(value)

def make_deck():
    cards = []
    for color in COLORS:
        for n in NUMBERS:
            cards.append((color, n))
            if n != 0:
                cards.append((color, n))
        for a in ACTIONS:
            cards.append((color, a))
            cards.append((color, a))
    for w in WILDS:
        for _ in range(4):
            cards.append((None, w))
    random.shuffle(cards)
    return cards

def draw_card(self):
        if not self.cards:
            raise ValueError("No cards left in the deck")
        return self.cards.pop()

def make_game_state(num_players):
    return {
        "num_players": num_players,
        "players": [],
        "hands": {},
        "deck": make_deck(),
        "discard": [],
        "turn_index": 0,
    }
