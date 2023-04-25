from tsi.tsi_devices.Dut_tests.opf_dsc_parse import *
from tsi.tsi_devices.Dut_tests.opf_audio_parse import *
from tsi.tsi_devices.Dut_tests.opf_tsi_device import *


class OPF:

    def __init__(self):
        self.opf_device = None
        self.functions = None
        self.dsc_parse = OpfDscParse()
        self.video_parse = OpfVideoParse()
        self.audio_parse = OpfAudioParse()
        self.other_parse = OpfOtherParse()
        self.answer = {0: TSI_OPF_RETURN_CODE_ABORT, 1: TSI_OPF_RETURN_CODE_PASS, 2: TSI_OPF_RETURN_CODE_PROCEED}

    def set_device(self, _device):
        self.other_parse.set_device(self.opf_device)

    def set_opf_dialog(self, dialog):
        self.opf_device = dialog

    def input_message(self, id_test: int, *args):
        self.set_device(self.opf_device.device)
        print(args[0])
        print(args[1])
        _type = None
        if id_test in [11, 12, 13, 101, 102, 104, 105, 121, 122]:
            print(args[2])
            return self.output_message(1)
        elif id_test in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 14, 15, 16, 17, 18, 103, 140, 141]:
            self.parse_message(id_test, args[1], args[3])
            print(args[2])
            return self.output_message(2)
        else:
            return self.output_message(0)

    def output_message(self, code: int):
        time.sleep(1)
        return self.answer.get(code)

    def parse_message(self, _id: int, request: str, args: list):
        name = []
        message = []
        if len(args) >= 2:
            for i in args:
                name.append(i.Name.decode('utf-8'))
                message.append(i.Description.decode('utf-8'))
        elif _id not in [3, 4, 5, 7, 8, 14, 15, 16, 17]:
            name.append(args[0].contents.Name.decode('utf-8'))
            message.append(args[0].contents.Description.decode('utf-8'))
        else:
            pass
        if _id == 1:  # link_training
            args = self.other_parse.link_training(name, message)
            self.opf_device.link_training(*args)
        elif _id in [2, 6, 9, 140]:  # Video
            args = self.video_parse.parse_video(request, name, message)
            self.opf_device.set_pg_settings(*args)
        elif _id == 3:
            self.opf_device.edid_read()
        elif _id in [4, 5]:  # Lane count
            args = self.other_parse.lane_count(request)
            self.opf_device.set_lane_count(args)
        elif _id in [7, 8]:  # Power save mode
            self.opf_device.set_pg_settings(h_active=640, v_active=480, bpc=8, rate=60000, pattern='Color Bars',
                                            _color_format=0, video_mode=0)
        elif _id == 10:
            args_audio = self.audio_parse.parse_audio(message, 1)
            self.opf_device.generate_audio(*args_audio)
            args_video = self.video_parse.parse_video("", name, message)
            self.opf_device.set_pg_settings(*args_video)
        elif _id in [14, 15, 16]:  # FEC
            args = self.other_parse.parse_fec(request)
            self.opf_device.set_fec(args)
        elif _id in [17, 18]:  # DSC
            args = self.dsc_parse.parse_dsc(_id, request, name, message)
            self.opf_device.load_dsc_image(*args)
        elif _id == 141:  # Audio
            args = self.audio_parse.parse_audio(message)
            self.opf_device.generate_audio(*args)
