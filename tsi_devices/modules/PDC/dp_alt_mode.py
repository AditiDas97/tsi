from tsi.tsi_devices.libs.lib_tsi.tsi import *


class UfpDCaps:

    def __init__(self):
        self.c_4DPLanes = True
        self.d_2DPLanes_USBSS = True
        self.e_4DPLanes = True


class DfpDCaps:

    def __init__(self):
        self.c_4DPLanes = True
        self.d_2DPLanes_USBSS = True
        self.e_4DPLanes = True


class USBCDPAltMode:

    def __init__(self):
        self.autoEnter = True
        self.enabled = False
        self.ufd_caps = UfpDCaps()
        self.dfp_caps = DfpDCaps()
        self.multiFunction = False
        self.dpToTypeCCableAdapterMode = False


class DpAltMode:

    def __init__(self, device):
        self.device = device

    def usbc_set_dp_alt_mode_setup(self, value):
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_USBC_DP_ALT_MODE_SETUP, value, c_uint32)

    def usbc_set_dp_alt_mode(self, te_role: bool, mode_type: str, autoenter=1):
        """TSI_USBC_DP_ALT_MODE_SETUP"""
        mode_type_dict = {'c': 1, 'd': 2, 'e': 4}
        if mode_type.lower() in ['c', 'd', 'e']:
            old_mode = self.usbc_get_dp_alt_mode()
            if te_role:
                old_mode &= ~ (7 << 2)
                old_mode |= (mode_type_dict.get(mode_type) << 2)
            else:
                old_mode &= ~ (7 << 10)
                old_mode |= (mode_type_dict.get(mode_type) << 10)
            old_mode &= ~ (1 << 30)
            if mode_type == 'd':
                old_mode |= (1 << 30)
            else:
                old_mode |= (0 << 30)
            old_mode &= ~ (autoenter << 31)
            old_mode |= (autoenter << 31)
            self.usbc_set_dp_alt_mode_setup(old_mode)
        else:
            print("Invalid mode type. Need to select from list: C, D, E.")

    def usbc_get_dp_alt_mode(self):
        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_USBC_DP_ALT_MODE_SETUP, c_uint32)

        return result[1]

    def usbc_alt_mode_sink_enter_2_lanes_mode_d(self):

        old_mode = self.usbc_get_dp_alt_mode()
        old_mode &= ~ (7 << 2)
        old_mode |= (2 << 2)
        self.usbc_set_dp_alt_mode_setup(old_mode)

    def usbc_alt_mode_sink_enter_4_lanes_mode_c(self):

        old_mode = self.usbc_get_dp_alt_mode()
        old_mode &= ~ (7 << 2)
        old_mode |= (1 << 2)
        self.usbc_set_dp_alt_mode_setup(old_mode)

    def usbc_alt_mode_sink_enter_4_lanes_mode_e(self):

        old_mode = self.usbc_get_dp_alt_mode()
        old_mode &= ~ (7 << 2)
        old_mode |= (4 << 2)
        self.usbc_set_dp_alt_mode_setup(old_mode)

    def usbc_alt_mode_source_enter_2_lanes_mode_d(self):

        old_mode = self.usbc_get_dp_alt_mode()
        old_mode &= ~ (7 << 10)
        old_mode |= (2 << 10)
        self.usbc_set_dp_alt_mode_setup(old_mode)

    def usbc_alt_mode_source_enter_4_lanes_mode_c(self):

        old_mode = self.usbc_get_dp_alt_mode()
        old_mode &= ~ (7 << 10)
        old_mode |= (1 << 10)
        self.usbc_set_dp_alt_mode_setup(old_mode)

    def usbc_alt_mode_source_enter_4_lanes_mode_e(self):

        old_mode = self.usbc_get_dp_alt_mode()
        old_mode &= ~ (7 << 10)
        old_mode |= (4 << 10)
        self.usbc_set_dp_alt_mode_setup(old_mode)

    def usbc_alt_mode_exit(self):

        value = 1
        self.usbc_set_dp_alt_mode_setup(value << 31)

    def usbc_alt_mode_command(self, value: int):

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_W_USBC_DP_ALT_MODE_COMMAND, value, c_int32)

    def usbc_alt_mode_disable(self):

        self.usbc_alt_mode_command(2)

    def usbc_alt_mode_multi_function(self, value: bool):

        old_mode = self.usbc_get_dp_alt_mode()
        old_mode &= ~ (1 << 30)
        old_mode |= (int(value) << 30)
        self.usbc_set_dp_alt_mode_setup(old_mode)

    def usbc_set_auto_enter(self, value: bool):
        old_mode = self.usbc_get_dp_alt_mode()
        old_mode &= ~ (1 << 31)
        old_mode |= (int(value) << 31)
        self.usbc_set_dp_alt_mode_setup(old_mode)

    def usbc_get_auto_enter(self):

        state = self.usbc_get_dp_alt_mode()

        return ((state >> 31) & 1) != 0

    def usbc_get_multi_function(self):

        state = self.usbc_get_dp_alt_mode()

        return ((state >> 30) & 1) != 0

    def usbc_get_dp_to_typeC_cable_adapter_mode(self):

        state = 0

        return (state >> 2 & 1) != 0

    def usbc_get_alt_mode_sink_enter_2_lanes_mode_d(self):

        state = self.usbc_get_dp_alt_mode()

        return ((state >> 2) & 1) != 0

    def usbc_get_alt_mode_sink_enter_4_lanes_mode_c(self):

        state = self.usbc_get_dp_alt_mode()

        return ((state >> 3) & 1) != 0

    def usbc_get_alt_mode_sink_enter_4_lanes_mode_e(self):

        state = self.usbc_get_dp_alt_mode()

        return ((state >> 4) & 1) != 0

    def usbc_get_alt_mode_source_enter_2_lanes_mode_d(self):

        state = self.usbc_get_dp_alt_mode()

        return ((state >> 10) & 1) != 0

    def usbc_get_alt_mode_source_enter_4_lanes_mode_c(self):

        state = self.usbc_get_dp_alt_mode()

        return ((state >> 11) & 1) != 0

    def usbc_get_alt_mode_source_enter_4_lanes_mode_e(self):

        state = self.usbc_get_dp_alt_mode()

        return ((state >> 12) & 1) != 0
