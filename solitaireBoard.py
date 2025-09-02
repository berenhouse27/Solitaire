from unittest import case

from card import Card, Deck
from pile import Pile, AceStack
from color_card import color_card

class SolitaireBoard:
    def __init__(self, DEBUG: bool = False):
        self.deck: Deck = Deck()
        self.deck.create()
        self.move_count: int = 0
        self.DEBUG: bool = DEBUG

        self.card_piles: list[Pile] = []  # Collection of 7 card piles
        for i in range(1,8):
            self.card_piles.append(Pile(i))

        self.ace_piles: list[AceStack] = []  # Collection of 4 ace piles
        for n in range(4):
            self.ace_piles.append(AceStack())

    def _DEBUG(self, func_name: str, card: Card = None,
               pile_1: list[Card] = [], pile_2: list[Card] = []) -> None:

         self.card_piles[0].flipped.clear()
         self.card_piles[1].flipped.clear()
         self.card_piles[0].unflipped.clear()
         self.card_piles[1].unflipped.clear()
         self.card_piles[0].DEBUG = True
         self.card_piles[1].DEBUG = True

         if len(pile_1) > 0:
             pile_1.reverse()
             for card in pile_1:
                 self.card_piles[0].flipped.push(card)
         if len(pile_2) > 0:
             pile_2.reverse()
             for card in pile_2:
                 self.card_piles[1].flipped.push(card)

         match func_name:
             case 'place':
                 print('[DEBUGGING] place()')
                 self.place(card, 1)
             case 'move':
                 print('[DEBUGGING] move()')
                 self.move(1, 2)
             case 'move_king':
                 print('[DEBUGGING] move_king()')
                 self.move_king(1, 2)

    # Place card onto flipped pile
    def place(self,card: Card, pile_id: int) -> bool:
        target: Pile = self.card_piles[pile_id-1]
        if self.DEBUG:
            print(f'[DEBUG] Attempting to place {color_card(card)} on Pile {pile_id}')
        if target.test(card):
            self.deck.drawn_cards.remove(card)
            target.add_to_flipped(card)
            if self.DEBUG:
                print(f'[DEBUG] {color_card(card)} successfully placed on Pile {pile_id}')
            return True
        else:
            if self.DEBUG:
                print(f"[DEBUG] Failed to place {color_card(card)} on Pile {pile_id}")
            return False

    # Place card onto ace pile
    def score(self, card: Card) -> bool:
        for stack in self.ace_piles:
            if stack.push(card) == 1:
                if self.DEBUG:
                    print(f"[DEBUG] {color_card(card)} successfully scored")
                return True
        if self.DEBUG:
            print(f"[DEBUG] Failed to score {color_card(card)}")
        return False

    # Test if cards can be moved from one row to another
    def test_move(self, pile_id: int, target_id: int) -> Card|bool:
        start = self.card_piles[pile_id-1]
        target = self.card_piles[target_id-1]
        if self.DEBUG:
            print(f'[DEBUG] TESTING MOVE Pile {pile_id} to Pile {target_id}')
        for card in start.flipped.stack:
            if target.test(card):   # Only one possible card can fulfill conditions from a given row
                print(f'[DEBUG] MOVE TEST PASSED')
                return card    # returns card in starting pile that acts as the head for moving
        print(f'[DEBUG] MOVE TEST FAILED')
        return False

    # Move group of cards from one row to another
    def move(self, pile_id: int, target_id: int) -> bool:
        leader = self.test_move(pile_id, target_id) # Card from starting row
        if not leader:
            return False
        start = self.card_piles[pile_id - 1]
        destination = self.card_piles[target_id - 1]
        if self.DEBUG:
            print(f'[DEBUG] Attempting to move Pile {pile_id} to Pile {target_id} from {color_card(leader)}')
                                      # if leader card exists, continue
        holding = []                   # holding stack used to maintain proper order of cards
        for card in start.flipped.stack:    # run through start flipped cards
            if card.rank <= leader.rank:
                holding.append(card)
        for card in range(len(holding)):
            if self.DEBUG:
                print(f'[DEBUG] {color_card(holding[0])} moved from Pile {pile_id} to Pile {target_id}')
            start.remove_from_flipped()
            destination.add_to_flipped(holding.pop(0))
        if self.DEBUG:
            print(f'[DEBUG] All Cards Moved')
        return True

    def move_king(self, pile_id: int, target_id: int) -> bool:
        destination = self.card_piles[target_id - 1]
        if self.DEBUG:
            print(f'[DEBUG] Attempting to move king')
        if pile_id == 0:
            hand = self.deck.drawn_cards
            card = hand[-1]
            if destination.test(card):
                destination.add_to_flipped(card)
                hand.pop()
        if 1 <= pile_id <= 7:
            start = self.card_piles[pile_id-1]
            king_card = start.flipped.seek(0)
            if destination.test(king_card):
                holding = []
                for card in start.flipped.stack:
                    holding.append(card)
                for card in range(len(holding)):
                    destination.add_to_flipped(holding.pop(0))
                    start.remove_from_flipped()
                if self.DEBUG:
                    print(f'[DEBUG] King Moved')
                return True
            else:
                if self.DEBUG:
                    print(f'[DEBUG] King Not Moved')
                return False
        else:
            if self.DEBUG:
                print(f'[DEBUG] King Not Moved')
            return False

    def success(self) -> bool:
        for stack in self.ace_piles:
            card: Card = stack.peek()
            if card:
                if card.rank != 13:
                    return False
                else:
                    return True
        return False

    def print_ace_piles(self):
        print("SCORED CARDS: ", end = '')
        print("|", end = '')
        for stack in self.ace_piles:
            top = stack.peek()
            if top:
                print(str(color_card(top)), end ='')
            else:
                print("   ", end = '')
            print("|", end = '')
        print(f"    Move Count: {self.move_count}")

    def print_title(self):
        space = 18
        for i in range(7):
            text = f"ROW {self.card_piles[i].id} ({self.card_piles[i].unflipped.length()} LEFT)"
            print(text, end = '')
            for n in range(space - len(text)):
                print(' ', end = '')
            print(" | ", end = '')
        print("\n-------------------------------------------------------------------------------------------------------------------------------------------------------")

    def print_column(self):
        self.print_title()
        space = 18
        for pile in self.card_piles:
            pile.flip()
        for i in range(12):
            for pile in self.card_piles:
                pile_length = pile.flipped.length()
                if pile_length > i:
                    card = pile.flipped.seek(i)
                    print(color_card(card), end =' ')
                    for n in range(space - len(str(card))):
                        print(' ', end='')
                    print('| ', end='')
                else:
                    for n in range(space):
                        print(' ', end = '')
                    print(' | ', end='')
            print('')

    def print_all(self):
        print("*******************************************************************************************************************************************************")
        self.print_column()
        self.print_ace_piles()
        if self.deck.drawn_cards:
            card: Card = self.deck.drawn_cards[-1]
            print(f"NEXT CARD ({len(self.deck.undrawn_cards)}/{len(self.deck.drawn_cards)+len(self.deck.undrawn_cards)}): {color_card(card)}")
        self.move_count += 1

    def print_success(self) -> bool:
        if self.success():
            print(f"------------------------------------------------------------------\n"
                  f"*****************************************************************\n"
                  f"Congratulations! There are no more cards left\n"
                  f"       You completed the game in {self.move_count} moves\n"
                  f"*****************************************************************\n"
                  f"------------------------------------------------------------------")
            return True
        else:
            return False

    def initialize_board(self):
        self.deck.create()
        for card_pile in self.card_piles:
            card_pile.reset()
        for ace_pile in self.ace_piles:
            ace_pile.reset()
        self.deck.shuffle()
        for i in range(8):
            for pile in self.card_piles:
                if pile.id > i:
                    card = self.deck.take_card()
                    pile.push_unflip(card)
        for pile in self.card_piles:
            pile.flip()
        self.deck.deal_card()



def main() -> None:
    board = SolitaireBoard(DEBUG = True)
    board.initialize_board()
    cards_1: list[Card] = []
    cards_2: list[Card] = []
    for i in range(1, 13):
        if i % 2 == 0:
            cards_1.append(Card('Diamonds',i))
        else:
            cards_1.append(Card('Clubs',i))
    for i in range(6, 14):
        if i % 2 != 0:
            cards_2.append(Card('Clubs',i))
        else:
            cards_2.append(Card('Diamonds',i))

    board._DEBUG('move', pile_1 = cards_1, pile_2 = cards_2)
    board.print_all()


if __name__ == '__main__':
    main()