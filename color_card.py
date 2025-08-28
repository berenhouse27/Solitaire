from card import Card

def color_card(card: Card) -> str:
    if isinstance(card, Card):
        if card.color == 'red':
            color = '\033[31m'
            reset = '\033[0m'
        else:
            color = ''
            reset = ''
        return f'{color}{str(card)}{reset}'
    else:
        return f'{card}'