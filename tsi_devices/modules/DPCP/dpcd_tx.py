from tsi.tsi_devices.libs.lib_tsi.tsi import *


class DpcdTx:

    def __init__(self, device):
        self.device = device

    def write_dpcd(self, base: int, count: int, data: bytearray) -> object:
        """

        Parameters
        ----------
        self.device : DPTX (TSIDevice)
            Indicates the device on which the operation is to be carried out
        base : int
            Start address of DPCD register
        count : int
            Number of registers to write
        data : bytearray
            data to be written into DPCD register

        """

        result = TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_W_DPTX_DPCD_BASE, base)
        if result < TSI_SUCCESS:
            return result
        TSIX_TS_SetConfigItem(self.device, TSI_DPTX_DPCD_DATA, data, c_byte, count)

    def read_dpcd(self, base: int, count: int) -> bytearray:
        """

        Parameters
        ----------
        self.device : DPTX (TSIDevice)
            Indicates the device on which the operation is to be carried out
        base : int
            Start address of DPCD register
        count : int
            Number of registers being read (Each DPCD register is one byte (8 bits))

        Returns
        -------
        list : bytearray
            list of DPCD data

        """
        result = TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_W_DPTX_DPCD_BASE, base)
        if result < TSI_SUCCESS:
            return bytearray()

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_DPTX_DPCD_DATA, c_byte, count)
        if result[0] < TSI_SUCCESS:
            return bytearray()
        else:
            return result[1]

    @staticmethod
    def load_dpcd(path: str):
        """"""
        file_dpd = open(path, 'rb')
        dpd_mark = file_dpd.read(4)
        list_dicts = []
        dict_for_first = {"base_address": int(), "size": int(), "data": None}
        dict_for_second = {"base_address": int(), "size": int(), "data": None}
        list_dicts.append(dict_for_first)
        list_dicts.append(dict_for_second)
        for i in range(2):
            list_dicts[i].update({"base_address": int.from_bytes(file_dpd.read(4)[::-1], 'little')})
            list_dicts[i].update({"size": int.from_bytes(file_dpd.read(4)[::-1], 'little')})
            list_dicts[i].update({"data": file_dpd.read(list_dicts[i].get('size'))})
        file_dpd.close()
        return list_dicts

    @staticmethod
    def save_dpcd(base_address_range_1: int, size_range_1: int, data_range_1: bytearray,
                       base_address_range_2: int, size_range_2: int, data_range_2: bytearray, path: str):
        """"""

        file_dpd = open(path + '.DPD', 'bw+')
        dpd_mark = 1
        file_dpd.write(dpd_mark.to_bytes(4, 'little'))
        if size_range_1 > 0 and len(data_range_1) > 0:
            file_dpd.write(base_address_range_1.to_bytes(4, 'little'))
            file_dpd.write(size_range_1.to_bytes(4, 'little'))
            file_dpd.write(data_range_1)
        if size_range_2 > 0 and len(data_range_2) > 0:
            file_dpd.write(base_address_range_2.to_bytes(4, 'little'))
            file_dpd.write(size_range_2.to_bytes(4, 'little'))
            file_dpd.write(data_range_2)
        file_dpd.close()

        file_hex = open(path + '.HEX', 'w')
        str_for_save = ""
        if size_range_1 > 0 and len(data_range_1) > 0:
            num = str(hex(base_address_range_1)).replace("0x", "")
            num2 = str(hex(size_range_1)).replace("0x", "")
            str_for_save += "\nRange 1. Start " + "0x" + num.rjust(8, '0') + ", Length 0x" + num2.rjust(8, '0')
            for i in range(len(data_range_1)):
                if i % 16 == 0:
                    str_for_save += "\n"
                tmp = str(hex(data_range_1[i])).replace("0x", "")
                str_for_save += ' ' + tmp.rjust(2, '0')
            str_for_save += '\n'
        if size_range_2 > 0 and len(data_range_2) > 0:
            num = str(hex(base_address_range_2)).replace("0x", "")
            num2 = str(hex(size_range_2)).replace("0x", "")
            str_for_save += "\nRange 2. Start " + "0x" + num.rjust(8, '0') + ", Length 0x" + num2.rjust(8, '0')
            for i in range(len(data_range_2)):
                if i % 16 == 0:
                    str_for_save += "\n"
                tmp = str(hex(data_range_2[i])).replace("0x", "")
                str_for_save += ' ' + tmp.rjust(2, '0')
            str_for_save += '\n'
        file_hex.write(str_for_save)
        file_hex.close()

        file_csv = open(path + '.CSV', 'w')
        str_for_save_csv = "Address (A), Data A+0, Data A+1, Data A+2, Data A+3, Data A+4, Data A+5, Data A+6, Data A+7"
        if size_range_1 > 0 and len(data_range_1) > 0:
            for i in range(size_range_1):
                if (i - base_address_range_1) % 8 == 0:
                    str_for_save_csv += "\n" + str(i)
                str_for_save_csv += "," + str(data_range_1[i])
            str_for_save_csv += '\n'
        if size_range_2 > 0 and len(data_range_2) > 0:
            for i in range(size_range_2):
                if (i - base_address_range_2) % 8 == 0:
                    str_for_save_csv += "\n" + str(i)
                str_for_save_csv += "," + str(data_range_2[i])
            str_for_save_csv += '\n'
        file_csv.write(str_for_save_csv)
        file_csv.close()
