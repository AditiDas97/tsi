from tsi.tsi_devices.libs.lib_tsi.tsi import *


class LinkStatusTx:

    def __init__(self, device):
        self.device = device

    def dptx_set_dp_link_pattern(self, value):

        try:
            assert 0 <= value <= 8
            TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_DPTX_DP_LINK_PATTERN, value, c_int)
        except AssertionError:
            print("Error. Invalid value")

    def dptx_get_dp_link_pattern(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_DPTX_DP_LINK_PATTERN, c_int)

        return result[1]

    def dptx_get_link_status_lane_count(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_DPTX_LINK_STATUS_LANE_COUNT, c_int)

        return result[1]

    def dptx_get_link_status_bit_rate(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_DPTX_LINK_STATUS_BIT_RATE, c_int)

        return result[1]

    def dptx_get_link_status_bits(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_DPTX_LINK_STATUS_BITS, c_int)

        return result[1]

    def dptx_get_link_status_volt_swing(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_DPTX_LINK_STATUS_VOLT_SWING, c_int, 4)

        return result[1]

    def dptx_get_link_status_pre_emp(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_DPTX_LINK_STATUS_PRE_EMP, c_int), 4

        return result[1]

    def dptx_get_dsc_status(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_DPTX_DSC_STATUS_R, c_int)

        return result[1]

    def dptx_set_pre_emphasis(self, pre_emp):

        intValue = (pre_emp << 24) | (pre_emp << 16) | (pre_emp << 8) | pre_emp
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_DPTX_OVERRIDE_PRE_EMPHASIS, intValue, c_uint32)

    def dptx_get_pre_emphasis(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_DPTX_OVERRIDE_PRE_EMPHASIS, c_uint32)

        return result[1]

    def dptx_set_voltage(self, voltage):

        intValue = (voltage << 24) | (voltage << 16) | (voltage << 8) | voltage
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_DPTX_OVERRIDE_VOLTAGE_SWING, intValue, c_uint32)
        self.device.apply_setting()

    def dptx_get_voltage(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_DPTX_OVERRIDE_VOLTAGE_SWING, c_uint32)

        return result[1]
