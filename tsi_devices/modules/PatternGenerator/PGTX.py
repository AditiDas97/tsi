from tsi.tsi_devices.libs.lib_tsi.tsi import *
from ..device_constants import *
from PIL import Image


class PatternGeneratorTx:

    def __init__(self, device):
        self.device = device

    @staticmethod
    def clamp(v: int, lo: int, hi: int):
        return lo if v < lo else (hi if hi < v else v)

    @staticmethod
    def add_bytes(value, lines):
        if lines >= 256:
            value += lines.to_bytes((lines.bit_length() + 7) // 8, byteorder='big')
        else:
            value += b'\x00' + lines.to_bytes((lines.bit_length() + 7) // 8, byteorder='big')
        return value

    @staticmethod
    def convert_to_bytes(value):
        if value > 0:
            result = value.to_bytes((value.bit_length() + 7) // 8, byteorder='big')
            return result
        else:
            return b'\x00'

    @staticmethod
    def build_color_format(image_format, bpc):
        if image_format == 'rgb':
            if bpc == 8:
                return dict_build_color_format.get("PGImageFormatRGB_080808")
            elif bpc in [10, 12]:
                return dict_build_color_format.get("PGImageFormatRGB_121212")
            elif bpc == 16:
                return dict_build_color_format.get("PGImageFormatRGB_161616")
        elif image_format == 'rgba':
            if bpc == 8:
                return dict_build_color_format.get("PGImageFormatRGBA_080808A")
            elif bpc in [10, 12, 16]:
                return dict_build_color_format.get("PGImageFormatRGBA_161616A")
        elif image_format == "yuv444":
            if bpc == 8:
                return dict_build_color_format.get("PGImageFormatYCbCr_080808")
            elif bpc in [10, 12, 16]:
                return dict_build_color_format.get("PGImageFormatYCbCr_161616")
        elif image_format == "yuv422":
            if bpc == 8:
                return dict_build_color_format.get("PGImageFormatYCbYCr_08")
            elif bpc in [10, 12, 16]:
                return dict_build_color_format.get("PGImageFormatYCbYCr_16")
        elif image_format == "yuv420":
            if bpc == 8:
                return dict_build_color_format.get("PGImageFormatI420_08")
            elif bpc == 10:
                return dict_build_color_format.get("PGImageFormatI420_10")
            elif bpc == 12:
                return dict_build_color_format.get("PGImageFormatI420_12")
            elif bpc == 16:
                return dict_build_color_format.get("PGImageFormatI420_16")
        else:
            return dict_build_color_format.get("PGImageFormatUnknown")

    @staticmethod
    def aligned(v, by):
        return (v + (by - 1)) / by * by

    def get_frame_size(self, width: int, height: int):

        line_stride_bytes = width * 4
        line_stride_aligned_bytes = self.aligned(line_stride_bytes, 1024)

        line_stride_bytes2 = width * 2
        line_stride_aligned_bytes2 = self.aligned(line_stride_bytes2, 1024)

        return (line_stride_aligned_bytes + line_stride_aligned_bytes2) * height

    def pg_apply_setting(self):

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_W_PG_COMMAND, 3)

    def pg_get_predef_pattern_count(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_PG_PREDEF_PATTERN_COUNT, c_int)

        return result[1]

    def pg_set_predef_pattern_params(self, params: list):

        pattern = self.pg_get_link_pattern()
        value = 0
        _type = c_int32

        if pattern in [3, 8, 9, 12]:
            if pattern == 3:
                red = params[0]
                green = params[1]
                blue = params[2]
                color_info = self.pg_get_timing_flags()[0]
                value = b'\x00'

                if color_info != 0:
                    y = self.clamp(int((0.257 * red) + (0.504 * green) + (0.098 * blue) + 16), 0, 255)
                    v = self.clamp(int((0.439 * red) - (0.368 * green) - (0.071 * blue) + 128), 0, 255)
                    u = self.clamp(int(-(0.148 * red) - (0.291 * green) + (0.439 * blue) + 128), 0, 255)
                    value += self.convert_to_bytes(y)
                    value += b'\x00'
                    value += self.convert_to_bytes(v)
                    value += b'\x00'
                    value += self.convert_to_bytes(u)
                else:
                    value += self.convert_to_bytes(green)
                    value += b'\x00'
                    value += self.convert_to_bytes(red)
                    value += b'\x00'
                    value += self.convert_to_bytes(blue)
                value += b'\x00\x00'
                value = int.from_bytes(value, byteorder='little', signed=True)
                _type = c_int64

            elif pattern == 8:
                white_lines = params[0]
                black_lines = params[1]
                value = b'\x00\x00'
                value = self.add_bytes(value, black_lines)
                value += b'\x00\x00'
                value = self.add_bytes(value, white_lines)
                value = int.from_bytes(value, byteorder='big', signed=True)
                _type = c_int64
            elif pattern in [9, 12]:
                step = params[0]
                value = b'\x00\x00'
                value += self.convert_to_bytes(step)
                value = int.from_bytes(value, byteorder='big', signed=True)
                _type = c_uint32

            TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_PG_PREDEF_PATTERN_PARAMS, value, _type)
        else:
            print("Invalid pattern. Please, choose the valid pattern.")

    def pg_get_predef_pattern_params(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_PG_PREDEF_PATTERN_PARAMS, c_uint)

        return result[1]

    def pg_get_predef_timing_count(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_PG_PREDEF_TIMING_COUNT, c_uint)

        return result[1]

    def pg_get_custom_timing_standart(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_PG_CUSTOM_TIMING_STANDARD, c_uint32)

        return result[1]

    def pg_get_custom_timing_id(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_PG_CUSTOM_TIMING_ID, c_int)

        return result[1]

    def pg_set_command(self, value: int):

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_W_PG_COMMAND, value, c_uint32)

    def pg_set_predef_timing_select(self, value: int):

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_W_PG_PREDEF_TIMING_SELECT, value, c_int)

    def pg_get_enable_stream_count(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_PG_ENABLED_STREAM_COUNT, c_uint)

        return result[1]

    def pg_set_enable_stream_count(self, value: int):

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_PG_ENABLED_STREAM_COUNT, value, c_int)

    def pg_set_link_pattern(self, value: str):

        try:
            TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_PG_PREDEF_PATTERN_SELECT, dict_pattern.get(value))
        except AssertionError:
            print("Error. Invalid value")

    def pg_get_link_pattern(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_PG_PREDEF_PATTERN_SELECT, c_int)

        return result[1]

    def pg_set_stream_select(self, value):

        try:
            assert 0 <= value <= TSI_R_PG_MAX_STREAM_COUNT
            TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_PG_STREAM_SELECT, value)
        except AssertionError:
            print("Error. Invalid value")

    def pg_set_h_active(self, value):

        try:
            assert value > 0
            TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_PG_CUSTOM_TIMING_HACTIVE, value)
        except AssertionError:
            print("Error. Invalid value")

    def pg_get_h_active(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_PG_CUSTOM_TIMING_HACTIVE, c_int)

        return result[1]

    def pg_set_v_active(self, value):

        try:
            assert value > 0
            TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_PG_CUSTOM_TIMING_VACTIVE, value)
        except AssertionError:
            print("Error. Invalid value")

    def pg_get_v_active(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_PG_CUSTOM_TIMING_VACTIVE, c_int)

        return result[1]

    def get_resolution_active(self):

        return self.pg_get_h_active(), self.pg_get_v_active()

    def pg_set_h_sync(self, value):

        try:
            assert value > 0
            TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_PG_CUSTOM_TIMING_HSYNCW, value)
        except AssertionError:
            print("Error. Invalid value")

    def pg_get_h_sync(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_PG_CUSTOM_TIMING_HSYNCW, c_int)

        return result[1]

    def pg_set_v_sync(self, value):

        try:
            assert value > 0
            TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_PG_CUSTOM_TIMING_VSYNCW, value)
        except AssertionError:
            print("Error. Invalid value")

    def pg_get_v_sync(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_PG_CUSTOM_TIMING_VSYNCW, c_int)

        return result[1]

    def get_resolution_sync(self):

        return self.pg_get_h_sync(), self.pg_get_v_sync()

    def pg_set_h_start(self, value):

        try:
            assert value > 0
            TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_PG_CUSTOM_TIMING_HSTART, value)
        except AssertionError:
            print("Error. Invalid value")

    def pg_get_h_start(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_PG_CUSTOM_TIMING_HSTART, c_int)

        return result[1]

    def pg_set_v_start(self, value):

        try:
            assert value > 0
            TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_PG_CUSTOM_TIMING_VSTART, value)
        except AssertionError:
            print("Error. Invalid value")

    def pg_get_v_start(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_PG_CUSTOM_TIMING_VSTART, c_int)

        return result[1]

    def get_resolution_start(self):

        return self.pg_get_h_start(), self.pg_get_v_start()

    def pg_set_h_total(self, value):

        try:
            assert value > 0
            TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_PG_CUSTOM_TIMING_HTOTAL, value)
        except AssertionError:
            print("Error. Invalid value")

    def pg_get_h_total(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_PG_CUSTOM_TIMING_HTOTAL, c_int)

        return result[1]

    def pg_set_v_total(self, value):

        try:
            assert value > 0
            TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_PG_CUSTOM_TIMING_VTOTAL, value)
        except AssertionError:
            print("Error. Invalid value")

    def pg_get_v_total(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_PG_CUSTOM_TIMING_VTOTAL, c_int)

        return result[1]

    def get_resolution_total(self):

        return self.pg_get_h_total(), self.pg_get_v_total()

    def pg_set_field_rate(self, field_rate):

        try:
            assert field_rate > 0
            TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_PG_CUSTOM_TIMING_FIELD_RATE, field_rate)
        except AssertionError:
            print("Error. Invalid value")

    def pg_get_field_rate(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_PG_CUSTOM_TIMING_FIELD_RATE, c_int)

        return result[1]

    def pg_set_timing_flags(self, color_info: str = 'RGB', color_depth: int = 8, h_sync_polarity: bool = True,
                            v_sync_polarity: bool = True, timf_meta_reduced_blank=0):

        PG_TIMF_COLOR_RGB = 0 << 11
        PG_TIMF_COLOR_YUV = 1 << 11
        PG_TIMF_COLOR_YUV422 = 2 << 11
        PG_TIMF_COLOR_YUV420 = 3 << 11

        dict_color = {0: PG_TIMF_COLOR_RGB, 1: PG_TIMF_COLOR_YUV | (0 << 16), 2: PG_TIMF_COLOR_YUV422 | (0 << 16),
                      3: PG_TIMF_COLOR_YUV420 | (0 << 16), 4: PG_TIMF_COLOR_YUV | (1 << 16),
                      5: PG_TIMF_COLOR_YUV422 | (1 << 16), 6: PG_TIMF_COLOR_YUV420 | (1 << 16)}

        dict_meta_reduced = {1: PG_TIMF_META_REDUCED_BLANK, 2: PG_TIMF_META_REDUCED_BLANK_2,
                             3: PG_TIMF_META_REDUCED_BLANK_3}

        if type(color_info) == str:
            color_info = dict_color_formate.get(color_info)
        assert -1 <= color_info <= 6
        _color_info = dict_color.get(color_info)

        pattern_index = self.pg_get_link_pattern()
        flag = int()
        # dsc_image = pattern_index == 0x10
        custom_image = pattern_index == 0xD
        if pattern_index == 11 or pattern_index == 3 or custom_image:
            flag |= _color_info

        if color_depth >= 6:
            color_depth = dict_bpc.get(color_depth)

        assert 0 <= color_depth <= 4

        flag |= color_depth

        if not h_sync_polarity:
            flag |= (1 << 9)
        if not v_sync_polarity:
            flag |= (1 << 10)

        if timf_meta_reduced_blank in [1, 2, 3]:
            flag |= dict_meta_reduced.get(timf_meta_reduced_blank)

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_PG_CUSTOM_TIMING_FLAGS, flag)

    def pg_get_timing_flags(self):

        PG_TIMF_COLOR_MASK = (0xF << 11)
        PG_TIMF_MASK = 0x07 << 0
        PG_TIMF_COLORIMETRY_MASK = 0x01 << 16

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_PG_CUSTOM_TIMING_FLAGS, c_int)

        flags = result[1]
        color_mode = flags & PG_TIMF_COLOR_MASK
        color_depth = flags & PG_TIMF_MASK
        colorimetry = flags & PG_TIMF_COLORIMETRY_MASK

        return color_mode, color_depth, colorimetry

    def pg_get_all_info(self):

        color_mode, color_depth, colorimetry = self.pg_get_timing_flags()
        full_color_mode = dict_color_formate_tx_rev.get(color_mode)

        return [self.pg_get_h_total(), self.pg_get_v_total(), self.pg_get_h_active(), self.pg_get_v_active(),
                self.pg_get_h_start(), self.pg_get_v_start(), self.pg_get_h_sync(), self.pg_get_v_sync(),
                self.pg_get_field_rate() / 1000, full_color_mode, dict_bpc_rev.get(color_depth)]

    def pg_set_pixel_format(self, value):

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_PG_CUSTOM_PATTERN_PIXEL_FORMAT, value)

    def pg_select_pattern_resolution(self, number=None, custom_params=None):

        if custom_params is not None and len(custom_params) == 15:
            params = custom_params
        elif number is not None and type(number) == int:
            params = case_values_pg[number]
        else:
            params = case_values_pg[0]

        self.pg_set_h_total(params[0])
        self.pg_set_v_total(params[1])
        self.pg_set_h_active(params[2])
        self.pg_set_v_active(params[3])
        self.pg_set_h_start(params[4])
        self.pg_set_v_start(params[5])
        self.pg_set_h_sync(params[6])
        self.pg_set_v_sync(params[7])
        self.pg_set_field_rate(params[8])
        self.pg_set_timing_flags(params[9], params[10], params[11], params[12], params[13])
        self.pg_set_link_pattern(params[14])

    def pg_load_image(self, path: str, width: int, height: int):

        self.pg_set_link_pattern("Custom image")

        if path.find(".bin") != -1:
            file = open(path, 'rb')
            path = path.replace(".bin", "")
            image_format = ""
            bits_per_component = 0
            width = 0
            height = 0
            color_info = ""
            string_parts = path.split("_")
            for part in string_parts:
                if part.find('x') != -1:
                    start = -1
                    if part.rfind("\\") != -1 or part.rfind('/') != -1:
                        start = part.rfind("\\") + 1 if part.rfind("\\") != -1 else part.rfind('/') + 1
                    width = int(part[start if start != -1 else 0: part.find('x')])
                    height = int(part[part.find('x') + 1:])
                elif part.find('bits') != -1:
                    bits_per_component = int(part.replace("bits", ""))
                elif part.lower() == "rgb" or part.lower() == "rgb444":
                    image_format = 'rgb'
                    color_info = "RGB"
                elif part.lower() == "rgba" or part.lower() == "rgba444":
                    image_format = 'rgba'
                    color_info = "RGB"
                elif part.lower() == "yuv444":
                    image_format = 'yuv444'
                    color_info = "YCbCr 4:4:4 ITU-601"
                elif part.lower() == "yuv422":
                    image_format = 'yuv422'
                    color_info = "YCbCr 4:2:2 ITU-601"
                elif part.lower() == "yuv420":
                    image_format = 'yuv420'
                    color_info = "YCbCr 4:2:0 ITU-601"

            image_format = self.build_color_format(image_format, bits_per_component)
            assert image_format != dict_build_color_format.get("PGImageFormatUnknown")

            data = bytearray(file.read())
            data_size = len(data)
            file.close()

        else:
            color_info = "RGB"
            im = Image.open(path)
            if self.get_resolution_active() != im.size:
                im = im.resize(self.get_resolution_active())
            im = im.convert('RGBA')
            _list = list(im.getdata())
            _array = [x for sets in _list for x in sets]
            data = bytearray(_array)
            image_format = dict_build_color_format.get("PGImageFormatRGBA_080808A")
            width, height = self.get_resolution_active()
            data_size = len(data)

        block_sizes = self.get_frame_size(width, height)

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_MEMORY_LAYOUT, int(block_sizes), c_uint64, data_size=1)
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_MEMORY_BLOCK_INDEX, 0)
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_PG_CUSTOM_PATTERN_INDEX, 0)
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_PG_CUSTOM_PATTERN_WIDTH, width)
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_PG_CUSTOM_PATTERN_HEIGHT, height)
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_PG_CUSTOM_PATTERN_PIXEL_FORMAT, image_format, c_uint)
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_PG_CUSTOM_PATTERN_DATA, data, c_uint8, data_count=data_size)
        self.pg_apply_setting()

    def pg_load_dsc_image(self, path: str):

        file = open(path, 'rb')
        data = list(file.read())
        file.close()

        assert data[0] != 'D' or data[1] != 'S' or data[2] != 'C' or data[3] != 'F', "Failed loading file {}". \
            format(path)

        dsc_version_minor = int(data[4]) & 0xF
        bits_per_component = (int(data[7]) >> 4) & 0xF

        if dsc_version_minor == 0x2 and bits_per_component == 0x0:
            bits_per_component = 16

        image_width = int(data[4 + 8]) << 8 | int(data[4 + 9])
        image_height = int(data[4 + 6]) << 8 | int(data[4 + 7])

        simple_422 = (int(data[4 + 4]) >> 3) & 0x1
        convert_rgb = (int(data[4 + 4]) >> 4) & 0x1
        native_422 = (int(data[4 + 88]) >> 0) & 0x1
        native_420 = (int(data[4 + 88]) >> 1) & 0x1
        color_info = ""
        image_format = ""

        if convert_rgb == 1 and simple_422 == 0 and native_422 == 0 and native_420 == 0:
            color_info = "RGB"
            image_format = "rgb"
        elif convert_rgb == 0 and simple_422 == 0 and native_422 == 0 and native_420 == 0:
            color_info = "YCbCr 4:4:4 ITU-601"
            image_format = "yuv444"
        elif convert_rgb == 0 and simple_422 == 1 and native_422 == 0 and native_420 == 0:
            color_info = "YCbCr 4:4:4 ITU-601"
            image_format = "yuv444"
        elif convert_rgb == 0 and simple_422 == 0 and native_422 == 1 and native_420 == 0:
            color_info = "YCbCr 4:2:2 ITU-601"
            image_format = "yuv422"
        elif convert_rgb == 0 and simple_422 == 0 and native_422 == 0 and native_420 == 1:
            color_info = "YCbCr 4:2:0 ITU-601"
            image_format = "yuv420"

        image_format = self.build_color_format(image_format, bits_per_component)
        assert image_format != dict_build_color_format.get("PGImageFormatUnknown")

        data_size = len(data)

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_MEMORY_LAYOUT, data_size, c_uint64, data_count=1,
                              data_size=1)
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_MEMORY_BLOCK_INDEX, 0, data_size=4)
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_PG_CUSTOM_PATTERN_INDEX, 0, data_size=4)
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_PG_CUSTOM_PATTERN_DATA, data, data_type=c_uint8,
                              data_count=data_size)

        self.pg_apply_setting()
        time.sleep(1)

    def pg_check_status(self):

        dict_status = {0: "OK", 1: "HW Fault", 2: "Bandwidth error", 3: "Memory error"}

        try:
            result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_PG_STS_EX, c_uint32)
        except AssertionError:
            result = (0, 0)

        if ((result[1] >> 30) & 1) == 0:
            return dict_status.get(result[1] & 0xFF)
        else:
            return "Not Ready"

    def dptx_set_mst(self, value: bool):

        input_value = 3 if value else 4
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_W_DPTX_COMMAND, input_value, c_int)
