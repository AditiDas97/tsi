from tsi.tsi_devices.libs.lib_tsi.tsi import *
from ..device_constants import *


class CapabilitiesInfo:

    def __init__(self):
        self.initialRole = None
        self.rejectPR_Swap = None
        self.rejectDR_Swap = None
        self.rejectFR_Swap = None
        self.rejectVconnSwap = None
        self.audioAccessory = None
        self.debugAccessory = None
        self.ccPullUp = None
        self.tryBehavior = None
        self.tryBehaviorSNK = None
        self.tryBehaviorSRC = None
        self.FRSwap = None
        self.CableSim = None
        self.usb2Bypass = None
        self.usb3Bypass = None

    def get_info_about_class(self):
        return self.__dict__


class Capabilities:

    def __init__(self, device):
        self.device = device

    def usbc_get_pdc_state(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_PDC_STATE, c_uint32)

        return result[1]

    def usbc_set_initial_role(self, command: int):

        assert command in [0, 1, 2, 3]
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_W_USBC_INITIAL_ROLE, command, c_int32)

    def usbc_set_initial_role_ufp(self):

        self.usbc_set_initial_role(1)

    def usbc_set_initial_role_dfp(self):

        self.usbc_set_initial_role(2)

    def usbc_set_initial_role_drp(self):

        self.usbc_set_initial_role(3)

    def usbc_get_initial_role(self):

        result = self.usbc_get_pdc_state()
        result = (result >> PDC_STATE_DEV_ROLE_POS) & 0x3

        return result

    def usbc_get_cc_pull_up(self):

        result = self.usbc_get_pdc_state()
        result = (result >> PDC_STATE_PULLUP_POS) & 0x3

        return result

    def usbc_get_reject_dr_swap(self):

        result = self.usbc_get_pdc_state()

        return not (result & PDC_STATE_DR_SWAP_EN)

    def usbc_get_reject_pr_swap(self):

        result = self.usbc_get_pdc_state()

        return not (result & PDC_STATE_PR_SWAP_EN)

    def usbc_get_reject_vconn_swap(self):

        result = self.usbc_get_pdc_state()

        return not (result & PDC_STATE_VCONN_SWAP_EN)

    def usbc_get_reject_fr_swap(self):

        result = self.usbc_get_pdc_state()

        return not (result & PDC_STATE_FR_SWAP_EN)

    def usbc_get_audio_accessory(self):

        result = self.usbc_get_pdc_state()

        return result & PDC_STATE_AUDIO_ACCESSORY

    def usbc_get_debug_accessory(self):

        result = self.usbc_get_pdc_state()

        return result & PDC_STATE_DEBUG_ACCESSORY

    def usbc_get_try_behavior(self):

        result = self.usbc_get_pdc_state()
        result = (result >> PDC_STATE_DRP_TRY_MODE_POS) & 0x3

        return result

    def usbc_get_pdc_caps(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_PDC_CAPS, c_uint32)

        return result[1]

    def usbc_get_try_behavior_snk(self):

        result = self.usbc_get_pdc_caps()

        return result & 0x1

    def usbc_get_try_behavior_src(self):

        result = self.usbc_get_pdc_caps()

        return (result >> 1) & 0x1

    def usbc_get_fr_swap(self):

        result = self.usbc_get_pdc_caps()

        return (result >> 2) & 0x1

    def usbc_get_cable_sim(self):

        result = self.usbc_get_pdc_caps()

        return (result >> 3) & 0x1

    def usbc_get_hw_status(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_PDC_HW_STATUS, c_uint32)

        return result[1]

    def usbc_get_usb_2_bypass(self):

        result = self.usbc_get_hw_status()

        return (result >> 4) & 1

    def usbc_get_usb_3_bypass(self):

        result = self.usbc_get_hw_status()

        return (result >> 12) & 1

    def usbc_get_capability_info(self):

        capability = CapabilitiesInfo()

        capability.initialRole = self.usbc_get_initial_role()
        capability.rejectPR_Swap = self.usbc_get_reject_pr_swap()
        capability.rejectDR_Swap = self.usbc_get_reject_dr_swap()
        capability.rejectFR_Swap = self.usbc_get_reject_fr_swap()
        capability.rejectVconnSwap = self.usbc_get_reject_vconn_swap()
        capability.audioAccessory = self.usbc_get_audio_accessory()
        capability.debugAccessory = self.usbc_get_debug_accessory()
        capability.ccPullUp = self.usbc_get_cc_pull_up()
        capability.tryBehavior = self.usbc_get_try_behavior()
        capability.tryBehaviorSNK = self.usbc_get_try_behavior_snk()
        capability.tryBehaviorSRC = self.usbc_get_try_behavior_src()
        capability.FRSwap = self.usbc_get_fr_swap()
        capability.CableSim = self.usbc_get_cable_sim()
        capability.usb2Bypass = self.usbc_get_usb_2_bypass()
        capability.usb3Bypass = self.usbc_get_usb_3_bypass()

        return capability
