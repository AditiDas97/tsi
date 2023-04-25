from tsi.tsi_devices.libs.lib_tsi.tsi import *


class CecHdRx:

    def __init__(self, device):
        self.device = device

    def hdrx_set_cec_ctrl(self, value):

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_HDRX_CEC_CTRL_RW, value, c_int)

    def hdrx_get_cec_ctrl(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_HDRX_CEC_CTRL_RW, c_int)

        return result[1]

    def hdrx_set_cec_cmd(self, value):

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_HDRX_CEC_CMD_RW, value, c_int)

    def hdrx_get_cec_cmd(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_HDRX_CEC_CMD_RW, c_int)

        return result[1]

    def hdrx_get_cec_version(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_HDRX_CEC_VERSION_R, c_int)

        return result[1]

    def hdrx_set_cec_logical_address(self, value):

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_HDRX_CEC_LOGICAL_ADDRESS_RW, value, c_int)

    def hdrx_get_cec_logical_address(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_HDRX_CEC_LOGICAL_ADDRESS_RW, c_int)

        return result[1]

    def hdrx_set_cec_phy_address(self, value):

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_HDRX_CEC_PHYSICAL_ADDRESS_RW, value, c_int)

    def hdrx_get_cec_phy_address(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_HDRX_CEC_PHYSICAL_ADDRESS_RW, c_int)

        return result[1]

    def hdrx_set_cec_op_code(self, value):

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_HDRX_CEC_OP_CODE_RW, value, c_int)

    def hdrx_get_cec_op_code(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_HDRX_CEC_OP_CODE_RW, c_int)

        return result[1]

    def hdrx_set_cec_op_code_param(self, value):

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_HDRX_CEC_OP_CODE_PARAM_RW, value, c_int)

    def hdrx_get_cec_op_code_param(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_HDRX_CEC_OP_CODE_PARAM_RW, c_int)

        return result[1]

    def hdrx_set_cec_device_type(self, value):

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_HDRX_CEC_DEVICE_TYPE_RW, value, c_int)

    def hdrx_get_cec_device_type(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_HDRX_CEC_DEVICE_TYPE_RW, c_int)

        return result[1]
