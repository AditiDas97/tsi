from tsi.tsi_devices.Dut_tests.opf_video_parse import *
from tsi.tsi_devices.Dut_tests.opf_other_parse import *


class OpfDscParse:

    def __init__(self):
        self.video_parse = OpfVideoParse()
        self.other_parse = OpfOtherParse()

    def parse_dsc(self, _id, pattern_message: str, name, message):
        if _id == 18:
            h_active, v_active, bpc, _color_formate = self.video_parse.parse_video(pattern_message, name, message, "DSC")
            return h_active, v_active, bpc, _color_formate,
        elif _id == 17:
            for i in message:
                print(i)
