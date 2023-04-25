from tsi.tsi_devices.libs.lib_tsi.tsi import *


class HDCPStatusRX:

    def __init__(self):
        self.active = bool()
        self.keysLoaded = int()
        self.enabled = bool()
        self.authenticated = bool()
        self.hwsupported = bool()
        self.productionKeysAvailable = bool()
        self.testKeysAvailable = bool()

    def change_values(self, list_values: list):
        self.active = list_values[0]
        self.keysLoaded = list_values[1]
        self.enabled = list_values[2]
        self.authenticated = list_values[3]
        self.hwsupported = list_values[4]
        self.productionKeysAvailable = list_values[5]
        self.testKeysAvailable = list_values[6]

    def get_info_about_class(self):
        return self.__dict__

    def __eq__(self, other):
        count = 0
        for key in self.__dict__.keys():
            if self.__dict__[key] != other.__dict__[key]:
                count += 1
                print(key + ": " + str(self.__dict__[key]) + " != " + str(other.__dict__[key]))
        if count > 0:
            return False
        else:
            return True


class HdcpRx:

    def __init__(self, device):
        self.device = device

    def hdcprx_get_1x_status_all_info(self) -> HDCPStatusRX:

        status = HDCPStatusRX()
        intValue = self.hdcp_get_1x_status()

        status.active = bool(intValue & 1)
        status.keysLoaded = ((intValue >> 1) & 3)
        status.enabled = bool(((intValue >> 3) & 1) != 0)
        status.authenticated = bool((((intValue >> 4) & 1) != 0))
        status.hwsupported = bool(((intValue >> 16) & 1) != 0)
        status.productionKeysAvailable = bool(((intValue >> 17) & 1) != 0)
        status.testKeysAvailable = bool(((intValue >> 18) & 1) != 0)

        return status

    def hdcprx_get_2x_status_all_info(self) -> HDCPStatusRX:

        status = HDCPStatusRX()
        intValue = self.hdcp_get_2x_status()

        status.active = bool(intValue & 1)
        status.keysLoaded = ((intValue >> 1) & 3)
        status.enabled = bool(((intValue >> 3) & 1) != 0)
        status.authenticated = bool(((intValue >> 4) & 1) != 0)
        status.hwsupported = bool(((intValue >> 16) & 1) != 0)
        status.productionKeysAvailable = bool(((intValue >> 17) & 1) != 0)

        return status

    def hdcprx_1_set_capable(self, value: bool):

        res = H1_SINK_SET_CAPABLE if value else H1_SINK_CLEAR_CAPABLE

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_W_HDCP_1X_COMMAND, res)

    def hdcprx_1_load_keys(self, value: int):

        dict_value = {0: H1_SINK_UNLOAD_KEYS, 1: H1_SINK_LOAD_TEST_KEYS, 2: H1_SINK_LOAD_PROD_KEYS}

        assert value in [0, 1, 2]
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_W_HDCP_1X_COMMAND, dict_value.get(value))

    def hdcprx_2_set_capable(self, value: bool):

        res = H2_SINK_SET_CAPABLE if value else H2_SINK_CLEAR_CAPABLE

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_W_HDCP_2X_COMMAND, res)

    def hdcprx_2_load_keys(self, value: int):

        dict_value = {0: H2_SINK_UNLOAD_KEYS, 1: None, 2: H2_SINK_LOAD_PROD_KEYS}

        assert value in [0, 2]
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_W_HDCP_2X_COMMAND, dict_value.get(value))

    def hdcp_get_1x_status(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_HDCP_1X_STATUS, c_int)
        assert result[0] >= TSI_SUCCESS

        return result[1]

    def hdcp_get_2x_status(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_HDCP_2X_STATUS, c_int)
        assert result[0] >= TSI_SUCCESS

        return result[1]
