from .capture import *


class CapturerHdRx(Capturer):

    def __init__(self, device):
        super().__init__(device)
        self.device = device

    @staticmethod
    def hdrx_config_event_filter(event_types=('Packets',)):

        event_filter = 0
        if 'HPD' in event_types:
            event_filter |= TSI_HDRX_LOG_CTRL_VALUE_HPD
        if 'Packets' in event_types:
            event_filter |= TSI_HDRX_LOG_CTRL_VALUE_INFO
        if 'I2C' in event_types:
            event_filter |= TSI_HDRX_LOG_CTRL_VALUE_I2C
        if 'CEC' in event_types:
            event_filter |= TSI_HDRX_LOG_CTRL_VALUE_CEC

        return event_filter

    def hdrx_start_event_capture(self, event_types: tuple):

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_EVCAP_CTRL, 0)
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_HDRX_LOG_CTRL_RW, 0)

        event_filter = self.hdrx_config_event_filter(event_types)

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_HDRX_LOG_CTRL_RW, event_filter)
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_EVCAP_CTRL, 1)


    def hdrx_stop_event_capture(self):
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

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_HDRX_LOG_CTRL_RW, 0)
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_EVCAP_CTRL, 0)

        return TSI_SUCCESS

    def hdrx_download_captured_frames(self, count, frame_type='RAW') -> list:
        """

        Downloads captured video frames.

        Parameters
        ----------
        self : HDRX (TSIDevice)
            Indicates the device on which the operation is to be carried out
        count : int
            Number of frames to download
        frame_type : str
            'RGB', 'RAW' or 'Native'
        Returns
        ------
        frames_list : list
            List of the captured video frames (see struct of each frame in class Frame)

        """

        events = self.download_captured_events()

        while not self.frame_capture_is_ready():
            time.sleep(0.05)
            more_events = self.download_captured_events()
            events += more_events

        frames = []

        for i in range(count):
            try:
                result = TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_VIDCAP_CAPTURE_NEXT_W, 0,
                                               print_error=False)
                if result == TSI_ERROR_DATA_PROTECTION_ENABLED:
                    warnings.warn("Video data is HDCP protected. Capturing is not available.")
                    return frames
            except BaseException:
                return frames

            print('Downloading frame {} of {}'.format(i + 1, count))

            min_buffer_size = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_VIDCAP_MIN_BUFFER_SIZE, c_int)[1]

            frame_data = bytearray(TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_VIDCAP_FRAME_DATA, c_byte,
                                                         min_buffer_size)[1])

            frame_attributes = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_VIDCAP_FRAME_HEADER_R,
                                                     c_uint32, 8)[1]

            frame = self.parse_attributes(frame_attributes[6])
            frame.type = frame_type
            print('frame size=', len(frame_data))

            frame.width = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_VIDCAP_WIDTH, c_int)[1]
            frame.height = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_VIDCAP_HEIGHT, c_int)[1]
            frame.add_data(frame_data)

            TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_W_HDRX_TIM_COMMAND, 1)
            timestamp = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_VIDCAP_TIMESTAMP, c_uint64)[1]
            framerate = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_HDRX_TIM_FRATE, c_uint32)[1]

            total_frame_duration = 10000000 * 1000 / framerate

            frame.end_timestamp_us = timestamp / 10
            frame.start_timestamp_us = (timestamp - total_frame_duration) / 10

            frame.setting_src_object()

            frames.append(frame)

        for data in events:
            result, parsed = TSI_ParseEvent(data, to_dict=True)
            event = EventData(parsed['timestamp'], parsed['data'], parsed['type'])
            if result == TSI_SUCCESS:
                timestamp_us = event.timestamp / 10
                for frame in frames:
                    if frame.start_timestamp_us <= timestamp_us <= frame.end_timestamp_us:
                        if event.type == 'SDP':
                            frame.sdp_list.append(event.event_data)
                        if event.type.find('MSA') != -1:
                            frame.msa = event.event_data

        return frames

    def hdrx_buffered_captured_frames(self, path: str, count: int = 1, frame_type: str = 'RAW', save_to_bin=True,
                                      save_to_bmp=False, save_to_ppm=False):
        frames = self.hdrx_download_captured_frames(count, frame_type)
        if not os.path.exists(path):
            os.makedirs(path)
        else:
            shutil.rmtree(path)
            os.makedirs(path)

        i = 0
        for fr in frames:
            if save_to_bin:
                file = open(path + r'\video_{count}_[{w}x{h}_{cs}_{bpc}bpc].bin'.format(count=i, w=fr.width,
                                                                                        h=fr.height, bpc=fr.bpc,
                                                                                        cs=uicl.dict_colorspace.get(
                                                                                            fr.colorspace
                                                                                        )),
                            'wb')
                file.write(fr.data_ptr)
                file.close()
            if save_to_bmp:
                fr.save_to_bmp(path + r'\video_{count}_[{w}x{h}_{cs}_{bpc}bpc]'.
                               format(count=i, w=fr.width, h=fr.height, bpc=fr.bpc,
                                      cs=uicl.dict_colorspace.get(fr.colorspace)))
            if save_to_ppm:
                fr.save_to_ppm(path + r'\video_{count}_[{w}x{h}_{cs}_{bpc}bpc]'.
                               format(count=i, w=fr.width, h=fr.height, bpc=fr.bpc,
                                      cs=uicl.dict_colorspace.get(fr.colorspace)))
            i += 1

    def hdrx_start_capture_frames(self, count):
        """

        A sample usecase of frame capture.
        Captures a number of video frames along with their MSA and SDP.

        Parameters
        ----------
        self : HDRX (TSIDevice)
            Indicates the device on which the operation is to be carried out
        count : int
            Number of frames to be captured
        """
        self.hdrx_start_event_capture(('HPD', 'I2C'))

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_W_CAP_COMMAND, 2)
        cap_config = 1
        cap_config |= (1 << 1)
        cap_config |= (1 << 3)
        cap_config |= (1 << 5)
        cap_config |= (count << 8)
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_CAP_CONFIG, cap_config)
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_W_CAP_COMMAND, 1)
        print('Started capture of {} frames'.format(count))

    def hdrx_stop_capture_frames(self):
        """"""
        self.hdrx_stop_event_capture()
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_W_CAP_COMMAND, 2)

    def hdrx_capture_events_selected_packets(self, list_packets: tuple, time_for_capture: int = 1, save_to_bin=True,
                                             save_to_txt=False, path_to_save=""):

        self.hdrx_start_event_capture(list_packets)

        time.sleep(time_for_capture)

        events = self.download_captured_events(save_to_bin, save_to_txt, path_to_save)
        self.hdrx_stop_event_capture()
        parsed_events = []

        for data in events:
            result = TSI_ParseEvent(data)
            if result[2] in list_packets:
                parsed_events.append(result)

        return parsed_events

    def hdrx_download_captured_events(self, save_to_bin=True, save_to_txt=False, path_to_save=""):
        """"""
        return self.download_captured_events(save_to_bin, save_to_txt, path_to_save)
