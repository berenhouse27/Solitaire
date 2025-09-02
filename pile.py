# Stack most logical for building card piles since cards are taken top to bottom
from card import Card
from typing import Any
from color_card import color_card

class Stack:
    def __init__(self):
        self.stack: list[Any] = []


    def push(self, card: Card)  -> None:
        self.stack.append(card)

    def pop(self) -> Any:
        return self.stack.pop()

    def clear(self) -> None:
        self.stack = []

    def length(self) -> int:
        return len(self.stack)

    def seek(self, index) -> Any:
        return self.stack[index]

    def peek(self) -> Any:
        if self.length():
            return self.stack[-1]
        else:
            return 0

    def show(self) -> None:
        print([str(x) for x in self.stack])

# Holds flipped/unflipped piles and must only accept king if empty
# or a card with opposite color and -1 rank
class Pile:
    def __init__(self, id: int, DEBUG: bool = False):
        self.id = id
        self.unflipped = Stack()
        self.flipped = Stack()
        self.DEBUG: bool = DEBUG

    def reset(self) -> None:
        self.unflipped.clear()
        self.flipped.clear()

    def push_unflip(self, card: Card) -> None:
        self.unflipped.push(card)

    def flip(self) -> None:  # Flip card if none in flipped and cards in unflipped
        if (self.flipped.peek() == 0) and (self.unflipped.peek() != 0):
            self.flipped.push(self.unflipped.pop())

    def test(self, card: Card) -> bool|None: # Test compatability of cards
        top = self.flipped.peek()
        if self.DEBUG:
            print(f"[DEBUG] BEGINNING TEST {color_card(card)} onto {color_card(top)}")
        if (self.unflipped.peek() == 0) and (top == 0) and (card.rank == 13):
            if self.DEBUG:
                print("[DEBUG] PASS")
            return True   # succeeds if unflipped/flipped are empty and card is king
        elif top != 0: # if cards are in flipped
            if top.rank == 14:
                if self.DEBUG:
                    print(f"[DEBUG] TEST FAILED")
                return False  # if top card is an ace, nothing can be placed
            elif (card.color != top.color) and (card.rank == top.rank - 1):
                if self.DEBUG:
                    print(f"[DEBUG] TEST PASSED")
                return True # if card rank one less and color doesn't match, test succeeds
            else:
                if self.DEBUG:
                    print(f"[DEBUG] TEST FAILED")
                return False
        else:
            if self.DEBUG:
                print(f"[DEBUG] TEST FAILED")
            return False

    def add_to_flipped(self, card: Card) -> None:
        self.flipped.push(card)

    def remove_from_flipped(self) -> Card:
        return self.flipped.pop()

    def show_flipped(self) -> None:
        print("---------------------------")
        print(f"PILE {self.id}:")
        for card in self.flipped.stack:
            print(str(card))
        print("---------------------------")

    def _show_unflipped(self) -> None:
        print("---------------------------")
        for card in self.unflipped.stack:
            print(str(card))
        print("---------------------------")


# Holds cards after scoring and must only accept same suit and +1 rank
class AceStack(Stack):
    def __init__(self):
        super().__init__()
        self.suit: str = 'None'

    def test(self, card: Card) -> bool:
        if isinstance(card, Card):
            if (card.rank == 14) and (self.suit == 'None'):
                self.suit = card.suit
                return True # if card is an ace nothing inside, add ace and take on its suit
            else:
                top_card = self.peek()
                if top_card:
                    if card.suit == self.suit:  # Cards must be same suit
                        if (top_card.rank == 14) and (card.rank == 2):
                            return True # if the top card is an ace, accept a 2 (needed since 2 != 1+14)
                        elif card.rank == top_card.rank + 1:
                            return True # accept card if rank is one higher than top rank
        return False

    def reset(self) -> None:
        self.suit = 'None'
        self.stack.clear()

    def push(self, card: Card) -> bool:
        test = self.test(card)
        if test:
            super().push(card)
        return test







