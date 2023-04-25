from tsi.tsi_devices.libs.lib_tsi.tsi import *


class TmdsRx:

    def __init__(self, device):
        self.device = device

    def hdrx_set_behavior(self, value: int):

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_HDRX_BEHAVIOR_RW, value)

    def hdrx_get_behavior(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_HDRX_BEHAVIOR_RW, c_int)

        return result[1]

    def hdrx_get_link_status_r(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_HDRX_LINK_STATUS_R, c_int)

        return result[1]

    def hdrx_get_input_stream_lock_status(self) -> bool:

        return (self.hdrx_get_link_status_r() & 4) != 0

    def hdrx_get_clock_rate(self):

        result = self.hdrx_get_link_status_r()

        return result & 2,  "1/10 3G mode" if (result & 2) == 0 else "1/40 6G mode"

    def hdrx_get_link_mode(self):

        result = self.hdrx_get_link_status_r()

        return result & 8, "DVI" if result & 8 == 1 else "HDMI"

    def hdrx_get_lines_locked(self) -> tuple:

        result = self.hdrx_get_link_status_r()

        return (result & 16) != 0, (result & 32) != 0, (result & 64) != 0

    def hdrx_get_arc_value_supported(self) -> bool:

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_HDRX_ARC_STATUS, c_int)

        return (result[1] >> 0) & 1

    def hdrx_get_arc_value_supported_tpg(self) -> bool:

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_HDRX_ARC_STATUS, c_int)

        return (result[1] >> 1) & 1

    def hdrx_get_arc_value_supported_hdmi(self) -> bool:

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_HDRX_ARC_STATUS, c_int)

        return (result[1] >> 2) & 1

    def hdrx_get_arc_value_supported_dvi(self) -> bool:

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_HDRX_ARC_STATUS, c_int)

        return (result[1] >> 8) & 1

    def hdrx_get_arc_value_supported_dp(self) -> bool:

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_HDRX_ARC_STATUS, c_int)

        return (result[1] >> 9) & 1

    def hdrx_get_arc_value_supported_sdpif(self) -> bool:

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_HDRX_ARC_STATUS, c_int)

        return (result[1] >> 10) & 1

    def hdrx_get_arc_value_supported_enabled(self) -> bool:

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_HDRX_ARC_STATUS, c_int)

        return (result[1] >> 31) & 1

    def hdrx_set_arc_control(self, single_mode: bool, arc_loopback_audio_source: int):

        int_value = 0

        if arc_loopback_audio_source == 1:
            int_value |= 2
            int_value |= (0 << 8)
        elif arc_loopback_audio_source == 0:
            int_value |= 1
        elif arc_loopback_audio_source == 2:
            int_value |= 2
            int_value |= (1 << 8)
        elif arc_loopback_audio_source == 3:
            int_value |= 2
            int_value |= (2 << 8)
        elif arc_loopback_audio_source == 4:
            int_value |= 2
            int_value |= (3 << 8)
        int_value |= (1 << 16) if single_mode else 0

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_W_ARC_CONTROL, int_value)
