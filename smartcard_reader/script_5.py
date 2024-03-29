"""
Selecting the card communication protocol

Communication parameters are important for the protocol negotiation between the smart card reader and the card.
The main smartcard protocols are the T=0 protocol and the T=1 protocol, for byte or block transmission, respectively.
The required protocol can be specified at card connection or card transmission.
"""

from smartcard.CardType import AnyCardType
from smartcard.CardConnection import CardConnection
from smartcard.CardRequest import CardRequest
from smartcard.util import toHexString

card_type = AnyCardType()
card_request = CardRequest(timeout=1, cardType=card_type)
card_service = card_request.waitforcard()

# By defaults, connect() method of the CardConnection object will try to connect using either the T=0 or T=1 protocol.
# To force a connection protocol, you can pass the required protocol to the connect() method.
card_service.connection.connect(CardConnection.T0_protocol)

print(toHexString(card_service.connection.getATR()))
