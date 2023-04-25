from .tmds_tx import *
from .frl_control_tx import *
from .frl_status_tx import *


class LinkStatusHdtx:

    def __init__(self):
        self.scrambler = bool()
        self.clockRate = int()
        self.linkMode = int()
        self.videoEnabled = bool()
        self.hpd_status = bool()
        self.supportedSCDC = bool()
        self.supportedScrambler = bool()
        self.linkModeFRL = int()

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


class LinkControlFRLHdtx:

    def __init__(self):
        self.linkModeFRLMax = 1
        self.ltTimeout = 2000
        self.ltPollTimeout = 2
        self.ffeMax = [int() for i in range(6)]


class LinkStatusFRLHdtx:

    def __init__(self):
        self.frlMode = 0
        self.channelLock = [bool() for i in range(4)]
        self.pattern = [int() for i in range(4)]
        self.lastPattern = [int() for i in range(4)]
        self.ffeLevel = [int() for i in range(4)]
        self.ltStatus = 0
        self.errorCounters = [0 for i in range(4)]
        self.fltUpdate = False
        self.fltReady = False
        self.frlStart = False
        self.fltNoTimeout = False
        self.frlMax = False

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
        self.tmds = TmdsTx(self.device)
        self.frl_status = FrlStatusTx(self.device)
        self.frl_control = FrlControlTx(self.device)

    def hdtx_get_hpd_status(self) -> bool:

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_HDTX_HPD_STATUS_R, c_int)

        return (result[1] & 1) != 0

    def hdtx_set_behavior(self, behavior: int):

        int_value = 0
        link_mode = self.hdtx_get_mode()
        if link_mode == 1:
            int_value = 1

        if behavior == 0:
            pass
        elif behavior == 1:
            int_value |= 1 << 2
        elif behavior == 2:
            int_value |= 2 << 2

        # TODO: change to TSI_HDTX_BEHAVIOUT when implemented
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_HDTX_CONTROL_W, int_value)

    def hdtx_set_mode(self, mode: int):

        int_value = 0
        int_value |= 1 if mode == 1 else 0

        behavior = self.hdtx_get_behavior()
        # print(behavior)

        if behavior == 1:
            int_value |= 0b0100
        elif behavior == 0:
            int_value |= 0b0000
        elif behavior == 2:
            int_value |= 0b1100

        print(int_value)
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_HDTX_CONTROL_W, int_value)

    def hdtx_get_behavior(self):

        return (self.tmds.hdtx_get_status_r() >> 2) & 0x3

    def hdtx_get_mode(self):

        return self.tmds.hdtx_get_status_r() & 0x1

    def hdtx_get_video_enable(self) -> bool:

        return ((self.device.hdtx_get_status_r() >> 1) & 0x1) != 0

    def hdtx_get_lanes_error_counters(self) -> tuple:

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_HDTX_LANES_ERR_COUNTERS_R, c_uint64)

        return result[1] & 0xFFFF, (result[1] >> 16) & 0xFFFF, (result[1] >> 32) & 0xFFFF, (result[1] >> 48) & 0xFFFF
