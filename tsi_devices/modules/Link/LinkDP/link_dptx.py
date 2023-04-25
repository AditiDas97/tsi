from .link_status_tx import *
from .link_configuration import *


class LinkSetupDpTx:

    def __init__(self):
        self.maxSupportedLinkRate = 0
        self.lanesCount = 0
        self.linkRate = 0
        self.enhancedFraming = 0
        self.supportedSSC = False
        self.enabledSSC = False
        self.downspreadAMP = 0
        self.downspreadFREQ = 0

    def __eq__(self, other):
        count = 0
        for key in self.__dict__.keys():
            if self.__dict__[key] != other.__dict__[key]:
                count += 1
                print(key + ": " + str(self.__dict__[key]) + " != " + str(other.__dict__[key]))
        if count > 0:
            return False
        else:
            return True


class LaneStatusDpTx:

    def __init__(self):
        self.clock_recovery = False
        self.channel_equalization = False
        self.symbol_link = False
        self.voltage_swing = str()
        self.pre_emphasis = str()

    def get_info_about_class(self):
        return self.__dict__

    def __eq__(self, other):
        count = 0
        for key in self.__dict__.keys():
            if self.__dict__[key] != other.__dict__[key]:
                count += 1
                print(key + ": " + str(self.__dict__[key]) + " != " + str(other.__dict__[key]))
        if count > 0:
            return False
        else:
            return True


class LinkStatusDptx:

    def __init__(self):
        self.assertedHPD = False
        self.sscEnabled = False
        self.sscSupported = False
        self.dscEnabled = False
        self.dscSupported = False
        self.lanesCount = 0
        self.linkRate = str()
        self.interlaneAlignStatus = False
        self.framing = str()
        self.scrambling = str()
        self.multiStream = False
        self.linkPattern = int()
        self.lanes = [LaneStatusDpTx() for i in range(4)]

    def get_info_about_class(self):
        return self.__dict__

    def __eq__(self, other):
        count = 0
        for key in self.__dict__.keys():
            if self.__dict__[key] != other.__dict__[key]:
                count += 1
                print(key + ": " + str(self.__dict__[key]) + " != " + str(other.__dict__[key]))
        if count > 0:
            return False
        else:
            return True


class LinkTx:

    def __init__(self, device):
        self.device = device
        self.link_configuration = LinkConfiguration(device)
        self.link_status = LinkStatusTx(device)

    def dptx_get_crc_values(self) -> dict:

        crc_red = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_DPTX_CRC_R, c_uint)
        assert crc_red[0] >= TSI_SUCCESS

        crc_green = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_DPTX_CRC_G, c_uint)
        assert crc_green[0] >= TSI_SUCCESS

        crc_blue = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_DPTX_CRC_B, c_uint)
        assert crc_blue[0] >= TSI_SUCCESS

        return dict({"r": hex(crc_red[1]), "g": hex(crc_green[1]), "b": hex(crc_blue[1])})

    def dptx_get_hpd_status(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_DPTX_HPD_STATUS, c_int)

        return result[1]

    def dptx_get_hw_caps(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_DPTX_HW_CAPS, c_int)

        return result[1]
