import time

from tsi.tsi_devices.Dut_tests.opf_device import *


class TsiOpfDevice(OpfDevice):

    def __init__(self, device):
        super().__init__()
        self.device = device

    def link_training(self, lanes, rate):
        self.device.dptx_set_link_cfg_lanes(lanes)
        self.device.dptx_set_link_cfg_bit_rate(dict_rate.get(rate))

    def set_pg_settings(self, h_active: int, v_active: int, bpc: int, rate: int, pattern: str, _color_format: int,
                        video_mode: int):
        bpc = dict_bpc.get(bpc)
        self.update_pg_settings(self.device, self.calculation_parameters(h_active, v_active, bpc, int(rate),
                                                                         pattern, _color_format, video_mode))

    def edid_read(self):
        time.sleep(1)
        self.device.read_edid()

    def set_fec(self, flag_fec):
        self.device.dptx_enable_fec(flag_fec)

    def set_lane_count(self, lane_count):
        self.device.dptx_set_link_cfg_lanes(lane_count)

    def generate_audio(self, waveform, signal_frequency, sample_rate, bits, amplitude, channels):
        self.device.start_generate_audio(waveform, signal_frequency, sample_rate, bits, amplitude, channels)

    def load_dsc_image(self, h_active, v_active, bpc, _color_formate):
        slicew = 2 if h_active != 7680 else 4
        sliceh = 4 if h_active == 1920 else 8
        lb = 13
        dict_color_format_dsc = {0: "RGB444", 1: "YUV444", 4: "YUV444", 2: "YUV422", 5: "YUV422", 3: "YUV420",
                                 6: "YUV420"}
        col_form = dict_color_format_dsc.get(_color_formate)

        path = "C:\\ProgramData\\Unigraf\\DSC_content_library\\" \
               "{}x{}_{}_BPY_bpc{}_bpp128_{}slicew_{}sliceh_{}lb.dsc"\
               .format(h_active, v_active, bpc, col_form, slicew, sliceh, lb)

        self.device.pg_load_dsc_image(path)
        time.sleep(1)
        self.set_fec(True)
