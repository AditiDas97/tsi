def fill_pdo(pdos, device_role):
    """
    device_role: 1 - source, 0 - sink
    """
    pdo = PDO()
    pdo_data = pdos
    pdo_type = (pdo_data >> 30) & 3
    if pdo_type == 0:
        maxCurrent = (pdos & 0x03ff) * 10
        voltage = ((pdos >> 10) & 0x03ff) * 50
        role = (pdos >> 29) & 1
        usb_communications_capable = (pdos >> 26) & 1
        dual_role_data = (pdos >> 25) & 1
        unchunked_extended_messages_supported = (pdos >> 24) & 1
        if device_role:
            peakCurrent = (pdos >> 20) & 3
            usb_suspend_supported = (pdos >> 28) & 1
            externally_powered = (pdos >> 27) & 1
            pdo.assign_settings(max_current=maxCurrent, voltage=voltage, peak_current=peakCurrent, is_source=role,
                                usb_suspend_supported=usb_suspend_supported, externally_powered=externally_powered,
                                usb_communications_capable=usb_communications_capable,
                                dual_role_data=dual_role_data,
                                unchunked_extended_messages_supported=unchunked_extended_messages_supported,
                                pdo_type=pdo_type)
        else:
            higher_capability = (pdos >> 28) & 1
            unconstrained_power = (pdos >> 27) & 1
            pdo.assign_settings(max_current=maxCurrent, voltage=voltage, is_source=role, dual_role_data=dual_role_data,
                                usb_communications_capable=usb_communications_capable,
                                unchunked_extended_messages_supported=unchunked_extended_messages_supported,
                                pdo_type=pdo_type, unconstrained_power=unconstrained_power,
                                higher_capability=higher_capability)

    elif pdo_type == 1:
        maxPower = (pdos & 0x03ff) * 250
        maxVoltage = ((pdos >> 20) & 0x03ff) * 50
        minVoltage = ((pdos >> 10) & 0x03ff) * 50
        pdo.assign_settings(max_power=maxPower, max_voltage=maxVoltage, min_voltage=minVoltage,
                            pdo_type=pdo_type)
    elif pdo_type == 2:
        maxCurrent = (pdos & 0x03ff) * 10
        maxVoltage = ((pdos >> 20) & 0x03ff) * 50
        minVoltage = ((pdos >> 10) & 0x03ff) * 50
        pdo.assign_settings(max_current=maxCurrent, max_voltage=maxVoltage, min_voltage=minVoltage,
                            pdo_type=pdo_type)
    return pdo


class PdoInfo:

    def __init__(self):
        self.szPDOsSupported = None
        self.pdos = []

    def get_info_about_class(self):
        return self.__dict__

    def print_info(self):
        print('szPDOsSupported = ', self.szPDOsSupported)
        for i in range(7):
            print('source PDO {0} = {1}'.format(i + 1, self.pdos[i].get_info_about_class()))


class PowerContractConrol:

    def __init__(self, auto_negotiate_flag=0, use_battery_PDO=0, use_variable_PDO=0, communication_capable_flag=0,
                 contract_preference=0, no_usb_suspend_flag=0, give_back_flag=0, automatic_minimum_power=0,
                 minimum_required_power=0, manual_power_contract_selection=0):
        self.auto_negotiate_flag = auto_negotiate_flag
        self.use_battery_PDO = use_battery_PDO << 1
        self.use_variable_PDO = use_variable_PDO << 2
        self.communication_capable_flag = communication_capable_flag << 3
        self.contract_preference = contract_preference << 4
        self.no_usb_suspend_flag = no_usb_suspend_flag << 6
        self.give_back_flag = give_back_flag << 7
        self.automatic_minimum_power = automatic_minimum_power << 8
        self.minimum_required_power = minimum_required_power << 16
        self.manual_power_contract_selection = manual_power_contract_selection << 31

    def get_pcc_value(self):

        return self.auto_negotiate_flag + self.use_battery_PDO + self.use_variable_PDO + \
               self.communication_capable_flag + self.contract_preference + self.no_usb_suspend_flag + \
               self.give_back_flag + self.automatic_minimum_power + self.minimum_required_power + \
               self.manual_power_contract_selection


class PDO:

    def __init__(self):
        self.role = None
        self.pdo_selected = None
        self.pdo_type = None
        self.voltage = None
        self.max_voltage = None
        self.min_voltage = None
        self.max_current = None
        self.peak_current = None
        self.max_power = None
        self.fixed_bits = None
        self.pdos = None
        self.usb_suspend_supported = None
        self.externally_powered = None
        self.usb_communications_capable = None
        self.dual_role_data = None
        self.unchunked_extended_messages_supported = None
        self.higher_capability = None
        self.unconstrained_power = None

    def assign_settings(self, is_source=False, pdo_selected=0, pdo_type=0, voltage=0, max_voltage=0, min_voltage=0,
                        max_current=0, peak_current=0, max_power=0, fixed_bits=0, pdos=None,
                        usb_suspend_supported=None, externally_powered=None, usb_communications_capable=None,
                        dual_role_data=None, unchunked_extended_messages_supported=None,
                        higher_capability=None, unconstrained_power=None):
        self.role = is_source
        self.pdo_selected = pdo_selected
        self.pdo_type = pdo_type
        self.voltage = voltage
        self.max_voltage = max_voltage
        self.min_voltage = min_voltage
        self.max_current = max_current
        self.peak_current = peak_current
        self.max_power = max_power
        self.fixed_bits = fixed_bits
        self.pdos = pdos
        self.usb_suspend_supported = usb_suspend_supported
        self.externally_powered = externally_powered
        self.usb_communications_capable = usb_communications_capable
        self.dual_role_data = dual_role_data
        self.unchunked_extended_messages_supported = unchunked_extended_messages_supported
        self.higher_capability = higher_capability
        self.unconstrained_power = unconstrained_power

    def set_pdo_fixed_source(self, max_current, voltage, peak_current, fixed_bits):
        self.pdo_type = 1
        self.max_current = max_current
        self.voltage = voltage
        self.peak_current = peak_current
        self.fixed_bits = fixed_bits
        self.role = True

    def set_pdo_variable_source(self, max_current, max_voltage, min_voltage):
        self.pdo_type = 2
        self.max_current = max_current
        self.max_voltage = max_voltage
        self.min_voltage = min_voltage
        self.role = True

    def set_pdo_battery_source(self, max_power, max_voltage, min_voltage):
        self.pdo_type = 3
        self.max_power = max_power
        self.max_voltage = max_voltage
        self.min_voltage = min_voltage
        self.role = True

    def set_pdo_fixed_sink(self, max_current, voltage, fixed_bits=0):
        self.pdo_type = 1
        self.max_current = max_current
        self.voltage = voltage
        self.fixed_bits = fixed_bits
        self.role = False

    def set_pdo_variable_sink(self, max_current, max_voltage, min_voltage):
        self.pdo_type = 2
        self.max_current = max_current
        self.max_voltage = max_voltage
        self.min_voltage = min_voltage
        self.role = False

    def set_pdo_battery_sink(self, max_power, max_voltage, min_voltage):
        self.pdo_type = 3
        self.max_power = max_power
        self.max_voltage = max_voltage
        self.min_voltage = min_voltage
        self.role = False

    def clear_values(self):
        self.role = 0
        self.pdo_selected = 0
        self.pdo_type = 0
        self.voltage = 0
        self.max_voltage = 0
        self.min_voltage = 0
        self.max_current = 0
        self.peak_current = 0
        self.max_power = 0
        self.fixed_bits = 0
        self.pdos = []

    def get_info_about_class(self):
        return self.__dict__
