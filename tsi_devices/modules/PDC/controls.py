from tsi.tsi_devices.libs.lib_tsi.tsi import *


class ControlsInfo:

    def __init__(self):
        self.autoNegotiatePowerContract = None
        self.rdoGiveBackFlag = None
        self.rdoNoUSBSuspend = None
        self.autoMinPower = False
        self.minPower = 0
        self.cableDiffPairsUSB2 = None
        self.externallyPowered = False
        self.capPDSource = True
        self.capPDSink = True

    def get_info_about_class(self):
        return self.__dict__


def set_bits_by_index(data: int, start_index: int, count_of_bits: int, new_bits: int) -> int:

    assert new_bits < 2**count_of_bits
    mask = 0xffffffff
    mask = mask >> (count_of_bits + start_index)
    mask = (mask << (count_of_bits + start_index)) + (2**start_index - 1)
    return (mask & data) + (new_bits << start_index)


class Controls:

    def __init__(self, device):
        self.device = device

    def usbc_get_pwr_contract_control(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_USBC_PWR_CONTRACT_CONTROL, c_int32)

        return result[1]

    def usbc_set_pwr_contract_control(self, data: int):

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_USBC_PWR_CONTRACT_CONTROL, data, c_int32)

    def usbc_get_hardware_options(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_USBC_TE_HW_CONFIGURATION, c_uint32)

        return result[1]

    def usbc_get_auto_negotiate_pc(self):

        result = self.usbc_get_pwr_contract_control()

        return result & 1

    def usbc_get_use_battery_PDO(self):

        result = self.usbc_get_pwr_contract_control()

        return (result >> 1) & 1

    def usbc_get_use_variable_PDO(self):

        result = self.usbc_get_pwr_contract_control()

        return (result >> 2) & 1

    def usbc_get_contract_preference(self):

        result = self.usbc_get_pwr_contract_control()

        return (result >> 4) & 3

    def usbc_get_rdo_no_usb_suspend(self):

        result = self.usbc_get_pwr_contract_control()

        return (result >> 6) & 1

    def usbc_get_rdo_give_back_flag(self):

        result = self.usbc_get_pwr_contract_control()

        return (result >> 7) & 1

    def usbc_get_auto_min_power(self):

        result = self.usbc_get_pwr_contract_control()

        return (result >> 8) & 1

    def usbc_get_manual_power_contract_selection(self):

        result = self.usbc_get_pwr_contract_control()

        return (result >> 31) & 1

    def usbc_get_min_power(self):

        result = self.usbc_get_pwr_contract_control()

        return 250 * ((result >> 16) & 0x3FF)

    def usbc_get_cable_diff_pairs_usb2(self):

        result = self.usbc_get_hardware_options()
        result = bool((result >> 3 & 1) != 0)

        return 2 if result else 1

    def usbc_get_controls_info(self):

        controls = ControlsInfo()

        controls.autoNegotiatePowerContract = self.usbc_get_auto_negotiate_pc()
        controls.rdoGiveBackFlag = self.usbc_get_rdo_give_back_flag()
        controls.rdoNoUSBSuspend = self.usbc_get_rdo_no_usb_suspend()
        controls.autoMinPower = self.usbc_get_auto_min_power()
        controls.minPower = self.usbc_get_min_power()
        controls.cableDiffPairsUSB2 = self.usbc_get_cable_diff_pairs_usb2()
        controls.externallyPowered = False
        controls.capPDSource = True
        controls.capPDSink = True

        return controls

    def usbc_get_pdo_count(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_PDO_COUNT_R, c_int32)

        return result[1]

    def usbc_set_pwr_contract_select(self, data: int):

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_USBC_PWR_CONTRACT_SELECT, data, c_int32)

    def usbc_set_priority_and_index(self, selected_by_index: bool = False, index: int = 0, priority: int = 0):

        if selected_by_index:
            assert index > 0
            priority = 0
        else:
            assert priority in [0, 1, 2]
            index = 0

        data = self.usbc_get_pwr_contract_control()
        if selected_by_index:
            data |= 1 << 31
            self.usbc_set_pwr_contract_control(data)
            self.usbc_set_pwr_contract_select(index)
        else:
            contractPriority = priority << 4
            data = set_bits_by_index(contractPriority, 4, 2, 0) + contractPriority
            data &= ~(1 << 31)
            self.usbc_set_pwr_contract_control(data)

    def usbc_set_local_sink_pdo_select(self, value):
        """"""
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_USBC_PWR_LOCAL_SINK_PDO_SELECT, value, c_int32)

    def usbc_set_local_sink_pdo_type(self, value):
        """"""
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_USBC_PWR_LOCAL_SINK_PDO_TYPE, value, c_int32)

    def usbc_set_local_sink_pdo_max_current(self, value):
        """"""
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_USBC_PWR_LOCAL_SINK_PDO_MAX_CURRENT, value, c_int32)

    def usbc_set_local_sink_pdo_voltage(self, value):
        """"""
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_USBC_PWR_LOCAL_SINK_PDO_VOLTAGE, value, c_int32)

    def usbc_set_local_sink_pdo_fixed_bits(self, value):
        """"""
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_USBC_PWR_LOCAL_SINK_PDO_FIXED_SUPPLY_BITS_25_TO_29, value,
                              c_int32)

    def usbc_set_local_sink_pdo_max_voltage(self, value):
        """"""
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_USBC_PWR_LOCAL_SINK_PDO_MAX_VOLTAGE, value, c_int32)

    def usbc_set_local_sink_pdo_min_voltage(self, value):
        """"""
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_USBC_PWR_LOCAL_SINK_PDO_MIN_VOLTAGE, value, c_int32)

    def usbc_set_local_sink_pdo_max_power(self, value):
        """"""
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_USBC_PWR_LOCAL_SINK_PDO_MAX_POWER, value, c_int32)

    def usbc_set_local_source_pdo_select(self, value):
        """"""
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_USBC_PWR_LOCAL_SOURCE_PDO_SELECT, value, c_int32)

    def usbc_set_local_source_pdo_type(self, value):
        """"""
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_USBC_PWR_LOCAL_SOURCE_PDO_TYPE, value, c_int32)

    def usbc_set_local_source_pdo_max_current(self, value):
        """"""
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_USBC_PWR_LOCAL_SOURCE_PDO_MAX_CURRENT, value, c_int32)

    def usbc_set_local_source_pdo_voltage(self, value):
        """"""
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_USBC_PWR_LOCAL_SOURCE_PDO_VOLTAGE, value, c_int32)

    def usbc_set_local_source_pdo_peak_current(self, value):
        """"""
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_USBC_PWR_LOCAL_SOURCE_PDO_PEAK_CURRENT, value, c_int32)

    def usbc_set_local_source_pdo_fixed_bits(self, value):
        """"""
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_USBC_PWR_LOCAL_SOURCE_PDO_FIXED_SUPPLY_BITS_25_TO_29, value,
                              c_int32)

    def usbc_set_local_source_pdo_max_voltage(self, value):
        """"""
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_USBC_PWR_LOCAL_SOURCE_PDO_MAX_VOLTAGE, value, c_int32)

    def usbc_set_local_source_pdo_min_voltage(self, value):
        """"""
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_USBC_PWR_LOCAL_SOURCE_PDO_MIN_VOLTAGE, value, c_int32)

    def usbc_set_local_source_pdo_max_power(self, value):
        """"""
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_USBC_PWR_LOCAL_SOURCE_PDO_MAX_POWER, value, c_int32)
