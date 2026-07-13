import random

COLORS = ["Red", "Green", "Blue", "Yellow"]
NUMBERS = list(range(0, 10))
ACTIONS = ["Skip", "Reverse", "Draw Two"]
WILDS = ["Wild", "Wild Draw Four"]

    

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

def draw_card(deck):
        if not deck:
            raise ValueError("No cards left in the deck")
        return deck.pop()

def make_game_state(num_players):
    return {
        "num_players": num_players,
        "players": [],
        "hands": {},
        "deck": make_deck(),
        "discard": [],
        "turn_index": 0,
        "direction": 1,
        "active_color": None,
    }

def add_player(state, sock, name):
    state["players"].append((sock, name))
    state["hands"][name] = []

def current_player_name(state):
    players = state["players"]
    if not players:
        return None
    return players[state["turn_index"]][1]

def advance_turn(state, steps=1):
    """Move turn_index forward by 'steps' player-slots, respecting direction."""
    n = len(state["players"])
    state["turn_index"] = (state["turn_index"] + steps * state["direction"]) % n

def deal_hands(state, cards_each=7):
    """Deal  cards_each cards to every registered player."""
    for _, name in state["players"]:
        state["hands"][name] = [draw_card(state["deck"]) for _ in range(cards_each)]

def is_valid_play(top_color, top_value, card):
    """Return True if `card` can legally be played on top of `top_card`.

    Rules:
    - Wild cards (color is None) can always be played.
    - Otherwise the card must match the top card's color OR its value
      (number or action name).
    """
    color, value = card

    if color is None:
        return True
    if color == top_color:
        return True
    if value == top_value:
        return True
    return False

def parse_card(tokens):
    """Convert a list of command tokens (everything after 'PLAY') into a
    card tuple, or return None if the tokens don't describe a real card.

    Examples of valid input:
        ["Red", "5"]          -> ("Red", 5)
        ["Blue", "Skip"]      -> ("Blue", "Skip")
        ["Green", "Draw", "Two"] -> ("Green", "Draw Two")
        ["Wild"]              -> (None, "Wild")
        ["Wild", "Draw", "Four"] -> (None, "Wild Draw Four")
    """
    if not tokens:
        return None

    if tokens[0] == "Wild":
        rest = " ".join(tokens[1:]).strip()
        if rest == "":
            return (None, "Wild")
        if rest == "Draw Four":
            return (None, "Wild Draw Four")
        return None
    
    color = tokens[0]
    if color not in COLORS:
        return None

    value_str = " ".join(tokens[1:]).strip()
    if value_str == "":
        return None

    if value_str.isdigit():
        return (color, int(value_str))
    if value_str in ACTIONS:
        return (color, value_str)

    return None