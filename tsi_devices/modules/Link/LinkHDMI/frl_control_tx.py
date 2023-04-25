from tsi.tsi_devices.libs.lib_tsi.tsi import *


class FrlControlTx:

    def __init__(self, device):
        self.device = device

    def hdtx_set_frl_capability(self, link_mode_frl_max: int, ffe_max: list):

        assert 0 <= link_mode_frl_max <= 6
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_HDTX_FRL_CAPABILITY_RW, (link_mode_frl_max & 0xF) |
                              ((ffe_max[0] & 0x3) << 5) | ((ffe_max[1] & 0x3) << 7) |
                              ((ffe_max[2] & 0x3) << 9) | ((ffe_max[3] & 0x3) << 11) |
                              ((ffe_max[4] & 0x3) << 13) | ((ffe_max[5] & 0x3) << 15))

    def hdtx_get_frl_capability(self) -> tuple:

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_HDTX_FRL_CAPABILITY_RW, c_uint32)

        return result[1] & 0xF, (result[1] >> 5) & 0x3, (result[1] >> 7) & 0x3, (result[1] >> 9) & 0x3, \
               (result[1] >> 11) & 0x3, (result[1] >> 13) & 0x3, (result[1] >> 15) & 0x3

    def hdtx_get_ffe_max(self) -> tuple:

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_HDTX_FRL_CAPABILITY_RW, c_uint32)[1]

        return (result >> 5) & 0x3, (result >> 7) & 0x3, (result >> 9) & 0x3, (result >> 11) & 0x3, \
               (result >> 13) & 0x3, (result >> 15) & 0x3

    def hdtx_set_frl_timers(self, lt_timeout: int, lt_poll_timeout: int):

        assert lt_timeout >= 0 and lt_poll_timeout >= 0
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_HDTX_FRL_TIMERS_RW,
                              ((lt_timeout & 0xFFFF) | ((lt_poll_timeout & 0xFFFF) << 16)))

    def hdtx_get_frl_timers(self) -> tuple:

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_HDTX_FRL_TIMERS_RW, c_uint32)

        return result[1] & 0xFFFF, (result[1] >> 16) & 0xFFFF

    def hdtx_set_sink_feature(self, value: int):

        try:
            assert 1 <= value <= 5
            TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_HDTX_SINK_FEATURE_W, value)
        except AssertionError:
            print("Error. Invalid value")

    def hdtx_get_lt_timeout(self):

        return self.hdtx_get_frl_timers()[0]

    def hdtx_get_lt_poll_timeout(self):

        return self.hdtx_get_frl_timers()[1]