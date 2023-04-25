from .capture import *


class CapturerDpTx(Capturer):

    def __init__(self, device):
        super().__init__(device)

    @staticmethod
    def dptx_config_event_filter(self, event_types=('AUX',)):

        event_filter = 0
        if 'AUX' in event_types:
            event_filter |= TSI_DPTX_LOG_CONTROL_VALUE_AUX
        if 'HPD' in event_types:
            event_filter |= TSI_DPTX_LOG_CONTROL_VALUE_HPD

        return event_filter

    def dptx_start_event_capture(self, event_types=('AUX',)):

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_EVCAP_CTRL, 0)
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_DPTX_LOG_CTRL_RW, 0)

        event_filter = self.dptx_config_event_filter(event_types)

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_DPTX_LOG_CTRL_RW, event_filter)
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_EVCAP_CTRL, 1)

        config = 1
        config |= (1 << 5)
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_EVCAP_EVENT_SRC_EN, UCD_ALL_EVENTS)
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_CAP_CONFIG, config)

    def dptx_stop_event_capture(self):

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_DPTX_LOG_CTRL_RW, 0)
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_EVCAP_CTRL, 0)

        return TSI_SUCCESS

    def dptx_download_captured_events(self, save_to_bin=True, save_to_txt=False, path_to_save=""):
        """"""
        return self.download_captured_events(save_to_bin, save_to_txt, path_to_save)

    def dptx_capture_events_selected_packets(self, list_packets: tuple, time_for_capture=1, save_to_bin=True,
                                             save_to_txt=False, path_to_save=""):

        self.dptx_start_event_capture(list_packets)

        time.sleep(time_for_capture)

        events = self.download_captured_events(save_to_bin, save_to_txt, path_to_save)
        self.dptx_stop_event_capture()
        parsed_events = []

        for data in events:
            result = TSI_ParseEvent(data)
            if result[2] in list_packets:
                parsed_events.append(result)

        return parsed_events
