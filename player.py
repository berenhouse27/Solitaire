from card import Card
from pile import Pile
from solitaireBoard import SolitaireBoard

class Player:
    def __init__(self):
        self.board = SolitaireBoard()

    def initialize_board(self) -> None:
        self.board.initialize_board()

    def check_if_int(self, user_input: str) -> int:
        if (len(user_input) == 1) and (48 <= ord(user_input) <= 56):
                return int(user_input)
        else:
            return 0

    def place_drawn(self, target_id: int) -> None:
        card: Card = self.board.deck.drawn_cards[-1]
        if 1 <= target_id <= 7:
            destination: Pile = self.board.card_piles[target_id - 1]
            if destination.test(card):
                destination.add_to_flipped(card)
                self.board.deck.drawn_cards.pop(-1)
        elif target_id == 8:
            self.score_from_drawn()

    def score_from_drawn(self) -> None:
        card: Card = self.board.deck.drawn_cards[-1]
        if self.board.score(card):
            self.board.deck.drawn_cards.pop(-1)
            self.board.deck.deal_card()

    def score_from_pile(self,pile_id: int) -> None:
        start: Pile = self.board.card_piles[pile_id-1]
        card: Card = start.flipped.peek()
        if self.board.score(card):
            start.remove_from_flipped()

    def move(self, pile_id: int, target_id: int) -> None:
        self.board.move(pile_id, target_id)

    def assign(self, pile_id: int, target_id: int) -> None:
        if pile_id == 0:
            self.board.move_king(pile_id, pile_id)
            self.board.deck.deal_card()
        elif 1 <= pile_id <= 7:
            self.board.move_king(pile_id, pile_id)

    def user_choice(self) -> str:
        print("Choose Action:\n"
              "P) Place from hand\n"
              "M) Move from board\n"
              "D) Draw card\n"
              "R) Reset board\n"
              "E) Exit")
        return input("Answer (p/m/d/e): ")

    def update_board(self) -> None:
        self.board.print_all()
        answer = self.user_choice()
        if answer == "p":
            destination = self.check_if_int(input("Target Row (1-7=rows,8=score): "))
            self.place_drawn(destination)
        elif answer == "m":
            start = self.check_if_int(input("Starting Row (1-7=rows): "))
            destination = self.check_if_int(input("Target Pos (1-7=rows,8=score): "))
            if 1 <= destination <= 7:
                self.move(start, destination)
            elif destination == 8:
                self.score_from_pile(start)
        elif answer == "d":
            self.board.deck.deal_card()
        elif answer == "r":
            self.board.initialize_board()
        elif answer == "e":
            print("------------------------\n"
                  "Thank you for playing!\n"
                  "------------------------")
            exit()

