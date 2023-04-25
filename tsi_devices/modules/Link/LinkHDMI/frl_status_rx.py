from tsi.tsi_devices.libs.lib_tsi.tsi import *


class FrlStatusRx:

    def __init__(self, device):
        self.device = device

    def hdrx_get_link_status_r(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_HDRX_LINK_STATUS_R, c_int)

        return result[1]

    def hdrx_get_link_mode_frl(self):

        return (self.hdrx_get_link_status_r() >> 9) & 0xF

    def hdrx_get_frl_data(self) -> tuple:

        result = self.hdrx_get_link_status_r()

        return result & (1 << 21), result & (1 << 22), result & (1 << 23), result & (1 << 24)

    def hdrx_get_frl_pattern(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_HDRX_FRL_PATTERN_RW, c_uint32)

        return result[1]

    def hdrx_set_frl_pattern(self, value: int):

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_HDRX_FRL_PATTERN_RW, value)

    def hdrx_get_ltp_req(self) -> tuple:

        result = self.hdrx_get_frl_ffe()

        return ((result & 0xFFFF) >> (0 * 4)) & 0xF, ((result & 0xFFFF) >> (1 * 4)) & 0xF, \
               ((result & 0xFFFF) >> (2 * 4)) & 0xF, ((result & 0xFFFF) >> (3 * 4)) & 0xF

    def hdrx_get_lt_status(self):

        return (self.hdrx_get_link_status_r() >> 18) & 0x7

    def hdrx_get_flt_update(self):

        return (self.hdrx_get_link_status_r() >> 17) & 0x7

    def hdrx_get_flt_no_retrain(self):

        return (self.hdrx_get_link_status_r() >> 27) & 0x7

    def hdrx_get_frl_ffe(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_HDRX_FRL_FFE_R, c_int)

        return result[1]

    def hdrx_get_ltp_add(self) -> tuple:

        result = self.hdrx_get_frl_ffe()
        LnxLtpAdd = (result >> 16) & 0xFFFF

        return (LnxLtpAdd >> (0 * 4)) & 0xF, (LnxLtpAdd >> (1 * 4)) & 0xF, (LnxLtpAdd >> (2 * 4)) & 0xF, \
               (LnxLtpAdd >> (3 * 4)) & 0xF
