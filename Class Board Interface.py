Python 3.11.3 (v3.11.3:f3909b8bc8, Apr  4 2023, 20:12:10) [Clang 13.0.0 (clang-1300.0.29.30)] on darwin
Type "help", "copyright", "credits" or "license()" for more information.
import random

class Space:
    def __init__(self, name, space_type):
        self.name = name
        self.space_type = space_type

class Property(Space):
    def __init__(self, name, price, color):
        super().__init__(name, "Property")
        self.price = price
        self.color = color
        self.owner = None

def create_board():
    board = []
    # Add properties, railroads, utilities, chance/community chest, etc.
    board.append(Space("Go", "Go"))
    board.append(Property("Mediterranean Avenue", 60, "Brown"))
    return board

def roll_dice():
    return random.randint(1, 6) + random.randint(1, 6)

if __name__ == "__main__":
    board = create_board()
    # Game logic here
