from tsi.tsi_devices.libs.lib_tsi.tsi import *


class DscPropertiesStruct:

    def __init__(self):
        self.major_version = 0
        self.minor_version = 0
        self.rc_block_size = 0
        self.rc_buffer_size = 0
        self.support_1_slice = 0
        self.support_2_slice = 0
        self.support_4_slice = 0
        self.support_6_slice = 0
        self.support_8_slice = 0
        self.support_10_slice = 0
        self.support_12_slice = 0
        self.support_16_slice = 0
        self.support_20_slice = 0
        self.support_24_slice = 0
        self.line_buffer_depth = 0
        self.block_prediction = 0
        self.support_rgb = 0
        self.support_ycbcr_444 = 0
        self.support_simple_422 = 0
        self.support_native_422 = 0
        self.support_ycbcr_420 = 0
        self.support_8bpc = 0
        self.support_10bpc = 0
        self.support_12bpc = 0
        self.throughput_mode_0 = 0
        self.throughput_mode_1 = 0
        self.max_slice_width = 0
        self.bpp_inc = 0

    def update_value(self, value):
        self.major_version = value[0] & 0xF
        self.minor_version = (value[0] >> 4) & 0xF
        self.rc_block_size = value[1] & 0x3
        self.rc_buffer_size = value[2] & 0xFF + 1
        self.support_1_slice = value[3] & 0x1
        self.support_2_slice = (value[3] >> 1) & 0x1
        self.support_4_slice = (value[3] >> 3) & 0x1
        self.support_6_slice = (value[3] >> 4) & 0x1
        self.support_8_slice = (value[3] >> 5) & 0x1
        self.support_10_slice = (value[3] >> 6) & 0x1
        self.support_12_slice = (value[3] >> 7) & 0x1
        self.support_16_slice = (value[3] >> 8) & 0x1
        self.support_20_slice = (value[3] >> 9) & 0x1
        self.support_24_slice = (value[3] >> 10) & 0x1
        self.line_buffer_depth = value[4] & 0xF
        self.block_prediction = value[5] & 0x1
        self.support_rgb = value[6] & 0x1
        self.support_ycbcr_444 = (value[6] >> 1) & 0x1
        self.support_simple_422 = (value[6] >> 2) & 0x1
        self.support_native_422 = (value[6] >> 3) & 0x1
        self.support_ycbcr_420 = (value[6] > 4) & 0x1
        self.support_8bpc = (value[7] >> 1) & 0x1
        self.support_10bpc = (value[7] >> 2) & 0x1
        self.support_12bpc = (value[7] >> 3) & 0x1
        self.throughput_mode_0 = value[8] & 0xF
        self.throughput_mode_1 = (value[8] >> 4) & 0xF
        self.max_slice_width = value[9] & 0xFF
        self.bpp_inc = value[10] & 0x7

    def get_value(self):
        value = [(self.major_version & 0xF) | ((self.minor_version << 4) & 0xF0), self.rc_block_size & 0x3,
                 self.rc_buffer_size & 0xFF - 1,
                 (self.support_1_slice & 0x1) | ((self.support_2_slice & 0x1) << 1) |
                 ((self.support_4_slice & 0x1) << 3) | ((self.support_6_slice & 0x1) << 4) |
                 ((self.support_8_slice & 0x1) << 5) | ((self.support_10_slice & 0x1) << 6) |
                 ((self.support_12_slice & 0x1) << 7) | ((self.support_16_slice & 0x1) << 8) |
                 ((self.support_20_slice & 0x1) << 9) | ((self.support_24_slice & 0x1) << 10),
                 self.line_buffer_depth & 0xF, self.block_prediction & 0x1, (self.support_rgb & 0x1) |
                 ((self.support_ycbcr_444 & 0x1) << 1) | ((self.support_simple_422 & 0x1) << 2) |
                 ((self.support_native_422 & 0x1) << 3) | ((self.support_ycbcr_420 & 0x1) << 4),
                 ((self.support_8bpc & 0x1) << 1) | ((self.support_10bpc & 0x1) << 2) |
                 ((self.support_12bpc & 0x1) << 3), (self.throughput_mode_0 & 0xF) |
                 ((self.throughput_mode_1 & 0xF) << 4), self.max_slice_width & 0xFF, self.bpp_inc & 0x7]

        return value


class DscProperties:

    def __init__(self, device):
        self.device = device
        self.dsc_caps = DscPropertiesStruct()

    def update_dsc_properties(self, value: DscPropertiesStruct):
        self.dsc_caps = value
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_VR_DPRX_DSC_DPCD_PROPERTIES, self.dsc_caps.get_value(),
                              data_type=c_uint32, data_count=11)
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_VR_DPRX_DSC_DPCD_CONTROL, 2)

    def get_dsc_properties(self) -> DscPropertiesStruct:
        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_VR_DPRX_DSC_DPCD_PROPERTIES, c_uint32, 11)

        self.dsc_caps.update_value(result[1])

        return self.dsc_caps

    def reset_dsc_properties(self):
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_VR_DPRX_DSC_DPCD_CONTROL, 1)
