import re
import json
import praw

from models import Card, Ability, Trap, Spell, Unit
from typing import List, Tuple, Dict

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

    # card_dicsts = defaultdict(lambda : [])
    name_to_card = {card.name.lower(): card for card in my_cards}
    code_to_card = {card.cardCode: card for card in my_cards}
    return name_to_card, code_to_card


def main():
    reddit = bot_login()
    for comment in reddit.subreddit('LegendsOfRuneterra').stream.comments(skip_existing=True):
        print(comment)


if __name__ == '__main__':
    main()
