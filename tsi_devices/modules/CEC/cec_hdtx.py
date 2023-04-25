from tsi.tsi_devices.libs.lib_tsi.tsi import *


class CecHdTx:

    def __init__(self, device):
        self.device = device

    def hdtx_get_capability(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_HDTX_CAPABILITY_R, c_int)

        return result[1]

    def hdtx_get_cec_status(self):

        result = self.hdtx_get_capability()

        return (result >> 4) & 1

    def hdtx_set_log_ctrl(self, value):

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_HDTX_LOG_CTRL_RW, value, c_int)

    def hdtx_get_log_ctrl(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_HDTX_LOG_CTRL_RW, c_int)

        return result[1]

    def hdtx_get_cec_log(self):

        result = self.hdtx_get_log_ctrl()

        return (result >> 2) & 1

    def hdtx_set_cec_state(self, value: bool):

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_HDTX_CEC_CTRL_RW, value, c_int)

    def hdtx_get_cec_version(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_HDTX_CEC_VERSION_R, c_int)

        return result[1]

    def hdtx_set_cec_logical_address(self, value):

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_HDTX_CEC_LOGICAL_ADDRESS_RW, value, c_int)

    def hdtx_get_cec_logical_address(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_HDTX_CEC_LOGICAL_ADDRESS_RW, c_int)

        return result[1]

    def hdtx_set_cec_phy_address(self, value):

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_HDTX_CEC_PHYSICAL_ADDRESS_RW, value, c_int)

    def hdtx_get_cec_phy_address(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_HDTX_CEC_PHYSICAL_ADDRESS_RW, c_int)

        return result[1]

    def hdtx_set_cec_op_code(self, value):

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_HDTX_CEC_OP_CODE_RW, value, c_int)

    def hdtx_get_cec_op_code(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_HDTX_CEC_OP_CODE_RW, c_int)

        return result[1]

    def hdtx_set_cec_op_code_param(self, value):

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_HDTX_CEC_OP_CODE_PARAM_RW, value, c_int)

    def hdtx_get_cec_op_code_param(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_HDTX_CEC_OP_CODE_PARAM_RW, c_int)

        return result[1]

    def hdtx_set_cec_device_type(self, value):

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_HDTX_CEC_DEVICE_TYPE_RW, value, c_int)

    def hdtx_get_cec_device_type(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_HDTX_CEC_DEVICE_TYPE_RW, c_int)

        return result[1]
