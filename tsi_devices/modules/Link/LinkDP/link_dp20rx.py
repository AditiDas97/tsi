from tsi.tsi_devices.libs.lib_tsi.tsi import *


class LinkDP20Rx:

    def __init__(self, device):
        self.device = device

    def dprx_set_dp20_link_rate(self, value):
        """"""
        dict_values = {10: 1, 20: 2, 13: 4}
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_DP2RX_LINK_RATE_CAPS, dict_values.get(value))

    def dprx_get_dp20_link_rate(self):
        """"""
        dict_values = {1: 10, 2: 20, 4: 13}
        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_DP2RX_LINK_RATE_CAPS, c_int)

        return dict_values.get(result[1])

    def dprx_get_dp20_ffe_preset(self):
        """"""
        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_DP2RX_LT_FFE_PRESET, c_int)

        return result[1]
