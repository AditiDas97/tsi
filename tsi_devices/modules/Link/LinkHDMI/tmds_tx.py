from tsi.tsi_devices.libs.lib_tsi.tsi import *


class TmdsTx:

    def __init__(self, device):
        self.device = device

    def hdtx_set_sink_feature(self, value: int):

        try:
            assert 1 <= value <= 5
            TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_HDTX_SINK_FEATURE_W, value)
        except AssertionError:
            print("Error. Invalid value")

    def hdtx_get_status_r(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_HDTX_STATUS_R, c_int)

        return result[1]

    def hdtx_get_sink_status(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_HDTX_SINK_STATUS_R, c_int)

        return result[1]

    def hdtx_get_scrambler(self) -> bool:

        return (self.hdtx_get_sink_status() & 1) != 0

    def hdtx_get_clock_rate(self):

        result = self.hdtx_get_sink_status() >> 1

        return result

    def hdtx_get_sink_caps(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_HDTX_SINK_CAPS_R, c_int)

        return result[1]

    def hdtx_get_supported_scrambler(self) -> bool:

        return (self.hdtx_get_sink_caps() & 2) != 0

    def hdtx_get_supported_scdc(self) -> bool:

        return (self.hdtx_get_sink_caps() & 1) != 0
