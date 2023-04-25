from tsi.tsi_devices.libs.lib_tsi.tsi import *


class FrlStatusTx:

    def __init__(self, device):
        self.device = device

    def hdtx_get_frl_status(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_HDTX_FRL_STATUS_R, c_uint32)

        return result[1]

    def hdtx_get_link_mode_frl(self):

        return self.hdtx_get_frl_status() & 0xF

    def hdtx_get_link_status_frl(self, value: int):

        try:
            assert 4 <= value <= 8
            return (self.hdtx_get_frl_status() >> value) & 0x1
        except AssertionError:
            print("Error. Invalid value")

    def hdtx_get_channel_lock(self) -> tuple:

        return (((self.hdtx_get_frl_status() >> 25) & 0xF) >> 0) & 0x1, \
               (((self.hdtx_get_frl_status() >> 25) & 0xF) >> 1) & 0x1, \
               (((self.hdtx_get_frl_status() >> 25) & 0xF) >> 2) & 0x1, \
               (((self.hdtx_get_frl_status() >> 25) & 0xF) >> 3) & 0x1

    def hdtx_get_ffe_level(self) -> tuple:

        return (((self.hdtx_get_frl_status() >> 9) & 0xFFFF) >> (0 * 4)) & 0xF, \
               (((self.hdtx_get_frl_status() >> 9) & 0xFFFF) >> (1 * 4)) & 0xF, \
               (((self.hdtx_get_frl_status() >> 9) & 0xFFFF) >> (2 * 4)) & 0xF, \
               (((self.hdtx_get_frl_status() >> 9) & 0xFFFF) >> (3 * 4)) & 0xF

    def hdtx_get_frl_pattern(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_HDTX_FRL_PATTERN_R, c_uint32)

        return result[1]

    def hdtx_get_pattern(self) -> tuple:

        return ((self.hdtx_get_frl_pattern() & 0xFFFF) >> (0 * 4)) & 0xF, \
               ((self.hdtx_get_frl_pattern() & 0xFFFF) >> (1 * 4)) & 0xF, \
               ((self.hdtx_get_frl_pattern() & 0xFFFF) >> (2 * 4)) & 0xF, \
               ((self.hdtx_get_frl_pattern() & 0xFFFF) >> (3 * 4)) & 0xF

    def hdtx_get_last_pattern(self) -> tuple:

        return (((self.hdtx_get_frl_pattern() >> 16) & 0xFFFF) >> (0 * 4)) & 0xF, \
               (((self.hdtx_get_frl_pattern() >> 16) & 0xFFFF) >> (1 * 4)) & 0xF, \
               (((self.hdtx_get_frl_pattern() >> 16) & 0xFFFF) >> (2 * 4)) & 0xF, \
               (((self.hdtx_get_frl_pattern() >> 16) & 0xFFFF) >> (3 * 4)) & 0xF
