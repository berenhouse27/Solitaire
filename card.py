import random
from dataclasses import dataclass, field

# Card object holds three pieces of data: rank, suit, and color

class Card:
    def __init__(self, suit: str, rank: int):
        self.suit: str = suit
        self.rank: int = rank
        if suit == 'Diamonds' or suit == 'Hearts':
            self.color = 'red'
        else:
            self.color = 'black'

    def __str__(self) -> str:
        if self.rank < 11:
            label = f'{self.rank} of {self.suit}'
        elif self.rank == 11:
            label = f'Jack of {self.suit}'
        elif self.rank == 12:
            label = f'Queen of {self.suit}'
        elif self.rank == 13:
            label = f'King of {self.suit}'
        elif self.rank == 14:
            label = f'Ace of {self.suit}'
        else:
            label = 'NONE'
        return f"{label}"

class Deck:
    def __init__(self):
        self.undrawn_cards: list[Card] = []
        self.drawn_cards: list[Card] = []
        self.rank_list: list[int] = [2,3,4,5,6,7,8,9,10,11,12,13,14]
        self.suit_list: list[str] = ["Clubs", "Diamonds", "Hearts", "Spades"]
        self.create()

    # Create 52 card deck
    def create(self) -> None:
        self.undrawn_cards = []
        for suit in self.suit_list:
            for rank in self.rank_list:
                card: Card = Card(suit, rank)
                self.undrawn_cards.append(card)

    def reset(self) -> None:
        self.drawn_cards = []
        self.create()

    def shuffle(self) -> None:
        for i in range(len(self.drawn_cards)):
            card: Card = self.drawn_cards.pop()
            self.undrawn_cards.append(card)
        random.shuffle(self.undrawn_cards)

    # Remove card entirely (used when placing cards directly from deck to board)
    def take_card(self) -> Card:
        card: Card = self.undrawn_cards.pop(0)
        return card

    # Move card from deck to drawn pile
    def deal_card(self) -> Card|None:
        if len(self.undrawn_cards) > 0:
            card: Card = self.undrawn_cards.pop(0)
            self.drawn_cards.append(card)
            return card
        else:
            self.undrawn_cards = self.drawn_cards
            self.drawn_cards = []
            if len(self.undrawn_cards) != 0:
                card: Card = self.undrawn_cards.pop(0)
                self.drawn_cards.append(card)

    def add_to_deck(self, card: Card) -> None:
        self.undrawn_cards.append(card)
        if card in self.drawn_cards:
            self.drawn_cards.remove(card)

