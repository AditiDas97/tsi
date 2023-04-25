from tsi.tsi_devices.libs.lib_tsi.tsi import *
from tsi.tsi_devices.modules.device_constants import *


class LinkCapabilities:

    def __init__(self, device):
        self.device = device

    def dprx_get_max_lanes(self) -> int:

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_DPRX_MAX_LANES, c_int)

        return result[1]

    def dprx_set_max_lanes(self, lanes: int):

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_DPRX_MAX_LANES, lanes, c_int)

    def dprx_get_max_link_rate(self) -> int:

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_DPRX_MAX_LINK_RATE, c_int)

        return result[1]

    def dprx_set_max_link_rate(self, rate):

        try:
            rate = dict_rate.get(rate)
            TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_DPRX_MAX_LINK_RATE, rate)
        except BaseException:
            print("Error. Invalid value")

    def dprx_get_dsc_status(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_DPRX_DSC_STATUS_R, c_uint32)

        return result[1]

    def dprx_set_dsc(self, value: bool):

        if self.dprx_get_dsc_status() & 1:
            TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_DPRX_DSC_CTRL, int(value))

    def dprx_get_dsc(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_DPRX_DSC_CTRL, c_uint32)

        return bool(result[1])

    def dprx_set_link_flags(self, supportMST: bool = True, supportTPS3: bool = True, supportTPS4: bool = True,
                            eDp14bSupport: bool = True,
                            enableDP2: bool = True, supportSsSBM: bool = True):
        value = 0
        # if self.device.type.find("400") != -1:
        #     value |= 1 if supportMST else 0
        value |= (1 << 1) if supportTPS3 else 0
        value |= (1 << 2) if supportTPS4 else 0
        value |= (1 << 3) if eDp14bSupport else 0
        value |= (1 << 4) if enableDP2 else 0
        value |= (1 << 5) if supportSsSBM else 0

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_DPRX_LINK_FLAGS, value, c_int)

    def dprx_get_link_flags(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_DPRX_LINK_FLAGS, c_int)

        return result[1]

    def dprx_capable_fec(self, capable: bool):
        """"""
        val = 0x1 if capable else 0x0
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_DPRX_FEC_CTRL, val)
        # if generate_hpd:
        #     self.dprx_set_hpd_pulse(1000)

    def dprx_get_edp_link_rates(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_DPRX_EDP_LINK_RATES, c_int)

        return result[1]

    def dprx_set_crd_features(self, value: int):

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_DPRX_CRD_FEATURES, value, c_int)

    def dprx_set_force_link_conf(self, value):

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_DPRX_FORCE_LINK_CONF_W, value)
