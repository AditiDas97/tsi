from .tmds_rx import *
from .frl_status_rx import *
from .frl_control_rx import *


class LinkStatusHdrx:

    def __init__(self):
        self.tdms_clock_detected = False
        self.clockRate = 0
        self.inputStreamLockStatus = False
        self.linkMode = 0
        self.line0_locked = False
        self.line1_locked = False
        self.line2_locked = False
        self.hpd_status = False
        self.linkModeFRL = 0
        self.ltStatus = 0
        self.fltUpdate = False
        self.fltNoRetrain = False
        self.errorCounters = [0 for i in range(4)]
        self.channelLock = [bool() for i in range(4)]
        self.frlData = [bool() for i in range(4)]
        self.ffeLevel = [int() for i in range(4)]
        self.ltpReq = [int() for i in range(4)]

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


class LinkControlFRL:

    def __init__(self):
        self.linkModeFRLMax = 0
        self.frlStart = False
        self.fltReady = False
        self.fltNoTimeout = False
        self.frlMax = False
        self.checkPatterns = False
        self.ltpAdd = [None for i in range(4)]

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


class ARCStatusHdrx:

    def __init__(self):
        self.supported = bool()
        self.loopbackSupportedTPG = bool()
        self.loopbackSupportedHDMI = bool()
        self.loopbackSupportedDVI = bool()
        self.loopbackSupportedDP = bool()
        self.loopbackSupportedSPDIF = bool()
        self.enabled = False
        self.source = 1
        self.singleMode = True

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


class LinkRx:

    def __init__(self, device):
        self.device = device
        self.tmds = TmdsRx(self.device)
        self.frl_status = FrlStatusRx(self.device)
        self.frl_control = FrlControlRx(self.device)

    def hdrx_set_link_control(self, state: bool) -> TSI_RESULT:

        return TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_W_HDRX_LINK_CONTROL, state)

    def hdrx_get_hpd_status(self) -> bool:

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_HDRX_HPD_STATUS_R, c_int)

        return (result[1] & 1) != 0

    def hdrx_get_channel_lock(self) -> tuple:

        result = self.tmds.hdrx_get_link_status_r()

        return result & (1 << 13), result & (1 << 14), result & (1 << 15), result & (1 << 16)

    def hdrx_get_error_counters(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_HDRX_LANES_ERR_COUNTERS_R, c_uint64)

        return result[1]

    def hdrx_get_crc_values(self, number) -> list:

        crc = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_CRC_CAPTURE, c_uint8, 6 * number)[1]

        crc_list = []
        for i in range(0, len(crc), 6):
            crc_r = crc[i] + (crc[i + 1] << 8)
            crc_g = crc[i + 2] + (crc[i + 3] << 8)
            crc_b = crc[i + 4] + (crc[i + 5] << 8)
            crc_list.append(dict({"r": hex(crc_r), "g": hex(crc_g), "b": hex(crc_b)}))

        return crc_list

    def hdrx_get_link_status(self) -> int:

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_HDRX_LINK_STATUS, c_uint32)

        return result[1]
