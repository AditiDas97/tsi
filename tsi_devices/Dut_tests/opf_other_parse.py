from tsi.tsi_devices.tsi_device import *
from tsi.tsi_devices.modules.device_constants import *


class OpfOtherParse:

    def __init__(self):
        self.device = None

    def set_device(self, device):
        self.device = device

    @staticmethod
    def link_training(name: list, message: list):
        lanes = 1
        rate = 6
        if message[0].find('lanes') != -1:
            print(name[0])
            lanes = int(message[0][: message[0].find(' lanes')])
        elif message[1].find('Gbps link rate') != -1:
            print(name[1])
            rate = float(message[1][: message[1].find(' Gbps link rate')])

        return lanes, rate

    def lane_count(self, request: str):
        lanes = self.device.dptx_get_link_cfg_lanes()
        if request.find("reduce") != -1:
            if lanes == 1:
                pass
            else:
                lanes = 2 if lanes == 4 else 1
        elif request.find("increase") != -1:
            if lanes == 4:
                pass
            else:
                lanes = 2 if lanes == 1 else 4

        return lanes

    @staticmethod
    def parse_fec(request: str):
        if request.find("enable FEC") != -1:
            return True
        elif request.find("disable FEC") != -1:
            return False
