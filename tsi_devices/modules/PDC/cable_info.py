from tsi.tsi_devices.libs.lib_tsi.tsi import *


class CableInfoStruct:

    def __init__(self):
        self.vdo = str()
        self.vendorID = None
        self.modalOpSupported = None
        self.prodType = None
        self.asDevice = None
        self.asHost = None
        self.xID = None
        self.bcdDevice = None
        self.prodID = None
        self.superSpeed = None
        self.vbusThrough = None
        self.vbusCurrentCable = None
        self.ssrx2 = None
        self.ssrx1 = None
        self.sstx2 = None
        self.sstx1 = None
        self.terminationType = None
        self.latency = None
        self.captive = None
        self.fwVersion = None
        self.hwVersion = None

    def get_info_about_class(self):
        return self.__dict__


class CableInfo:

    def __init__(self, device):
        self.device = device

    def usbc_get_ido_table(self) -> list:

        try:
            result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_USBC_IDO_TABLE, c_uint32, 6)
            assert result[0] >= TSI_SUCCESS
            data = []
            for i in range(6):
                data.append(result[1][i])
            return data
        except AssertionError:
            return [-1, -1]

    def usbc_get_cable_info_all_info(self) -> CableInfoStruct:

        cable_info = CableInfoStruct()
        ido_table = self.usbc_get_ido_table()
        if ido_table[0] != -1:
            for i in range(len(ido_table)):
                cable_info.vdo += hex(ido_table[i] & 0xFF)[2:] + ' ' + hex((ido_table[i] >> 8) & 0xFF)[2:] + ' ' + \
                                  hex((ido_table[i] >> 16) & 0xFF)[2:] + ' ' + hex((ido_table[i] >> 24) & 0xFF)[
                                                                               2:] + ' '
            cable_info.vdo = cable_info.vdo[:-2]
            cable_info.prodType = (ido_table[0] >> 27) & 7
            cable_info.vendorID = ido_table[0] & 0xFFFF
            cable_info.modalOpSupported = (ido_table[0] >> 26) & 1
            cable_info.asDevice = (ido_table[0] >> 30) & 1
            cable_info.asHost = (ido_table[0] >> 31) & 1
            cable_info.xID = ido_table[1]
            cable_info.bcdDevice = ido_table[2] & 0xFFFF
            cable_info.prodID = (ido_table[2] >> 16) & 0xFFFF
            if cable_info.prodType == 3 or cable_info.prodType == 4:
                cable_info.superSpeed = ido_table[3] & 7
                if cable_info.prodType == 3:
                    cable_info.vbusThrough = (ido_table[3] >> 4) & 1
                else:
                    cable_info.vbusThrough = (ido_table[3] >> 4) & 1
                cable_info.vbusCurrentCable = (ido_table[3] >> 5) & 3
                cable_info.ssrx2 = (ido_table[3] >> 7) & 1
                cable_info.ssrx1 = (ido_table[3] >> 8) & 1
                cable_info.sstx2 = (ido_table[3] >> 9) & 1
                cable_info.sstx1 = (ido_table[3] >> 10) & 1
                cable_info.terminationType = (ido_table[3] >> 11) & 3
                cable_info.latency = (ido_table[3] >> 13) & 0xF
                cable_info.captive = (ido_table[3] >> 18) & 3
                cable_info.fwVersion = (ido_table[3] >> 24) & 0xF
                cable_info.hwVersion = (ido_table[3] >> 28) & 0xF
        return cable_info
