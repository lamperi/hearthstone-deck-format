# hearthstone-deck-format
Findings about Hearthstone deck format

Example code Blizzard posted: `AAECAR8GxwPJBLsFmQfZB/gIDI0B2AGoArUDhwSSBe0G6wfbCe0JgQr+DAA=`

The code is base64 encoded. After decoding, bytes can be inspected:

    b0 b1 b2 b3 b4 | b5     | b6 .. b17          | b18    | b19 .. b42         | b43
    0  1  2  1  1f | 6      | c7 .. f8           | c      | 8d  .. c           | 0
    header         | length | card set 1 payload | length | card set 2 payload | footer

## Header

I suspect header contains data for class, format (standard / wild) and maybe character. There can also be magic bytes to aid detecting card format: maybe first bytes are always 0, 1, 2.

## Card payload

Card set payload seems to contains two bytes for each card, for example bytes b6 & b7

    b6       | b7
    c7       | 3
    11000111 | 00000011
    
Of first byte, seven least significant bits seem to form the lowest bit for card ID. From second byte, it seems like all bytes can be used to form card ID:

    card id = (first & 0x7f) | (second << 7)

In case of bytes 6 and 7, card id is 455. Checking from https://github.com/HearthSim/hsdata, it matches Snake Trap. 

Card set 1 contains cards that are included once in the deck. Card set 2 contains cards that are included twice in the deck.

The first bit in card data seems to be always 1 in the example data. This could indicate that the cards are all golden or non golden. It would be also possible to embed the count of golden and non golden cards into most significant bits of second byte. More examples and verification if cards are golden is needed.

## Footer

For this deck it is 0. It can just mean that the card data has ended.
