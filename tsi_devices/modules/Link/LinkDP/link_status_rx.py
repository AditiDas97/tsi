from tsi.tsi_devices.libs.lib_tsi.tsi import *


class LinkStatusRx:

    def __init__(self, device):
        self.device = device

    def dprx_set_msa_command(self, command: int):

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_W_DPRX_MSA_COMMAND, command)

    def dprx_get_lane_count(self) -> int:

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_DPRX_LINK_LANE_COUNT, c_int)

        return result[1]

    def dprx_get_link_rate(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_DPRX_LINK_RATE, c_int)

        return result[1]

    def dprx_get_link_status(self) -> int:

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_DPRX_LINK_STATUS_FLAGS, c_uint)

        return result[1]

    def dprx_get_lt_status(self) -> int:

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_DPRX_LT_STATUS_FLAGS, c_uint32)

        return result[1]

    def dprx_get_lt_info(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_DPRX_LT_INFO_R, c_uint32)

        return result[1]

    def dprx_get_lt_voltage_swing(self) -> list:

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_DPRX_LINK_VOLTAGE_SWING, c_int)
        result = result[1]

        return [result & 0xFF, (result >> 8) & 0xFF, (result >> 16) & 0xFF, (result >> 24) & 0xFF]

    def dprx_get_lt_pre_emphasis(self) -> list:

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_DPRX_LINK_PRE_EMPHASIS, c_int)
        result = result[1]

        return [result & 0xFF, (result >> 8) & 0xFF, (result >> 16) & 0xFF, (result >> 24) & 0xFF]

    def dprx_get_lt_bit_rate(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_DPRX_LT_BR_R, c_int)

        return result[1] & 0xFF

    def dprx_get_lt_lane_count(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_DPRX_LT_LC_R, c_int)

        return result[1]

    def dprx_get_edp_link(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_DPRX_EDP_LT_BR_R, c_int)

        return result[1]

    def dprx_get_swing(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_DPRX_LINK_VS_R, c_int)

        return result[1]

    def dprx_get_pre_emphasis(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_DPRX_LINK_PE_R, c_int)

        return result[1]

    def dprx_get_edp_bit_rate(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_DPRX_EDP_LINK_BR_R, c_int)

        return result[1]

    def dprx_get_error_counts(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_DPRX_ERROR_COUNTS, c_int, 4)

        return result[1]

    def dprx_get_ssc_status(self) -> (bool, bool):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_DPRX_SSC_STATUS_R, c_uint)

        return bool(result[1] & 0x1), bool((result[1] >> 1) & 0x1)

    def dprx_clear_errors(self):

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_DPRX_CLEAR_ERROR_COUNTS_W, 0)

    def dprx_get_max_stream_count(self):

        multi_stream = (((self.device.dprx_get_link_status() >> 19) & 1) != 0)
        return 4 if multi_stream else 1

    def dprx_get_iop_errors(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_DPRX_IOP_ERROR_COUNTERS_RW, c_uint32, 12)

        return result[1]

    def dprx_clear_iop_errors(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_DPRX_IOP_ERROR_COUNTERS_RW, c_uint32)

        return result[1]

    def dprx_get_iop(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_DPRX_ALPM_LT_INFO_R, c_uint32, 320)

        return result[1]
