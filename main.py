import re
import json
import praw
from collections import defaultdict
from itertools import chain

from models import Card, Ability, Trap, Spell, Unit
from typing import List, Tuple, Dict, Set

# reddit = praw.Reddit(...)
extended_pattern = re.compile(r'(?<!<)<{2}([a-z]+)>{2}(?!>)')  # <<Draven>>
regular_pattern = re.compile(r'(?<!\[)\[{2}([a-z]+)\]{2}(?!\])')  # [[Draven]]
file_name = 'cards.json'


def bot_login():
    # Login with praw
    print("Logging in...")
    reddit = praw.Reddit(username='aes110',
                         password='',
                         client_id='',
                         client_secret='',
                         user_agent="Reddit bot")
    print("Logged in!")
    return reddit


def get_cards_dicts() -> Tuple[Dict[str, Card], Dict[str, Card]]:
    with open(file_name) as f:
        cards = json.load(f)

    types = {'Spell': Spell, 'Unit': Unit, 'Ability': Ability, 'Trap': Trap}
    my_cards = [types[card['type']](**card) for card in cards]

    # There are times where multiple cards have the same name, like Champions lv1/2
    name_to_cards = defaultdict(list)
    for card in my_cards:
        name_to_cards[card.name.lower()].append(card)

    code_to_card = {card.cardCode: card for card in my_cards}
    return name_to_cards, code_to_card


def get_list_of_cards(names: List[Tuple[str, bool]], cards) -> Set[str]:
    found = []
    for card, expended in names:
        if expended:
            found += list(chain.from_iterable([i.associatedCardRefs for i in cards[card]]))
        else:
            found += [i.cardCode for i in cards[card]]

    return set(found)


def extract_wanted_cards(comment_body: str) -> List[Tuple[str, bool]]:
    cards = []
    for match in regular_pattern.findall(comment_body):
        cards.append((match, False))

    for match in extended_pattern.findall(comment_body):
        cards.append((match, True))

    return cards


def build_comment(cards: Dict[str, List[Card]], cards_by_code: Dict[str, Card]):
    comment = ""
    for card_list in cards.values():

        # #### Lux - Unit (2 Cards)
        comment += f"##### {card_list[0].name} - {card_list[0].type} " \
                   f"({len(card_list)} Card{'s' if len(card_list) > 1 else ''})\n  "

        comment += "-----\n  "

        # Region: Demacia | Subtype: | Rarity: Champion
        # Some alternate versions dont have all the info, so search for one of the list that has it
        comment += f">**Region**: {next((card.region for card in card_list if card.region != ''), 'None')} | " \
                   f"**Subtype**: {next((card.subtype for card in card_list if card.subtype != ''), 'None')} | " \
                   f"**Rarity**: {next((card.rarity for card in card_list if card.rarity != ''), 'None')}\n  "

        comment += "_____\n  "

        # 1. Cost: 6 | Attack: 4 | Health: 5 | Keywords: Barrier
        #    Description: When I've seen you spend 6+ mana on spells, create a Fleeting Final Spark in hand.
        #    Level Up: When I've seen you spend 6+ mana on spells, create a Fleeting Final Spark in hand.

        for index, card in enumerate(card_list, start=1):
            comment += f">>{index}. {card.get_comment()}  \n  "
            comment += "&nbsp;\n  "

        # Related: Final Spark ,Lux's Prismatic Barrier ,Lux

        comment += f"\n  \n  >**Related**: " \
                   f"{', '.join([cards_by_code[card].name for card in card_list[0].associatedCardRefs])}"

        comment += "\n  \n  &nbsp;\n  \n  \n"

    comment += "I'm a bot :). Use [[card]] or <<expended>> to call me. | " \
               "[Code](https://github.com) | " \
               "[Report Bug](https://google.com)"

    return comment


def main():
    # reddit = bot_login()
    cards_by_name, cards_by_code = get_cards_dicts()
    # for comment in reddit.subreddit('LegendsOfRuneterra').stream.comments(skip_existing=True):
    comment = "Hello, i want <<darius>> , also [[lux]] weqw"
    extracted_cards = extract_wanted_cards(comment)  # TODO comment.body
    cards_to_get = get_list_of_cards(extracted_cards, cards_by_name)

    final_cards = defaultdict(list)
    for card_code in cards_to_get:
        card = cards_by_code[card_code]
        final_cards[card.name].append(card)

    return final_cards


if __name__ == '__main__':
    main()
