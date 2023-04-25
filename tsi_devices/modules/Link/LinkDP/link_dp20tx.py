from tsi.tsi_devices.libs.lib_tsi.tsi import *


class LinkDP20Tx:

    def __init__(self, device):
        self.device = device

    # 10 = 1, 20 = 2, 13 = 4
    def dptx_set_dp20_link_rate(self, value):
        """"""
        dict_values = {10: 1, 20: 2, 13: 4}
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_DP2TX_LT_SBR, dict_values.get(value))

    def dptx_get_dp20_link_rate(self):
        """"""
        dict_values = {1: 10, 2: 20, 4: 13}
        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_DP2TX_LT_SBR, c_int)

        return dict_values.get(result[1])

    def dptx_set_dp20_lane_count(self, value):
        """"""
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_DP2TX_LT_SLC, value)

    def dptx_get_dp20_lane_count(self):
        """"""
        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_DP2TX_LT_SLC, c_int)

        return result[1]
