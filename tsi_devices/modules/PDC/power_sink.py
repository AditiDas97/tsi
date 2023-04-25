from .controls import *
from .pdo import *


class PowerSinkInfo:

    def __init__(self):
        self.unigrafExternalPowerSupply = None
        self.powerContractSelectedByIndex = None
        self.powerContractSelect = None
        self.priority = None
        self.szPDOsSupported = None
        self.external = None
        self.internal = None
        self.pdos = []

    def get_info_about_class(self):
        return self.__dict__

    def print_info(self):
        print('unigrafExternalPowerSupply = ', self.unigrafExternalPowerSupply)
        print('powerContractSelectedByIndex = ', self.powerContractSelectedByIndex)
        print('powerContractSelect = ', self.powerContractSelect)
        print('priority = ', self.priority)
        print('szPDOsSupported = ', self.szPDOsSupported)
        print('external = ', self.external)
        print('internal = ', self.internal)
        for i in range(7):
            print('sink PDO {0} = {1}'.format(i + 1, self.pdos[i].get_info_about_class()))


class PowerSink:

    def __init__(self, device, controls):
        self.device = device
        self.controls = controls

    def usbc_get_local_sink_pdo(self) -> tuple:

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_USBC_PWR_LOCAL_SINK_PDO, c_int32, 7)
        return result[1]

    def usbc_set_local_sink_pdo(self, pdos: list):

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_USBC_PWR_LOCAL_SINK_PDO, pdos, c_uint32, 7)

    def usbc_get_remote_sink_pdo(self):
        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_USBC_PWR_REMOTE_SINK_PDO, c_uint32, 7)
        return result[1]

    def usbc_get_ext_resistance_status(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_USBC_EXT_RESISTANCE_STATUS, c_int32)
        return result[1]

    def usbc_get_int_resistance_status(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_USBC_INT_RESISTANCE_STATUS, c_int32)
        return result[1]

    def usbc_get_power_status(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_USBC_POWER_STATUS, c_uint32)
        assert result[0] >= TSI_SUCCESS
        return result[1]

    def usbc_set_load_resistor(self, resistor_type: int, value: int, type_of_call=1):
        """
        resistor_type: int
            0 - internal resistor
            1 - external resistor
        value: int
            Resistance value in milliohms
            external resistor values = [0, 13900, 10600, 9100, 7600, 6600, 5600, 4600, 3600, 1800]
            internal resistor values = [0, 10000, 5500, 3550, 3500, 2600, 2140, 1760]
        type_of_call: int
            value equals 1 (default setting)
        """
        external_power = self.controls.usbc_get_hardware_options() & 1
        _types = ["internal", "external"]
        external_resistor_values = [0, 13900, 10600, 9100, 7600, 6600, 5600, 4600, 3600, 1800]
        internal_resistor_values = [0, 10000, 5500, 3550, 3500, 2600, 2140, 1760]

        if ((resistor_type == 1 and external_power) or resistor_type == 0) and self.device.get_type().find("340") != -1:
            if (resistor_type == 0 and value in internal_resistor_values) \
                    or (resistor_type == 1 and value in external_resistor_values):
                value <<= 2
                value |= type_of_call
                value |= (resistor_type << 1)
                TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_USBC_RESISTANCE_CTRL, value, c_uint32)
            else:
                print("Invalid value for {} resistor: {}".format(_types[resistor_type], value))
        elif resistor_type not in [0, 1]:
            print("Invalid resistor type. Need to select: 0 - internal resistor, 1 - external resistor.")
        else:
            print("Unigraf External Power Unit is not connected")

    def usbc_disable_load_resistor(self):

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_USBC_RESISTANCE_CTRL, 0, c_uint32)

    def usbc_get_current_index_and_resistance(self, epsu: bool) -> tuple:

        s_resExt = [0, 13900, 10600, 9100, 7600, 6600, 5600, 4600, 3600, 1800]
        s_resInt = [0, 10000, 5500, 3550, 3500, 2600, 2140, 1760]
        Res = s_resExt if epsu else s_resInt
        ResNow = self.usbc_get_ext_resistance_status() if epsu else self.usbc_get_int_resistance_status()
        if ResNow == 0:
            return 0, ResNow

        try:
            f = next(idx for idx, res in enumerate(Res) if res == ResNow)
        except StopIteration:
            f = None

        if f is not None:
            return f, ResNow
        id = -1
        resClosest = sys.maxsize
        for i in range(len(Res)):
            res = Res[i]
            if abs(res - ResNow) < resClosest:
                resClosest = abs(res - ResNow)
                id = i
        return id, ResNow

    def usbc_get_local_sink_pdo_all_info(self) -> PdoInfo:

        pwrSource = PdoInfo()
        pdos = self.usbc_get_local_sink_pdo()
        for i in range(7):
            pwrSource.pdos.append(fill_pdo(pdos[i], False))

        return pwrSource

    def usbc_get_remote_sink_pdo_all_info(self) -> PdoInfo:

        pwrSource = PdoInfo()
        pdos = self.usbc_get_remote_sink_pdo()
        for i in range(7):
            pwrSource.pdos.append(fill_pdo(pdos[i], False))

        return pwrSource

    def usbc_get_power_sink_all_info(self) -> PowerSinkInfo:

        pwrSink = PowerSinkInfo()
        pwrSink.unigrafExternalPowerSupply = (self.controls.usbc_get_hardware_options() & 1) != 0
        pdos = self.usbc_get_local_sink_pdo()
        for i in range(7):
            pdo = PDO()
            pdo_data = pdos[i]
            pdo_type = (pdo_data >> 30) & 3
            if pdo_type == 0:
                operCurrent = (pdos[i] & 0x03ff) * 10
                voltage = ((pdos[i] >> 10) & 0x03ff) * 50
                pdo.assign_settings(max_current=operCurrent, voltage=voltage)
            elif pdo_type == 1:
                maxPower = (pdos[i] & 0x03ff) * 250
                maxVoltage = ((pdos[i] >> 20) & 0x03ff) * 50
                minVoltage = ((pdos[i] >> 10) & 0x03ff) * 50
                pdo.assign_settings(max_power=maxPower, min_voltage=minVoltage, max_voltage=maxVoltage)
            elif pdo_type == 2:
                operCurrent = (pdos[i] & 0x03ff) * 10
                maxVoltage = ((pdos[i] >> 20) & 0x03ff) * 50
                minVoltage = ((pdos[i] >> 10) & 0x03ff) * 50
                pdo.assign_settings(max_current=operCurrent, max_voltage=maxVoltage, min_voltage=minVoltage)
            pwrSink.pdos.append(pdo)

        pwrSink.priority = (self.controls.usbc_get_pwr_contract_control() >> 4) & 3
        pwrSink.powerContractSelectedByIndex = (self.controls.usbc_get_pwr_contract_control() >> 31) & 1
        if pwrSink.powerContractSelectedByIndex:
            pwrSink.powerContractSelect = self.controls.usbc_get_pwr_contract_select()
        pwrSink.szPDOsSupported = self.controls.usbc_get_pdo_count()

        epsu = (self.controls.usbc_get_hardware_options() & 1) != 0
        idRes = self.usbc_get_current_index_and_resistance(epsu)
        pwrContractEstablished = (self.usbc_get_power_status() & 4) != 0
        if not epsu:
            Load = idRes[0]
            if pwrContractEstablished and Load:
                pwrSink.external = 0
                pwrSink.internal = Load
        else:
            Load = idRes[0]
            if pwrContractEstablished and Load:
                pwrSink.internal = 0
                pwrSink.external = Load

        return pwrSink

    def usbc_set_sink_pdos(self, pwr_sink: PowerSinkInfo, set_pdos: list):

        arr = []
        for i in range(len(set_pdos)):
            tmp_pdo = pwr_sink.pdos[i].pdo
            if 0 <= i <= 3:
                if set_pdos[i].status == 0:
                    tmp_pdo = set_bits_by_index(tmp_pdo, 0, 10, set_pdos[i].operCurrent // 10)
                    tmp_pdo = set_bits_by_index(tmp_pdo, 10, 10, set_pdos[i].voltage // 50)
                if set_pdos[i].status == 1:
                    tmp_pdo = set_bits_by_index(tmp_pdo, 20, 10, set_pdos[i].maxVoltage // 50)
                    tmp_pdo = set_bits_by_index(tmp_pdo, 10, 10, set_pdos[i].minVoltage // 50)
                    tmp_pdo = set_bits_by_index(tmp_pdo, 0, 10, set_pdos[i].maxPower // 250)
                if set_pdos[i].status == 2:
                    tmp_pdo = set_bits_by_index(tmp_pdo, 20, 10, set_pdos[i].maxVoltage // 50)
                    tmp_pdo = set_bits_by_index(tmp_pdo, 10, 10, set_pdos[i].minVoltage // 50)
                    tmp_pdo = set_bits_by_index(tmp_pdo, 0, 10, set_pdos[i].operCurrent // 10)
                tmp_pdo = set_bits_by_index(tmp_pdo, 30, 2, set_pdos[i].status)
            arr.append(tmp_pdo)
        self.usbc_set_local_sink_pdo(arr[:4])

    def usbc_set_sink_pdo(self, pdo: PDO):
        self.controls.usbc_set_local_sink_pdo_select(pdo.pdo_selected)
        self.controls.usbc_set_local_sink_pdo_type(pdo.pdo_type)
        if pdo.pdo_type == 1:
            self.controls.usbc_set_local_sink_pdo_max_current(pdo.max_current)
            self.controls.usbc_set_local_sink_pdo_voltage(pdo.voltage)
            self.controls.usbc_set_local_sink_pdo_fixed_bits(pdo.fixed_bits)
        elif pdo.pdo_type == 2:
            self.controls.usbc_set_local_sink_pdo_max_current(pdo.max_current)
            self.controls.usbc_set_local_sink_pdo_max_voltage(pdo.max_voltage)
            self.controls.usbc_set_local_sink_pdo_min_voltage(pdo.min_voltage)
        elif pdo.pdo_type == 3:
            self.controls.usbc_set_local_sink_pdo_max_power(pdo.max_power)
            self.controls.usbc_set_local_sink_pdo_max_voltage(pdo.max_voltage)
            self.controls.usbc_set_local_sink_pdo_min_voltage(pdo.min_voltage)
