from tsi.tsi_devices.libs.lib_tsi.tsi import *
from ..device_constants import *


class PatternGeneratorDpRx:

    def __init__(self, device):
        self.device = device

    def dprx_set_msa_stream_select(self, value: int = 0):

        try:
            TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_W_DPRX_MSA_COMMAND, 1)
            assert 0 <= value < self.dprx_get_msa_stream_count()
            TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_DPRX_MSA_STREAM_SELECT, value)
        except AssertionError:
            print("Error. Invalid value")

    def dprx_get_msa_stream_count(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_DPRX_MSA_STREAM_COUNT, c_int)

        return result[1]

    def dprx_get_msa_data(self, count: int):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_DPRX_MSA_DATA, c_int, count)

        return result[1]

    def dprx_get_frame_rate(self, stream: int = 0) -> float:

        self.dprx_set_msa_stream_select(stream)
        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_DPRX_MSA_FRATE, c_uint32)

        return result[1] / 1000

    def dprx_get_v_active(self, stream: int = 0):

        self.dprx_set_msa_stream_select(stream)
        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_DPRX_MSA_VACTIVE, c_int)

        return result[1]

    def dprx_get_h_active(self, stream: int = 0):

        self.dprx_set_msa_stream_select(stream)
        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_DPRX_MSA_HACTIVE, c_int)

        return result[1]

    def dprx_get_resolution_active(self, stream: int = 0):

        return self.dprx_get_h_active(stream), self.dprx_get_v_active(stream)

    def dprx_get_v_start(self, stream: int = 0):

        self.dprx_set_msa_stream_select(stream)
        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_DPRX_MSA_VSTART, c_int)

        return result[1]

    def dprx_get_h_start(self, stream: int = 0):

        self.dprx_set_msa_stream_select(stream)
        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_DPRX_MSA_HSTART, c_int)

        return result[1]

    def dprx_get_resolution_start(self, stream: int = 0):

        return self.dprx_get_h_start(stream), self.dprx_get_v_start(stream)

    def dprx_get_v_sync(self, stream: int = 0):

        self.dprx_set_msa_stream_select(stream)
        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_DPRX_MSA_VSYNC_WIDTH, c_int)

        return c_int16(result[1]).value

    def dprx_get_h_sync(self, stream: int = 0):

        self.dprx_set_msa_stream_select(stream)
        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_DPRX_MSA_HSYNC_WIDTH, c_int)

        return c_int16(result[1]).value

    def dprx_get_resolution_sync(self, stream: int = 0):

        return self.dprx_get_h_sync(stream), self.dprx_get_v_sync(stream)

    def dprx_get_v_total(self, stream: int = 0):

        self.dprx_set_msa_stream_select(stream)
        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_DPRX_MSA_VTOTAL, c_int)

        return result[1]

    def dprx_get_h_total(self, stream: int = 0):

        self.dprx_set_msa_stream_select(stream)
        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_DPRX_MSA_HTOTAL, c_int)

        return result[1]

    def dprx_get_resolution_total(self, stream: int = 0):

        return self.dprx_get_h_total(stream), self.dprx_get_v_total(stream)

    def dprx_get_color_mode(self, stream: int = 0):

        self.dprx_set_msa_stream_select(stream)
        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_DPRX_MSA_COLOR_MODE, c_int)

        return result[1]

    def dprx_get_color_depth(self, stream: int = 0):

        self.dprx_set_msa_stream_select(stream)
        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_DPRX_MSA_COLOR_DEPTH_BPC, c_int)

        return result[1]

    def dprx_get_colorimetry(self, stream: int = 0):

        self.dprx_set_msa_stream_select(stream)
        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_DPRX_MSA_COLORIMETRY, c_int)

        return result[1]

    def dprx_get_msa_port_number(self, stream: int = 0):

        self.dprx_set_msa_stream_select(stream)
        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_DPRX_MSA_PORT_NUMBER, c_int)

        return result[1]

    def dprx_get_n_video(self, stream: int = 0):

        self.dprx_set_msa_stream_select(stream)
        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_DPRX_MSA_N_VIDEO, c_int)

        return result[1]

    def dprx_get_m_video(self, stream: int = 0):

        self.dprx_set_msa_stream_select(stream)
        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_DPRX_MSA_M_VIDEO, c_int)

        return result[1]

    def dprx_get_vbid(self, stream: int = 0):

        self.dprx_set_msa_stream_select(stream)
        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_DPRX_MSA_VBID, c_int)

        return result[1]

    def dprx_get_misc(self, stream: int = 0):
        self.dprx_set_msa_stream_select(stream)
        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_DPRX_MSA_MISC, c_int, 1)

        return result[1]

    def dprx_pg_get_all_info(self):

        return [self.dprx_get_h_total(), self.dprx_get_v_total(), self.dprx_get_h_active(), self.dprx_get_v_active(),
                self.dprx_get_h_start(), self.dprx_get_v_start(), self.dprx_get_h_sync(), self.dprx_get_v_sync(),
                self.dprx_get_frame_rate(), dict_color_mode_dp.get(self.dprx_get_color_mode()),
                self.dprx_get_color_depth(), dict_colorimetry_dp.get(self.dprx_get_colorimetry())]

    def dprx_set_stream(self, stream: int):

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_DPRX_STREAM_SELECT, stream, c_int)

    def dprx_get_stream(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_DPRX_STREAM_SELECT, c_int)

        return result[1]

    def dprx_get_dsc_status(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_DPRX_DSC_STATUS_R, c_uint32)

        return result[1]

    def dprx_set_dsc(self, value: bool):

        if self.dprx_get_dsc_status() & 1:
            TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_DPRX_DSC_CTRL, int(value))

    def dprx_get_dsc(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_DPRX_DSC_CTRL, c_uint32)

        return bool(result[1])
