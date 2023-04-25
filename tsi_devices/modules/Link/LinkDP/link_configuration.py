from tsi.tsi_devices.libs.lib_tsi.tsi import *
from tsi.tsi_devices.modules.device_constants import *


class LinkConfiguration:

    def __init__(self, device):
        self.device = device

    def dptx_set_link_cfg_lanes(self, value):

        try:
            assert value == 1 or value == 2 or value == 4
            TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_DPTX_LINK_CFG_LANES, value, c_int)
        except AssertionError:
            print("Error. Invalid value")

    def dptx_get_link_cfg_lanes(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_DPTX_LINK_CFG_LANES, c_int)

        return result[1]

    def dptx_set_link_cfg_bit_rate(self, value: float = 1.62):

        try:
            value = dict_rate.get(value)
            TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_DPTX_LINK_CFG_BIT_RATE, value, c_int)
        except AssertionError:
            print("Error. Invalid value")

    def dptx_get_link_cfg_bit_rate(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_DPTX_LINK_CFG_BIT_RATE, c_int)

        return result[1]

    def dptx_get_downspread_status(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_DPTX_DOWNSPREAD_STATUS_R, c_int)

        return result[1]

    def dptx_set_downspread_amp(self, value):

        try:
            assert 1 <= value <= 50
            TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_DPTX_DOWNSPREAD_AMP_RW, value, c_int)
        except AssertionError:
            print("Error. Invalid value")

    def dptx_get_downspread_amp(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_DPTX_DOWNSPREAD_AMP_RW, c_int)

        return result[1]

    def dptx_set_downspread_freq(self, value):

        try:
            assert 30000 <= value <= 63000
            TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_DPTX_DOWNSPREAD_FREQ_RW, value, c_int)
        except AssertionError:
            print("Error. Invalid value")

    def dptx_get_downspread_freq(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_DPTX_DOWNSPREAD_FREQ_RW, c_int)

        return result[1]

    def dptx_set_enhanced_framing(self, value: bool):

        value = 1 << 2 if value else 0
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_DPTX_CFG_FLAGS, value, c_uint32)

    def dptx_get_enhanced_framing(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_DPTX_CFG_FLAGS, c_int)

        return result[1] & (1 << 2)

    def dptx_set_command(self, value):

        try:
            assert 0 <= value <= 4
            TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_W_DPTX_COMMAND, value, c_uint32)
        except AssertionError:
            print("Error. Invalid value")

    def link_training(self):

        self.dptx_set_command(1)

    def dptx_set_enable_ssc(self, value):

        val = 0x1 if value else 0x0
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_DPTX_DOWNSPREAD_CTRL_RW, val, c_int)
