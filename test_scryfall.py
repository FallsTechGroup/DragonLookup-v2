import scrython
cards = []
cards_strings = ["Bitterbow Sharpshooter", "Ambush Paratrooper", "Calamaty's Wake"]
for card in cards_strings:
    card_data = scrython.cards.Named(fuzzy=card)
    cards.append(card_data)
    print(card_data.name())