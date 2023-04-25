from .capture import *


class CapturerHdTx(Capturer):

    def __init__(self, device):
        super().__init__(device)
        self.device = device

    @staticmethod
    def hdtx_config_event_filter(event_types=('HPD',)):

        event_filter = 0
        if 'HPD' in event_types:
            event_filter |= TSI_HDTX_LOG_CTRL_VALUE_HPD
        if 'I2C' in event_types:
            event_filter |= TSI_HDTX_LOG_CTRL_VALUE_I2C
        if 'CEC' in event_types:
            event_filter |= TSI_HDTX_LOG_CTRL_VALUE_CEC

        return event_filter

    def hdtx_start_event_capture(self, event_types: tuple):

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_EVCAP_CTRL, 0)
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_HDTX_LOG_CTRL_RW, 0)

        event_filter = self.hdtx_config_event_filter(event_types)

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_HDTX_LOG_CTRL_RW, event_filter)
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_EVCAP_CTRL, 1)

    def hdtx_stop_event_capture(self):
        """

        Stops capture and downloads all captured events.

        Parameters
        ----------
        self : HDRX (TSIDevice)
            Indicates the device on which the operation is to be carried out

        Returns
        -------
        result : TSI_RESULT
            Result of the operation
        """

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_HDTX_LOG_CTRL_RW, 0)
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_EVCAP_CTRL, 0)

        return TSI_SUCCESS

    def hdtx_download_captured_events(self, save_to_bin=True, save_to_txt=False, path_to_save=""):
        """"""
        return self.download_captured_events(save_to_bin, save_to_txt, path_to_save)

    def hdtx_capture_events_selected_packets(self, list_packets: tuple, time_for_capture: int = 1, save_to_bin=True,
                                             save_to_txt=False, path_to_save=""):

        self.hdtx_start_event_capture(list_packets)

        time.sleep(time_for_capture)

        events = self.download_captured_events(save_to_bin, save_to_txt, path_to_save)
        self.hdtx_stop_event_capture()
        parsed_events = []

        for data in events:
            result = TSI_ParseEvent(data)
            if result[2] in list_packets:
                parsed_events.append(result)

        return parsed_events
