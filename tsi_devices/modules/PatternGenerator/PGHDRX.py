from tsi.tsi_devices.libs.lib_tsi.tsi import *
from ..device_constants import *


class PatternGeneratorHdRx:

    def __init__(self, device):
        self.device = device

    def hdrx_get_h_total(self):

        self.hdrx_set_tim_command(1)
        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_HDRX_TIM_HTOTAL, c_int)

        return result[1]

    def hdrx_get_v_total(self):

        self.hdrx_set_tim_command(1)
        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_HDRX_TIM_VTOTAL, c_int)

        return result[1]

    def hdrx_get_resolution_total(self):

        return self.hdrx_get_v_total(), self.hdrx_get_h_total()

    def hdrx_get_h_active(self):

        self.hdrx_set_tim_command(1)
        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_HDRX_TIM_HACTIVE, c_int)

        return result[1]

    def hdrx_get_v_active(self):

        self.hdrx_set_tim_command(1)
        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_HDRX_TIM_VACTIVE, c_int)

        return result[1]

    def hdrx_get_resolution_active(self):

        return self.hdrx_get_v_active(), self.hdrx_get_h_active()

    def hdrx_get_h_sync(self):

        self.hdrx_set_tim_command(1)
        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_HDRX_TIM_HSYNC_WIDTH, c_int)

        return result[1]

    def hdrx_get_v_sync(self):

        self.hdrx_set_tim_command(1)
        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_HDRX_TIM_VSYNC_WIDTH, c_int)

        return result[1]

    def hdrx_get_resolution_sync(self):

        return self.hdrx_get_v_sync(), self.hdrx_get_h_sync()

    def hdrx_get_h_start(self):

        self.hdrx_set_tim_command(1)
        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_HDRX_TIM_HSTART, c_int)

        return result[1]

    def hdrx_get_v_start(self):

        self.hdrx_set_tim_command(1)
        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_HDRX_TIM_VSTART, c_int)

        return result[1]

    def hdrx_get_resolution_start(self):

        return self.hdrx_get_v_start(), self.hdrx_get_h_start()

    def hdrx_get_frame_rate(self) -> float:

        self.hdrx_set_tim_command(1)
        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_HDRX_TIM_FRATE, c_int)

        return result[1] / 1000

    def hdrx_get_color_depth(self) -> int:

        self.hdrx_set_tim_command(1)
        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_HDRX_TIM_COLOR_DEPTH, c_int)

        return result[1]

    def hdrx_get_bpc(self) -> int:

        self.hdrx_set_tim_command(1)
        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_INPUT_COLOR_DEPTH_R, c_int)

        return result[1]

    def hdrx_get_color_mode(self):

        self.hdrx_set_tim_command(1)
        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_HDRX_TIM_COLOR_MODE, c_int)

        return dict_color_mode_hdmi.get(result[1])

    def hdrx_get_colorimetry(self):

        self.hdrx_set_tim_command(1)
        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_HDRX_TIM_COLORIMETRY, c_int)

        return dict_colorimetry_hdmi.get(result[1])

    def hdrx_set_tim_command(self, value: int):

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_W_HDRX_TIM_COMMAND, value)

    def hdrx_calculate_pixel_clock(self):
        pclk_value = (self.hdrx_get_h_total() * self.hdrx_get_v_total() * self.hdrx_get_frame_rate()) / 1000000

        return pclk_value

    def hdrx_calculate_tmds_clock(self):
        pixel_rate = self.hdrx_calculate_pixel_clock()

        color_mode = self.hdrx_get_color_mode()
        bpc = self.hdrx_get_bpc()
        m = 1
        n = 1
        if color_mode != 'YCbCr4:2:2':
            if bpc == 8:
                m = 1
                n = 1
            elif bpc == 10:
                m = 5
                n = 4
            elif bpc == 12:
                m = 3
                n = 2
            elif bpc == 16:
                m = 2
                n = 1

        if color_mode == 'YCbCr4:2:0':
            pixel_rate /= 2

        return m * pixel_rate / n

    def hdrx_pg_get_all_info(self):
        return [self.hdrx_get_h_total(), self.hdrx_get_v_total(), self.hdrx_get_h_active(), self.hdrx_get_v_active(),
                self.hdrx_get_h_start(), self.hdrx_get_v_start(), self.hdrx_get_h_sync(), self.hdrx_get_v_sync(),
                self.hdrx_get_frame_rate(), dict_color_mode_dp.get(self.hdrx_get_color_mode()),
                self.hdrx_get_bpc(), dict_colorimetry_dp.get(self.hdrx_get_colorimetry())]
