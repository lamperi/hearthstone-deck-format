# hearthstone-deck-format

Note: HearthSim developers figured it all. See https://github.com/HearthSim/python-hearthstone/blob/master/hearthstone/deckstrings.py
I have changed my repository to reflect correct format in case someone finds this.

# My research with corrections from HearthSim algorithms

Findings about Hearthstone deck format

Example code Blizzard posted: `AAECAR8GxwPJBLsFmQfZB/gIDI0B2AGoArUDhwSSBe0G6wfbCe0JgQr+DAA=`

The code is base64 encoded. After decoding, bytes can be inspected:

    b0 b1 b2 | b3     | b4           | b5     | b6 .. b17      | b18    | b19 .. b42     | b43
    0  1  2  | 1      | 1f           | 6      | c7 .. f8       | c      | 8d  .. c       | 0
    header   | length | hero payload | length | 1 card payload | length | 2 card payload | footer

## Header

Header contains three bytes. First byte should be 0. Second byte denotes the format version and is currently 1. Third byte denotes format, with value 1 meaning Wild and 2 Standard.

## Hero / Card payload

Card set payload contains integers in varint format, meaning card ID takes a variable number of bytes in the payload. For better description, see https://developers.google.com/protocol-buffers/docs/encoding

    b6       | b7
    c7       | 3
    11000111 | 00000011
    
Since b6 has 1 in most significant bit, next byte should also be used to form the number. In b7 most significant bit is 0 so the number ends there. This means, that of first byte, seven least significant bits form the lowest bits for card ID. From second byte, again seven least significants bits are counted for the number, but of course shifted.

    card id = (first & 0x7f) | (second << 7)
	card id =  0000011 1000111

In case of bytes 6 and 7, card id is 455. Checking from https://github.com/HearthSim/hsdata, it matches Snake Trap. 

Hero payload can contain from the format more than one hero, but more than one hero do not make any sense from deck perspective.

1 card payload contains cards that are included once in the deck. 2 card payload contains cards that are included twice in the deck.

## Footer

Footer needs to be 0. It just means that the card data has ended.
