from tsi.tsi_devices.tsi_device import *
from tsi.tsi_devices.modules.device_constants import *


dict_types = {
    0: int, 1: float, 2: str, 3: bool, 4: int, 5: list, 6: list, 7: list, 8: int, 9: bool, 10: list, 11: str, 12: int
}

dict_c_types = {int: c_uint32, float: c_double, bool: c_bool, str: c_char_p, list: c_uint32}

dict_video_mode = {"CTA": 0, "RB 1": 2, "RB 2": 1}


class OpfVideoParse:

    def __init__(self):
        pass

    @staticmethod
    def parse_video(pattern_message: str, name, message, pattern=""):
        h_active = 640
        v_active = 480
        rate = 60000
        bpc = 8
        if pattern == "":
            pattern = 'Color Bars'
        _color_format = 0  # RGB
        flag_by_video_mode = 0  # 0 = CTA, 1 = RB 1, 2 = RB 2
        if pattern_message.find('pattern #') != -1:
            pattern = pattern_message[pattern_message.find("(") + 1: pattern_message.find(')')]
        for i in range(len(name)):
            if name[i] == 'Video Mode' or name[i] == 'Timing':
                print(message[i])
                str_active = message[i][: message[i].find('x')]
                h_active = int(str_active[(0 if str_active.find(' ') == -1 else str_active.find(' ') + 1):])
                v_active = int(message[i][message[i].find('x') + 1: message[i].find('@')])
                rate = int(message[i][message[i].find('@') + 2: message[i].find('Hz')]) * 1000
                if message[i].find('BPC') != -1:
                    if message[i].rfind('Hz, ') != -1:
                        off = message[i].rfind('Hz, ') + 4
                    elif message[i].rfind(', ') != -1:
                        off = message[i].rfind(', ') + 2
                    else:
                        off = 0
                    bpc = int(message[i][off: message[i].find('BPC')])
                if message[i].find(", ") != -1:
                    flag_by_video_mode = dict_video_mode.get(message[i][message[i].find(", ") + 2:])
            elif name[i] == 'Color Format':
                print(message[i])
                _color_format = dict_color_formate.get(message[i][13: message[i].find(',')])
                bpc = int(message[i][message[i].find(', ') + 2: message[i].find(" bits per color")])

        return h_active, v_active, bpc, int(rate), pattern, _color_format, flag_by_video_mode
