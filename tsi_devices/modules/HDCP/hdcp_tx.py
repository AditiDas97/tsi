from tsi.tsi_devices.libs.lib_tsi.tsi import *


class HDCPStatusTx:

    def __init__(self):
        self.active = bool()
        self.keysLoaded = int()
        self.enabled = bool()
        self.authenticated = bool()
        self.hwsupported = bool()
        self.productionKeysAvailable = bool()
        self.testKeysAvailable = bool()

    def get_info_about_class(self):
        return self.__dict__

    def __eq__(self, other):
        count = 0
        for key in self.__dict__.keys():
            if self.__dict__[key] != other.__dict__[key]:
                count += 1
                print(self.__dict__[key] + "!=" + other.__dict__[key])
        if count > 0:
            return False
        else:
            return True


class HdcpTx:

    def __init__(self, device):
        self.device = device

    def hdcptx_get_1x_status_all_info(self) -> HDCPStatusTx:

        status = HDCPStatusTx()
        intValue = self.hdcp_get_1x_status()

        status.active = bool((intValue >> 8) & 1)
        status.keysLoaded = ((intValue >> 9) & 3)
        status.enabled = (((intValue >> 11) & 1) != 0)
        status.authenticated = (((intValue >> 12) & 1) != 0)
        status.hwsupported = (((intValue >> 24) & 1) != 0)
        status.productionKeysAvailable = (((intValue >> 25) & 1) != 0)
        status.testKeysAvailable = (((intValue >> 26) & 1) != 0)

        return status

    def hdcptx_get_2x_status_all_info(self) -> HDCPStatusTx:

        status = HDCPStatusTx()
        intValue = self.hdcp_get_2x_status()

        status.active = (intValue >> 8) & 1
        status.keysLoaded = ((intValue >> 9) & 3)
        status.enabled = (((intValue >> 11) & 1) != 0)
        status.authenticated = (((intValue >> 12) & 1) != 0)
        status.hwsupported = (((intValue >> 24) & 1) != 0)
        status.productionKeysAvailable = (((intValue >> 25) & 1) != 0)

        return status

    def hdcptx_1_encrypt(self, value: bool):

        res = H1_SOURCE_ENABLE_ENCRYPT if value else H1_SOURCE_DISABLE_ENCRYPT

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_W_HDCP_1X_COMMAND, res)

    def hdcptx_1_authenticate(self, value: bool):

        res = H1_SOURCE_AUTHENTICATE if value else H1_SOURCE_DE_AUTHENTICATE

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_W_HDCP_1X_COMMAND, res)

    def hdcptx_1_load_keys(self, value: int):

        dict_value = {0: H1_SOURCE_UNLOAD_KEYS, 1: H1_SOURCE_LOAD_TEST_KEYS, 2: H1_SOURCE_LOAD_PROD_KEYS}

        assert value in [0, 1, 2]
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_W_HDCP_1X_COMMAND, dict_value.get(value))

    def hdcptx_2_encrypt(self, value: bool):

        res = H2_SOURCE_ENABLE_ENCRYPT if value else H2_SOURCE_DISABLE_ENCRYPT

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_W_HDCP_2X_COMMAND, res)

    def hdcptx_2_authenticate(self, value: bool):

        res = H2_SOURCE_AUTHENTICATE if value else H2_SOURCE_DE_AUTHENTICATE

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_W_HDCP_2X_COMMAND, res)

    def hdcptx_2_load_keys(self, value: int):

        dict_value = {0: H1_SOURCE_UNLOAD_KEYS, 1: None, 2: H2_SOURCE_LOAD_PROD_KEYS}

        assert value in [0, 2]
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_W_HDCP_2X_COMMAND, dict_value.get(value))

    def hdcp_get_1x_status(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_HDCP_1X_STATUS, c_int)

        return result[1]

    def hdcp_get_2x_status(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_HDCP_2X_STATUS, c_int)

        return result[1]
