"""
Card-centric approach
Requesting any card

Smart card ATR parsing: https://smartcard-atr.apdu.fr/
"""

from smartcard.CardType import AnyCardType
from smartcard.CardRequest import CardRequest
from smartcard.util import toHexString

# The AnyCardType is useful for requesting any card in any reader
card_type = AnyCardType()
card_request = CardRequest(timeout=1, cardType=card_type)
card_service = card_request.waitforcard()

card_service.connection.connect()

print(toHexString(card_service.connection.getATR()))
