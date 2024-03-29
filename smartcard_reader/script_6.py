from smartcard.CardType import AnyCardType
from smartcard.CardConnection import CardConnection
from smartcard.CardRequest import CardRequest
from smartcard.util import toHexString, toBytes

card_type = AnyCardType()
card_request = CardRequest(timeout=1, cardType=card_type)
card_service = card_request.waitforcard()

card_service.connection.connect()

SELECT = [0xA0, 0xA4, 0x00, 0x00, 0x02]
DF_TELECOM = [0x7F, 0x23]
apdu = SELECT+DF_TELECOM

print('sending ' + toHexString(apdu))

response, sw1, sw2 = card_service.connection.transmit( apdu, CardConnection.T0_protocol)

print('response: ', response, ' status words: ', "%x %x" % (sw1, sw2))

if sw1 == 0x9F:
    GET_RESPONSE = [0XA0, 0XC0, 00, 00]
    apdu = GET_RESPONSE + [sw2]
    print('sending ' + toHexString(apdu))

    response, sw1, sw2 = card_service.connection.transmit(apdu)
    print('response: ', toHexString(response), ' status words: ', "%x %x" % (sw1, sw2))
