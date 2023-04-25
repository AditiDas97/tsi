from tsi.tsi_devices.libs.lib_tsi.tsi import *


class FrlControlRx:

    def __init__(self, device):
        self.device = device

    def hdrx_get_frl_capability(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_HDRX_FRL_CAPABILITY_RW, c_int)

        return result[1]

    def hdrx_get_link_mode_frl_max(self):

        return self.hdrx_get_frl_capability() & 0xF

    def hdrx_get_frl_start(self):

        return (self.hdrx_get_frl_capability() >> 4) & 0x1

    def hdrx_get_frl_ready(self):

        return (self.hdrx_get_frl_capability() >> 5) & 0x1

    def hdrx_get_frl_no_timeout(self):

        return (self.hdrx_get_frl_capability() >> 6) & 0x1

    def hdrx_get_frl_max(self):

        return (self.hdrx_get_frl_capability() >> 7) & 0x1

    def hdrx_get_frl_check_patterns(self):

        return (self.hdrx_get_frl_capability() >> 8) & 0x1

    def hdrx_set_frl_capability(self, link_mode_frl_max, value: list):

        frl_start = value[0]
        flt_ready = value[1]
        flt_no_timeout = value[2]
        frl_max = value[3]
        check_pattern = value[4]
        value = link_mode_frl_max | ((1 << 4) if frl_start else 0) | ((1 << 5) if flt_ready else 0) | \
                ((1 << 6) if flt_no_timeout else 0) | ((1 << 7) if frl_max else 0) | ((1 << 8) if check_pattern else 0)

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_HDRX_FRL_CAPABILITY_RW, value)
