from models import Card

from typing import List

def card_from_card_code(code: str, cards: List[Card]) -> Card:
    return next((card for card in cards if card.cardCode == co), None)