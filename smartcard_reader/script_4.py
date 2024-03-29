"""
Custom CardTypes

Custom CardTypes can be created, e.g. a card type that checks the ATR and the historical bytes of the card.
To create a custom CardType, derive your CardType class from the CardType base class (or any other CardType) and
override the matches() method.
For example to create a DCCardType that will match cards with the direct convention (first byte of ATR to 0x3b)

Scripts written with the card-centric approach fixes the problems of the reader-centric approach:
- There is no assumption concerning the reader index or reader name; the desired card will be located in any reader
- The request will block or time-out if the desired card type is not inserted since we request the desired card type,
the script is not played on an unknown or incompatible card

Scripts written with the card-centric approach have however the following drawbacks:
- The script is limited to a specific card type;
we have to modify the script if we want to execute the script on another card type.

For example, we have to modify the ATR of the card if we are using the ATRCardType.
This can be partially solved by having a custom CardType that matches several ATRs, though.
"""

from smartcard.CardType import CardType
from smartcard.CardRequest import CardRequest
from smartcard.util import toHexString


class DCCardType(CardType):
    def matches(self, atr, reader=None):
        return atr[0] == 0x3B


card_type = DCCardType()
card_request = CardRequest(timeout=1, cardType=card_type)
card_service = card_request.waitforcard()

card_service.connection.connect()

print(toHexString(card_service.connection.getATR()))
