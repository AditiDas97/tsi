from tsi.tsi_devices.libs.lib_tsi.tsi import *
from tsi.tsi_devices.modules.device_constants import *


class SdpDpRx:

    def __init__(self, device):
        self.device = device

    def dprx_get_sdp_frames(self):

        TSI_R_DP_SDP_ACR = TSI_BASE_R_DP_SDP + 0x01
        TSI_R_DP_SDP_ASP = TSI_BASE_R_DP_SDP + 0x02
        TSI_R_DP_SDP_AIF = TSI_BASE_R_DP_SDP + 0x84
        list_r_dp_sdp = [TSI_R_DP_SDP_ACR, TSI_R_DP_SDP_ASP, TSI_R_DP_SDP_AIF]
        hdmi = False
        out = str()
        out += "HB" + "PB\n"
        out += info_header(32 if hdmi else 37, 3 if hdmi else 4) + "\n"

        for i in range(len(list_r_dp_sdp)):
            result = TSIX_TS_GetConfigItem(self.device.get_handle(), list_r_dp_sdp[i], c_char)
            if result[0] >= TSI_SUCCESS:
                out += info_hex(i, result[1], 31 if hdmi else 36, 2 if hdmi else 3)
        return out
