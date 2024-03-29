"""
Card-centric approach

Requesting a card by ATR (Answer To Reset)
The first answer of a smart card inserted in a smart card reader is call the ATR.
The purpose of the ATR is to describe the supported communication parameters.

Smart card ATR parsing: https://smartcard-atr.apdu.fr/
"""

from smartcard.CardType import ATRCardType
from smartcard.CardRequest import CardRequest
from smartcard.util import toHexString, toBytes

# Create an ATRCardType object with the desired ATR
card_type = ATRCardType(toBytes("3B 6E 00 00 80 31 80 66 B0 84 0C 01 6E 01 83 00 90 00"))

# Create a CardRequest for this card type
card_request = CardRequest(timeout=1, cardType=card_type)
# waitforcard() will either return with a card service or a time-out.
card_service = card_request.waitforcard()

# The card service connection attribute can be used thereafter to transmit APDU commands to the card,
# as with the reader centric approach.
card_service.connection.connect()
print(toHexString(card_service.connection.getATR()))

SELECT = [0xA0, 0xA4, 0x00, 0x00, 0x02]
DF_TELECOM = [0x7F, 0x10]
data, sw1, sw2 = card_service.connection.transmit(SELECT + DF_TELECOM)

print("%x %x" % (sw1, sw2))

print(card_service.connection.getReader())
