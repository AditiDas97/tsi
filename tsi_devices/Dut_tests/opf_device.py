from tsi.tsi_devices.Dut_tests.opf_dsc_parse import *


class OpfDevice:

    def __init__(self):
        pass

    def link_training(self, lanes, rate):
        pass

    def set_pg_settings(self, h_active: int, v_active: int, bpc: int, rate: int, pattern: str, _color_format: int,
                        video_mode: int):
        pass

    def edid_read(self):
        pass

    def set_fec(self, flag_fec):
        pass

    def set_lane_count(self, lane_count):
        pass

    def generate_audio(self, waveform, signal_frequency, sample_rate, bits, amplitude, channels):
        pass

    def load_dsc_image(self, h_active, v_active, bpc, _color_formate):
        pass

    @staticmethod
    def calculation_parameters(h_active: int, v_active: int, bpc: int, rate: int, pattern: str, _color_format: int,
                               video_mode: int):
        values = None
        if h_active == 640 and v_active == 480:
            values = case_values_pg[0]
        elif h_active == 800 and v_active == 600:
            values = case_values_pg[1]
        elif h_active == 848 and v_active == 480:
            values = case_values_pg[2]
        elif h_active == 1024 and v_active == 768:
            values = case_values_pg[3]
        elif h_active == 1280 and v_active == 768:
            values = case_values_pg[5]
        elif h_active == 1280 and v_active == 800:
            ind = 7 - video_mode
            values = case_values_pg[ind]
        elif h_active == 1280 and v_active == 960:
            values = case_values_pg[9]
        elif h_active == 1280 and v_active == 1024:
            values = case_values_pg[10]
        elif h_active == 1360 and v_active == 768:
            values = case_values_pg[11]
        elif h_active == 1400 and v_active == 1050:
            values = case_values_pg[12]
        if h_active == 1600 and v_active == 1200:
            ind = 14 - video_mode
            values = case_values_pg[ind]  # 14
        elif h_active == 1732 and v_active == 1344:
            values = case_values_pg[17]
        elif h_active == 1920 and v_active == 1080:
            ind = 20 - video_mode
            values = case_values_pg[ind]
        elif h_active == 1920 and v_active == 1440:
            values = case_values_pg[21]
        elif h_active == 2048 and v_active == 1536:
            values = case_values_pg[22]
        elif h_active == 2560 and v_active == 1080:
            ind = 25 - video_mode
            values = case_values_pg[ind]
        elif h_active == 2560 and v_active == 1600:
            ind = 27 - video_mode
            values = case_values_pg[ind]
        elif h_active == 3840 and v_active == 2160:
            ind = 32 - video_mode
            values = case_values_pg[ind]
        elif h_active == 5120 and v_active == 2160:
            ind = 45 - video_mode
            values = case_values_pg[ind]
        if h_active == 5120 and v_active == 2160:
            ind = 51 - video_mode
            values = case_values_pg[ind]

        if values is not None:
            values[8] = rate
            values[9] = _color_format
            values[10] = bpc
            values[14] = pattern
        return values

    @staticmethod
    def update_pg_settings(device, params: list):
        try:
            assert params[8] > 0
            device.pg_set_h_total(params[0])
            device.pg_set_v_total(params[1])
            device.pg_set_h_active(params[2])
            device.pg_set_v_active(params[3])
            device.pg_set_h_start(params[4])
            device.pg_set_v_start(params[5])
            device.pg_set_h_sync(params[6])
            device.pg_set_v_sync(params[7])
            device.pg_set_field_rate(params[8])
            device.pg_set_timing_flags(params[9], params[10], params[11], params[12], params[13])
            device.pg_set_link_pattern(params[14])
            device.apply_setting()
            time.sleep(1)
        except BaseException:
            pass