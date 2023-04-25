from tsi.tsi_devices.tsi_device import *
from tsi.tsi_devices.modules.device_constants import *


class OpfAudioParse:

    def __init__(self):
        pass

    @staticmethod
    def parse_audio(message: list, type_parse=0):
        if type_parse == 0:
            for i in message:
                print(i)
            channels = int(message[0][message[0].find(', ') + 1: message[0].find(' Channels')])
            rate = float(message[0][message[0].find('@') + 1: message[0].find(' kHz')])
            bits = int(message[0][message[0].rfind(', ') + 1: message[0].find(' bits')])
            return 0, 1000, int(rate * 1000), bits, 60, channels
        elif type_parse == 1:
            channels = int(message[2][: message[2].find("channels")])
            rate = int(message[3][: message[3].find('Hz')])
            bits = int(message[4][: message[4].find('bits')])
            return 0, 1000, rate, bits, 60, channels
