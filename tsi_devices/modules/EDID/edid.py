from tsi.tsi_devices.libs.lib_tsi.tsi import *


class Edid:

    def __init__(self, device):
        self.device = device

    def read_edid(self) -> bytearray:

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_EDID_TE_OUTPUT, c_byte, 512)

        return result[1]

    def write_edid(self, data: bytearray) -> TSI_RESULT:

        return TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_EDID_TE_OUTPUT, data, c_byte, len(data))

    @staticmethod
    def save_edid(path: str, data: bytearray, save_bin: bool = True, save_hex: bool = False):

        if len(data) > 0:
            if save_bin:
                file_dpd = open(path + '.bin', 'bw+')
                file_dpd.write(data)
                file_dpd.close()
            if save_hex:
                file = open(path + '.hex', 'w')
                str_for_save = ''
                for i in data:
                    if i < 16:
                        str_for_save += str(hex(i)).replace("0x", "0")
                    else:
                        str_for_save += str(hex(i)).replace("0x", "")
                file.write(str_for_save)
                file.close()
                return str_for_save
    @staticmethod
    def load_edid(path: str) -> bytearray:

        if path.find('.hex') != -1:
            file = open(path, 'r')
            data = file.read()
            file.close()
            i = 0
            size = len(data)
            byte_array = bytearray()
            while i < size:
                byte_array.append(int('0x' + data[i] + data[i + 1], 16))
                i += 2
            return byte_array
        elif path.find('.bin') != -1:
            file = open(path, 'rb')
            data = file.read()
            file.close()
            return bytearray(data)
        else:
            print("Open file error.\nFile " + path + " not found.")
            return bytearray()
