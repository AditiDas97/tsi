from .link_capabilities import *
from .link_status_rx import *


TrainPatternEnum = {0: "NoLtAfterHpd", 2: "TP2", 3: "TP3", 7: "TP4", 8: "Unknown"}
SleepALPMPatternEnum = {0: "NoLT", 1: "Sleep", 2: "Standby", 3: "Unknown"}
WakeupALPMPatternEnum = {0: "NoLT", 1: "AUX_PHY_WAKE", 2: "AUX_WAKE_F_CHANGE", 3: "WAKEUP", 4: "EIEOS", 5: "Unknown"}
ALPMSequenceLocation = {0: "NoALPM", 1: "VB", 2: "IFP"}
LinkTrainingEnum = {0: "NoLtAfterHpd", 1: "Full", 2: "Fast", 3: "Quick", 4: "Auxless", 5: "Unknown"}


class HWCapabilities:

    def __init__(self, value):
        self.mst = value & 1
        self.hdcp1 = (value >> 1) & 1
        self.hdcp2 = (value >> 2) & 1
        self.fec = (value >> 3) & 1
        self.dsc = (value >> 4) & 1
        self.alpm = (value >> 5) & 1
        self.lanecount3 = (value >> 6) & 1
        self.edp = (value >> 7) & 1
        self.mstStreamCount = (value >> 11) & 0xF
        self.maxLinkRate = (value >> 15) & 0xFF
        self.forceLinkCongiguration = (value >> 24) & 1
        self.dpPower = (value >> 26) & 1
        self.auxSwing = (value >> 27) & 1
        self.dp2CustomRates = (value >> 28) & 1
        self.customRateEx = (value >> 29) & 1
        self.dp2Fec = (value >> 30) & 1
        self.dp2Dsc = (value >> 31) & 1
        self.dp2SupportRates = (value >> 32) & 0xFF


class LinkCapabilitiesDprx:

    def __init__(self):
        self.hwSupportMST = False
        self.forceLinkCfgSupport = False
        self.eDp14bSupport = False
        self.sscSupported = False
        self.sscEnabled = False
        self.dscSupported = False
        self.dscEnabled = False
        self.dscLinkEstablished = False
        self.maxLanes = 0
        self.maxLinkRate = 0
        self.maxSupportedLinkRate = 0
        self.enableFastLT = True
        self.forceCableStatusToPlugged = False
        self.supportTPS3 = True
        self.supportMST = True
        self.supportTPS4 = True
        self.eDpRates = [0 for i in range(8)]

    def __eq__(self, other):
        count = 0
        for key in self.__dict__.keys():
            if self.__dict__[key] != other.__dict__[key]:
                count += 1
        if count > 0:
            return False
        else:
            return True


class LaneStatus:

    def __init__(self):
        self.clock_recovery = False
        self.channel_equalization = False
        self.symbol_link = False
        self.voltage_swing = 0
        self.pre_emphasis = 0
        self.errorCount = 0
        self.ffe_preset = 0

    def get_info_about_class(self):
        return self.__dict__

    def __eq__(self, other):
        count = 0
        for key in self.__dict__.keys():
            if self.__dict__[key] != other.__dict__[key]:
                count += 1
        if count > 0:
            return False
        else:
            return True


class ALPMLinkStatus:

    def __init__(self):
        self.trainPattern = 8
        self.sleepPattern = int()
        self.wakeupPattern = int()
        self.alpmSequenceLocation = int()
        self.crPatternDurationUs = 0
        self.eqPatternDurationUs = 0
        self.eieosPatternDurationUs = 0
        self.alpmSequenceCounter = 0
        self.alpmSequenceErrors = 0
        self.bitrateGbps = 0.0

    def get_info_about_class(self):
        return self.__dict__

    def __eq__(self, other):
        count = 0
        for key in self.__dict__.keys():
            if self.__dict__[key] != other.__dict__[key]:
                count += 1
        if count > 0:
            return False
        else:
            return True


class InitialLinkStatus:

    def __init__(self):
        self.linkTraining = 5
        self.lanesCount = 0
        self.lanes = [LaneStatus() for i in range(4)]
        self.interlaneAlignStatus = False
        self.crPatternDurationUs = 0
        self.eqPattern = 8
        self.eqPatternDurationUs = 0
        self.eDpBitRate = '{:.2f}'.format(0)
        self.BitRateGbps = str()

    def __eq__(self, other):
        count = 0
        for key in self.__dict__.keys():
            if self.__dict__[key] != other.__dict__[key]:
                count += 1
        if count > 0:
            return False
        else:
            return True

    def get_info_about_class(self):
        return self.__dict__


class LinkStatusDprx:

    def __init__(self):
        self.lanesCount = 0
        self.lanes = [LaneStatus() for i in range(4)]
        self.interlaneAlignStatus = False
        self.linkRate = str()
        self.framing = str()
        self.scrambling = str()
        self.asserted = False
        self.fail128_132_LT = False
        self.CDS_ILA = False
        self.EQ_ILA = False
        self.isDp2LinkMode = False
        self.multiStream = False
        self.cableStatus = False
        self.hpdRawStatus = False
        self.eDpBitRate = '{:.2f}'.format(0)
        self.enabledSSC = False
        self.supportedSSC = False
        self.initial = InitialLinkStatus()
        self.alpm = ALPMLinkStatus()

    def get_info_about_class(self):
        return self.__dict__

    def __eq__(self, other):
        count = 0
        for key in self.__dict__.keys():
            if self.__dict__[key] != other.__dict__[key]:
                count += 1
        if count > 0:
            return False
        else:
            return True


class LinkRx:

    def __init__(self, device):
        self.device = device
        self.link_status = LinkStatusRx(self.device)
        self.link_capabilities = LinkCapabilities(self.device)

    def dprx_get_crc_values(self) -> dict:

        crc_red = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_DPRX_CRC_R, c_uint)
        crc_green = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_DPRX_CRC_G, c_uint)
        crc_blue = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_DPRX_CRC_B, c_uint)

        return dict({"r": hex(crc_red[1]), "g": hex(crc_green[1]), "b": hex(crc_blue[1])})

    def dprx_get_list_crc_values(self, number: int) -> list:

        crc = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_VIDCAP_SIGNAL_CRC_R, c_uint16, 3 * number)[1]

        crc_list = []
        for i in range(0, len(crc), 3):
            crc_r = crc[i]
            crc_g = crc[i + 1]
            crc_b = crc[i + 2]
            crc_list.append(dict({"r": hex(crc_r), "g": hex(crc_g), "b": hex(crc_b)}))

        return crc_list

    # HPD Block
    def dprx_set_assert_status(self, value: bool):

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_W_FORCE_HOT_PLUG_STATE, int(value), c_int)

    def dprx_set_hpd_pulse(self, pulse: int):

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_DPRX_HPD_PULSE_W, pulse, c_int)

    def dprx_set_cable_force_state(self, state: bool):

        state = 0x3C if state else 0
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_DPRX_HPD_FORCE, state, c_int)

    def dprx_get_cable_force(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_DPRX_HPD_FORCE, c_int)

        return result[1]

    def dprx_get_cable_status(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_CABLE_STATUS, c_int)

        return result[1]

    def dprx_get_hpd_status(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_DPRX_HPD_STATUS, c_int)

        return result[1]

    def dprx_get_hw_caps(self) -> HWCapabilities:

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_DPRX_HW_CAPS, c_uint64)

        hw_caps = HWCapabilities(result[1])

        return hw_caps

