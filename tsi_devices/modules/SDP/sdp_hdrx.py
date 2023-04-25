from tsi.tsi_devices.libs.lib_tsi.tsi import *
from tsi.tsi_devices.modules.device_constants import *


class SdpHdRx:

    def __init__(self, device):
        self.device = device

    def hdrx_get_info_frame(self):

        info_frames = [TSI_R_HDMI_INFOFRAME_ACR, TSI_R_HDMI_INFOFRAME_ASP, TSI_R_HDMI_INFOFRAME_GCP,
                       TSI_R_HDMI_INFOFRAME_ACP, TSI_R_HDMI_INFOFRAME_ISRC1, TSI_R_HDMI_INFOFRAME_ISRC2,
                       TSI_R_HDMI_INFOFRAME_OBA, TSI_R_HDMI_INFOFRAME_DTS, TSI_R_HDMI_INFOFRAME_HBR,
                       TSI_R_HDMI_INFOFRAME_GMP, TSI_R_HDMI_INFOFRAME_3D_ASP, TSI_R_HDMI_INFOFRAME_3D_OBA,
                       TSI_R_HDMI_INFOFRAME_AMP, TSI_R_HDMI_INFOFRAME_MST_ASP, TSI_R_HDMI_INFOFRAME_MST_OBA,
                       TSI_R_HDMI_INFOFRAME_VSI, TSI_R_HDMI_INFOFRAME_AVI, TSI_R_HDMI_INFOFRAME_SPD,
                       TSI_R_HDMI_INFOFRAME_AIF, TSI_R_HDMI_INFOFRAME_MPEG, TSI_R_HDMI_INFOFRAME_DRM]

        hdmi = True
        out = str()
        out += "HB" + "PB\n"
        out += info_header(32 if hdmi else 37, 3 if hdmi else 4) + "\n"

        for i in range(len(info_frames)):
            result = TSIX_TS_GetConfigItem(self.device.get_handle(), info_frames[i], c_char)
            if result[0] >= TSI_SUCCESS:
                out += info_hex(i, result[1], 31 if hdmi else 36, 2 if hdmi else 3)
        return out
