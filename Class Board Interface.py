Python 3.11.3 (v3.11.3:f3909b8bc8, Apr  4 2023, 20:12:10) [Clang 13.0.0 (clang-1300.0.29.30)] on darwin
Type "help", "copyright", "credits" or "license()" for more information.

import random

# Define the Space class
class Space:
    def __init__(self, name, space_type, price=0, rent=0):
        self.name = name
        self.space_type = space_type  # e.g., 'property', 'chance', 'community_chest', etc.
        self.price = price
        self.rent = rent
        self.owner = None

    def __repr__(self):
        return f"{self.name} ({self.space_type})"

# Define the Player class
class Player:
    def __init__(self, name):
        self.name = name
        self.position = 0  # Start at 'Go'
        self.balance = 1500  # Starting balance
        self.properties = []
        self.get_out_of_jail_free = False  # Boolean for 'Get Out of Jail Free' card

    def move(self, steps, board_size):
        self.position = (self.position + steps) % board_size
        print(f"{self.name} moves to position {self.position}")

# Define Chance and Community Chest cards with scaled probabilities
chance_cards = [
    {'description': 'Advance to Go', 'action': 'advance_to_go', 'probability': 1},
    {'description': 'Go to Jail', 'action': 'go_to_jail', 'probability': 1},
    {'description': 'Bank pays you dividend of $50', 'action': 'receive_money', 'amount': 50, 'probability': 2},
    {'description': 'Get Out of Jail Free', 'action': 'get_out_of_jail_free', 'probability': 1},
    # Add more cards as needed
]

community_chest_cards = [
    {'description': 'Doctor\'s fees. Pay $50', 'action': 'pay_money', 'amount': 50, 'probability': 2},
    {'description': 'From sale of stock you get $45', 'action': 'receive_money', 'amount': 45, 'probability': 2},
    {'description': 'Get Out of Jail Free', 'action': 'get_out_of_jail_free', 'probability': 1},
    {'description': 'Go to Jail', 'action': 'go_to_jail', 'probability': 1},
    # Add more cards as needed
]

# Function to build a deck with scaled probabilities
def build_deck(cards):
    deck = []
    for card in cards:
        deck.extend([card] * card['probability'])
    random.shuffle(deck)
    return deck

# Build the decks
chance_deck = build_deck(chance_cards)
community_chest_deck = build_deck(community_chest_cards)

# Function to draw a card from a deck
def draw_card(deck, player):
    if not deck:
        # Rebuild and reshuffle the deck if empty
        deck = build_deck(chance_cards if deck == chance_deck else community_chest_cards)
    card = deck.pop()
    print(f"{player.name} draws a card: {card['description']}")
    execute_card_action(card, player)
    return deck  # Return the deck in case it was rebuilt

# Function to execute the action of a card
def execute_card_action(card, player):
    action = card['action']
    if action == 'advance_to_go':
        player.position = 0
        print(f"{player.name} advances to Go!")
    elif action == 'go_to_jail':
        player.position = find_space('Jail')
        print(f"{player.name} goes to Jail!")
    elif action == 'receive_money':
        amount = card['amount']
        player.balance += amount
        print(f"{player.name} receives ${amount}. New balance: ${player.balance}")
    elif action == 'pay_money':
        amount = card['amount']
        player.balance -= amount
        print(f"{player.name} pays ${amount}. New balance: ${player.balance}")
    elif action == 'get_out_of_jail_free':
        player.get_out_of_jail_free = True
        print(f"{player.name} receives a 'Get Out of Jail Free' card!")

# Helper function to find the position of a space by name
def find_space(name):
    for idx, space in enumerate(board):
        if space.name == name:
            return idx
    return -1  # Return -1 if not found

# Create the game board
board = [
    Space('Go', 'go'),
    Space('Mediterranean Avenue', 'property', price=60, rent=2),
    Space('Community Chest', 'community_chest'),
    Space('Baltic Avenue', 'property', price=60, rent=4),
    Space('Income Tax', 'tax'),
    Space('Reading Railroad', 'railroad', price=200, rent=25),
    Space('Chance', 'chance'),
    Space('Oriental Avenue', 'property', price=100, rent=6),
    Space('Jail', 'jail'),
    # Continue adding spaces to complete the board
]
