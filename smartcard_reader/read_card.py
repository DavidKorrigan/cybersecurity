import logging
import json
from smartcard.util import toHexString, toBytes
from smartcard.ATR import ATR

class ReadData:
    def __init__(self, connection, card_type):
        self.connection = connection
        self.card_type = card_type

    def atr_content(self):
        """
        The Answer To Reset (ATR) is described in the ISO7816-3 standard: https://cardwerk.com/iso-7816-part-3/
        The first bytes of the ATR describe the voltage convention (direct or inverse),
        followed by bytes describing the available communication interfaces and their respective parameters.
        These interface bytes are then followed by Historical Bytes which are not standardized,
        and are useful for transmitting proprietary information such as the card type,
        the version of the embedded software, or the card state.
        Finally these historical bytes are eventually followed by a checksum byte.
        """
        atr = ATR(self.connection.getATR())
        print("--------------------------------------------------------------------------")
        print("Answer To Reset: " + str(atr))
        print('Historical bytes: ', toHexString(atr.getHistoricalBytes()))
        if atr.hasChecksum:
            print('Checksum: ', "0x%x" % (atr.getChecksum()))
            print('Checksum OK: ', atr.checksumOK)
        else:
            print("No checksum set")
        print('T0  supported: ', atr.isT0Supported())
        print('T1  supported: ', atr.isT1Supported())
        print('T15 supported: ', atr.isT15Supported())
        print("--------------------------------------------------------------------------")

    def card_content(self):
        HEADER = [0x00, 0xA4, 0x04, 0x00]           # HEADER: CLASS - INSTRUCTION - PARAMETER 1 - PARAMETER 2
                                                    # INSTRUCTION 0xA4: Select Command
                                                    # INSTRUCTION 0xB2: Read Record Command
        TRAILER_LC = [0x07]                         # Number of data bytes send to the card.
        TRAILER_DATA = self.get_app_identifier()    # Data
        TRAILER_LE = [0x00]                         # Number of data bytes expected in the response.

        try:
            # Send APDU (Application Protocol Data Units) commands to the card
            data, sw1, sw2 = self.connection.transmit(HEADER + TRAILER_LC + TRAILER_DATA + TRAILER_LE)
            response_interpreted = self.get_adpu_response(sw1, sw2)
            print("%x %x: %s - %s" % (sw1, sw2, response_interpreted[0], response_interpreted[1]))

            print(data)
        except Exception as error:
            logging.critical("SW1: %x - SW2: %x" % (sw1, sw2))
            logging.critical(error)


    def get_app_identifier(self):
        AID = {
            "VISA": [0xA0, 0x00, 0x00, 0x00, 0x03, 0x10, 0x10],
            "MASTERCARD": [0xA0, 0x00, 0x00, 0x00, 0x04, 0x10, 0x10],
            "VPAY": [0xA0, 0x00, 0x00, 0x00, 0x03, 0x20, 0x20],
            "EDENRED": [0xA0, 0x00, 0x00, 0x04, 0x36, 0x01, 0x00],
            "CARTEVITALEx": [0xE8, 0x28, 0xBD, 0x08, 0x0F, 0xD2, 0x50, 0x00, 0x00, 0x04, 0x41, 0x64, 0xE8, 0x6C, 0x65],
            "CARTEVITALEy": [0xD2, 0x50, 0x00, 0x00, 0x02, 0x56, 0x49, 0x54, 0x41, 0x4C, 0x45],
            "CARTEVITALEz": [0xD2, 0x50, 0x00, 0x00, 0x04, 0x41, 0x64, 0xE8, 0x6C, 0x65, 0x01, 0x01]
        }

        return AID[self.card_type]

    def get_adpu_response(self, sw1, sw2):
        hex_sw1 = hex(sw1)[2:].upper()
        hex_sw2 = hex(sw2)[2:].upper()
        response = []

        f = open('apdu_responses.json')
        responses = json.load(f)

        response.append(responses[hex_sw1]["type"])
        if hex_sw1 == "61" or hex_sw1 == "6C":
            response.append(responses[hex_sw1]["XX"].replace('XX', hex_sw2))
        else:
            response.append(responses[hex_sw1][hex_sw2])

        return response

    def read_file_structure(self):
        # File structure
        # The files on a smart card are organized in a tree structure.
        # The topmost file is the Master File (MF). The MF has one or more Application Definition Files (ADF).
        # Inside of an ADF are Applicaton Elementary Files (AEF) that contain data.
        # You can quickly select an ADF with the Application Identifier (AID).
        # Within an ADF you can select AEFs with the Short File Identifier (SFIHEADER = [0x00, 0xB2, 0x50, 0x0C, 0x00]
        for sfi in range(1, 40):
            for rec in range(1, 17):
                p1 = rec
                p2 = sfi << 3 | 4
                HEADER = [0x00, 0xB2, p1, p2, 0x00]
                data, sw1, sw2 = self.connection.transmit(HEADER)

                if sw1 == 0x6a and sw2 == 0x83:
                    response_interpreted = self.get_adpu_response(sw1, sw2)
                    logging.error("%x %x: %s - %s" % (sw1, sw2, response_interpreted[0], response_interpreted[1]))
                elif sw1 == 0x6c:
                    response_interpreted = self.get_adpu_response(sw1, sw2)
                    logging.error("%x %x: %s - %s" % (sw1, sw2, response_interpreted[0], response_interpreted[1]))
                    p1_x = hex(p1)[2:].upper()
                    p2_x = hex(p2)[2:].upper()
                    le_x = (hex(sw2)[2:]).upper()
                    if len(p1_x) == 1: p1_x = "0" + p1_x
                    if len(p2_x) == 1: p2_x = "0" + p2_x
                    if len(le_x) == 1: le_x = "0" + le_x

                    command = "00 B2 %s %s %s" % (p1_x, p2_x, le_x)

                    data, sw1, sw2 = self.connection.transmit(toBytes(command))
                    # print("%x %x" % (sw1, sw2))
                    print(data)

                    # Convert each hex value to its corresponding ASCII character
                    hex_values = toHexString(data).split()
                    ascii_characters = ''.join([chr(int(hex_values, 16)) for hex_values in hex_values])
                    print(ascii_characters)
                else:
                    print("%x %x" % (sw1, sw2))
                    print(data)
