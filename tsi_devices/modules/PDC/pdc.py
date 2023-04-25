from .capabilities import *
from .power_source import *
from .power_sink import *
from .dp_alt_mode import *
from .status import *
from .cable_info import *


class Pdc:

    def __init__(self, device):
        self.device = device
        self.controls = Controls(self.device)
        self.power_sink = PowerSink(self.device, self.controls)
        self.power_source = PowerSource(self.device, self.controls)
        self.capabilities = Capabilities(self.device)
        self.alt_mode = DpAltMode(self.device)
        self.status = StatusForm(self.device)
        self.cable = CableInfo(self.device)

    def usbc_set_pwr_command(self, command):
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_USBC_PWR_COMMAND, command, c_int32)

    def usbc_set_source_power_objects(self):
        self.usbc_set_pwr_command(1)

    def usbc_set_sink_power_objects(self):
        self.usbc_set_pwr_command(2)

    def usbc_set_role_control(self, command: int):

        assert command in [1, 2, 3]
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_W_USBC_ROLE_CONTROL, command, c_int32)

    def usbc_set_dr_swap(self):

        self.usbc_set_role_control(1)

    def usbc_set_pr_swap(self):

        self.usbc_set_role_control(2)

    def usbc_set_vconn_swap(self):

        self.usbc_set_role_control(3)

    def usbc_set_fr_swap(self):

        self.status.usbc_set_pdc_control(0x6)

    def usbc_send_orientation(self, value: bool):

        self.status.usbc_set_cable_control(2 if value else 1)

    def usbc_set_cc_pull_up(self, value):

        assert 3 <= value <= 5
        self.status.usbc_set_cable_control(value)

    def usbc_enable_adc_data_scanner(self):

        self.usbc_set_adc_ctrl_command(1)

    def usbc_disable_adc_data_scanner(self):

        self.usbc_set_adc_ctrl_command(2)

    def usbc_set_adc_ctrl_command(self, value):

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_W_USBC_ADC_CTRL, value)

    def usbc_set_pd_command(self, command: int):

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_W_USBC_PD_COMMAND, command, c_int32)
