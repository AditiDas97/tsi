from .controls import *
from .pdo import *


class PowerSource:

    def __init__(self, device, controls):
        self.device = device
        self.controls = controls

    def usbc_get_local_source_pdo(self) -> tuple:

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_USBC_PWR_LOCAL_SOURCE_PDO, c_uint32, 7)
        return result[1]

    def usbc_get_remote_source_pdo(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_USBC_PWR_REMOTE_SOURCE_PDO, c_uint32, 7)
        return result[1]

    def usbc_set_local_source_pdo(self, pdos: list):

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_USBC_PWR_LOCAL_SOURCE_PDO, pdos, c_uint32, 7)

    def usbc_get_local_source_pdo_all_info(self) -> PdoInfo:

        pwrSource = PdoInfo()
        pwrSource.szPDOsSupported = self.controls.usbc_get_pdo_count()
        pdos = self.usbc_get_local_source_pdo()
        for i in range(7):
            pwrSource.pdos.append(fill_pdo(pdos[i], True))

        return pwrSource

    def usbc_get_remote_source_pdo_all_info(self) -> PdoInfo:

        pwrSource = PdoInfo()
        pwrSource.szPDOsSupported = self.controls.usbc_get_pdo_count()
        pdos = self.usbc_get_remote_source_pdo()
        for i in range(7):
            pwrSource.pdos.append(fill_pdo(pdos[i], True))

        return pwrSource

    def usbc_set_source_pdos(self, pwr_source: PdoInfo, set_pdos: list):

        arr = []
        for i in range(len(set_pdos)):
            tmp_pdo = pwr_source.pdos[i].pdo
            if 0 <= i <= 3:
                if set_pdos[i].status == 0:
                    tmp_pdo = set_bits_by_index(tmp_pdo, 20, 2, set_pdos[i].peakCurrent)
                    tmp_pdo = set_bits_by_index(tmp_pdo, 10, 10, set_pdos[i].voltage // 50)
                    tmp_pdo = set_bits_by_index(tmp_pdo, 0, 10, set_pdos[i].maxCurrent // 10)
                if set_pdos[i].status == 1:
                    tmp_pdo = set_bits_by_index(tmp_pdo, 20, 10, set_pdos[i].maxVoltage // 50)
                    tmp_pdo = set_bits_by_index(tmp_pdo, 10, 10, set_pdos[i].minVoltage // 50)
                    tmp_pdo = set_bits_by_index(tmp_pdo, 0, 10, set_pdos[i].maxPower // 250)
                if set_pdos[i].status == 2:
                    tmp_pdo = set_bits_by_index(tmp_pdo, 20, 10, set_pdos[i].maxVoltage // 50)
                    tmp_pdo = set_bits_by_index(tmp_pdo, 10, 10, set_pdos[i].minVoltage // 50)
                    tmp_pdo = set_bits_by_index(tmp_pdo, 0, 10, set_pdos[i].maxCurrent // 10)
                tmp_pdo = set_bits_by_index(tmp_pdo, 30, 2, set_pdos[i].status)
            arr.append(tmp_pdo)

        self.usbc_set_local_source_pdo(arr[:4])

    def usbc_set_source_pdo(self, pdo: PDO):

        self.controls.usbc_set_local_source_pdo_select(pdo.pdo_selected)
        self.controls.usbc_set_local_source_pdo_type(pdo.pdo_type)
        if pdo.pdo_type == 1:
            self.controls.usbc_set_local_source_pdo_max_current(pdo.max_current)
            self.controls.usbc_set_local_source_pdo_voltage(pdo.voltage)
            self.controls.usbc_set_local_source_pdo_peak_current(pdo.peak_current)
            self.controls.usbc_set_local_source_pdo_fixed_bits(pdo.fixed_bits)
        elif pdo.pdo_type == 2:
            self.controls.usbc_set_local_source_pdo_max_current(pdo.max_current)
            self.controls.usbc_set_local_source_pdo_max_voltage(pdo.max_voltage)
            self.controls.usbc_set_local_source_pdo_min_voltage(pdo.min_voltage)
        elif pdo.pdo_type == 3:
            self.controls.usbc_set_local_source_pdo_max_power(pdo.max_power)
            self.controls.usbc_set_local_source_pdo_max_voltage(pdo.max_voltage)
            self.controls.usbc_set_local_source_pdo_min_voltage(pdo.min_voltage)
