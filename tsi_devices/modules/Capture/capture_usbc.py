from .capture_dprx import *


class CapturerUsbc(CapturerDpRx):

    def __init__(self, device):
        super().__init__(device)

    def usbc_start_event_capture(self, event_types=('PD',)):

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_EVCAP_CTRL, 0)
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_PDC_LOG_CTRL_RW, 0)

        event_filter = self.dprx_config_event_filter(event_types)

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_PDC_LOG_CTRL_RW, event_filter)
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_EVCAP_CTRL, 1)

        time.sleep(1)

    def usbc_stop_event_capture(self):

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_PDC_LOG_CTRL_RW, 0)
        self.dprx_stop_event_capture()

        return TSI_SUCCESS
