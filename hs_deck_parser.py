import base64
"""
Hearthstone deck format utility

See https://github.com/lamperi/hearthstone-deck-format/blob/master/README.md

Card IDs extracted from https://github.com/HearthSim/hsdata
"""

card_database = {
 141: "Hunter's Mark",
 216: 'Bloodfen Raptor',
 296: 'Kill Command',
 437: 'Animal Companion',
 455: 'Snake Trap',
 519: 'Freezing Trap',
 585: 'Explosive Trap',
 658: "Leper's Gnome",
 699: 'Tundra Rhino',
 877: 'Arcade Shot',
 921: 'Jungle Panther',
 985: 'Dire Wolf Alpha',
 1003: 'Houndmaster',
 1144: 'King Krush',
 1243: 'Unleash the Hounds',
 1261: 'Savannah Highmane',
 1281: 'Scavenging Hyena',
 1662: 'Eaglehorn Bow'
}

def parse_cardlist(data, length, offset):
    """
    Parse cardlist from data. 
    """
    card_names = []
    for i in range(offset, offset + 2 * length, 2):
        card_id = (data[i] & 0x7f) | (data[i+1] << 7)
        card_names.append(card_database[card_id])
    return card_names
    
def parse_deck(deck_code):
    """
    Parse decklist from base64 encoded string.
    """
    data = base64.b64decode(example_deck_code)
    header = data[0:5]
    length_index = 5
    once_cards = parse_cardlist(data, data[length_index], length_index+1)
    length_index += 1 + 2*data[length_index]
    twice_cards = parse_cardlist(data, data[length_index], length_index+1)
    return (header, once_cards, twice_cards)
  
if __name__ == "__main__":
    example_deck_code = "AAECAR8GxwPJBLsFmQfZB/gIDI0B2AGoArUDhwSSBe0G6wfbCe0JgQr+DAA="
    header, once, twice = parse_deck(example_deck_code)
    for name in once:
        print("1x {}".format(name))
    for name in twice:
        print("2x {}".format(name))
