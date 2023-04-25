from .tsi_rx import *
from .modules.PatternGenerator.PGHDRX import *
from .modules.SDP.sdp_hdrx import *
from .modules.Capture.capture_hdrx import *
from .modules.Link.LinkHDMI.link_hdrx import *


class HDRX(RX):

    def __init__(self, device: TSIDevice):
        """

        General class for HDMI device RX(sink) side. Inherited from class RX.

        The class contains the following fields:
        pg - Object of PatternGeneratorHdRx class. Allow to get some video information (video resolution, bpc,
        colorimetry, color mode and so on)
        link - Object of LinkRx class. Contain some control link device methods.
        sdp - Object of SdpHdRx class. Allows getting SDP frames.
        capturer - Object of CapturerHdRx class. Needed to capture, downloading and saving events and video frames.

        Parameters
        ----------
        device : TSIDevice
            Indicates the device on which the operation is to be carried out
        """

        index = -1
        dev_type = "HD"
        role = "RX"
        for item in device.get_ports_and_roles():
            if item[0] == "HD" and item[1] == "RX":
                index = item[2]
        if index == -1:
            raise AssertionError("Selected incorrect device: Incorrect device type or role")
        port_id = 0 if (len(device.get_ports_and_roles()) < 2) else index
        super().__init__(device)
        self.open_port(port_id, role, dev_type)
        self.read_info_from_device(self, port_id)
        self._pg = PatternGeneratorHdRx(device)
        self._sdp = SdpHdRx(device)
        self._capture = CapturerHdRx(device)
        self._link = LinkRx(device)

    def hdrx_get_link_status_all_info(self) -> LinkStatusHdrx:
        """

        Return the object of LinkStatusHdrx class. It contains information about device link status.

        Available info:
            tdms_clock_detected - info of tdms clock detected status (type: bool)
            clockRate - info of clock rate (type: bool)
            inputStreamLockStatus - info of input stream lock status (type: bool)
            linkMode - HDMI link mode (type: bool)
            line0_locked - info of line 0 locked (type: bool)
            line1_locked - info of line 1 locked (type: bool)
            line2_locked - info of line 2 locked (type: bool)
            hpd_status - info of HPD status (type: bool)
            linkModeFRL - info of link mode FRL (type: str)
            ltStatus - link training status (type: int)
            fltUpdate = False (type: bool)
            fltNoRetrain = False (type: bool)
            errorCounters = List of error counters for each lane (type: list)
            channelLock - List of channel lock for each lane (type: list)
            frlData = List of FRL data for each lane (type: list)

        Returns
        -------
        result : LinkStatusHdrx
            Link status HdRx data

        """
        link_status = LinkStatusHdrx()

        linkStatus = self.hdrx_get_link_status()
        hpdStatus = self.hdrx_get_hpd_status()

        link_status.inputStreamLockStatus = (linkStatus & 1)
        link_status.clockRate = True if (linkStatus & 2) else False
        link_status.inputStreamLockStatus = (linkStatus & 4) != 0
        link_status.linkMode = True if (linkStatus & 8) else False
        link_status.line0_locked = (linkStatus & 16) != 0
        link_status.line1_locked = (linkStatus & 32) != 0
        link_status.line2_locked = (linkStatus & 64) != 0
        link_status.hpd_status = (hpdStatus & 1) != 0
        link_status.linkModeFRL = dict_link_mode_frl.get(((linkStatus >> 9) & 0xF))
        link_status.ltStatus = (linkStatus >> 18) & 0x7
        link_status.fltUpdate = (linkStatus >> 17) & 0x1
        link_status.fltNoRetrain = (linkStatus >> 27) & 0x1
        link_status.channelLock[0] = (linkStatus >> 13) & 1
        link_status.channelLock[1] = (linkStatus >> 14) & 1
        link_status.channelLock[2] = (linkStatus >> 15) & 1
        link_status.channelLock[3] = (linkStatus >> 16) & 1
        link_status.frlData[0] = (linkStatus & (1 << 21))
        link_status.frlData[1] = (linkStatus & (1 << 22))
        link_status.frlData[2] = (linkStatus & (1 << 23))
        link_status.frlData[3] = (linkStatus & (1 << 24))

        errorCounters = self.hdrx_get_error_counters()
        link_status.errorCounters[0] = errorCounters & 0xFFFF
        link_status.errorCounters[1] = (errorCounters >> 16) & 0xFFFF
        link_status.errorCounters[2] = (errorCounters >> 32) & 0xFFFF
        link_status.errorCounters[3] = (errorCounters >> 48) & 0xFFFF

        if self.get_type().find("422") != -1:
            value = self.hdrx_get_ltp_req()
            value_2 = value
            for i in range(4):
                link_status.ffeLevel[i] = value[i]
                link_status.ltpReq[i] = value_2[i]

        return link_status

    def hdrx_get_arc_status_all_info(self) -> ARCStatusHdrx:
        """

        Return the object of ARCStatusHdrx class. It contains information about device ARC status.

        Available info:
            supported - ARC supported status (type: bool)
            loopbackSupportedTPG - SRC TPG supported status (type: bool)
            loopbackSupportedHDMI - SRC HDMI supported status (type: bool)
            loopbackSupportedDVI - SRC DVI supported status (type: bool)
            loopbackSupportedDP - SRC DP supported status (type: bool)
            loopbackSupportedSPDIF - SRC SPDIF supported status (type: bool)
            enabled - ARC enabled status (type: bool)
            singleMode - ARC single mode (type: bool)

        Returns
        -------
        result : ARCStatusHdrx
            ARC HdRx data

        """

        _arc_status = ARCStatusHdrx()

        _arc_status.supported = self.hdrx_get_arc_value_supported()
        _arc_status.loopbackSupportedTPG = self.hdrx_get_arc_value_supported_tpg()
        _arc_status.loopbackSupportedHDMI = self.hdrx_get_arc_value_supported_hdmi()
        _arc_status.loopbackSupportedDVI = self.hdrx_get_arc_value_supported_dvi()
        _arc_status.loopbackSupportedDP = self.hdrx_get_arc_value_supported_dp()
        _arc_status.loopbackSupportedSPDIF = self.hdrx_get_arc_value_supported_sdpif()
        _arc_status.enabled = self.hdrx_get_arc_value_supported_enabled()
        _arc_status.source = 1
        _arc_status.singleMode = True

        return _arc_status

    # Link Block
    def hdrx_get_crc_values(self, number: int) -> list:
        """

        Return red, green and blue CRC values for current input video stream.

        Parameters
        ----------
        number : int
            Number of captured crc

        Returns
        -------
        list:
            Element of list contain following info:
               crc red : int
                   CRC value for red component 0 - 63365
               crc green : int
                   CRC value for green component 0 - 63365
               crc blue : int
                   CRC value for blue component 0 - 63365

        """
        return self._link.hdrx_get_crc_values(number)

    def hdrx_get_link_status(self) -> int:
        """

        Return HDMI Link statu.
            Bits
            0 - Indicate that device detects clock on TMDS lanes: 0 - not detected, 1 - detected.
            1 - Clock rate: 0 - 3G, 1 - 6G.
            2 - Input stream lock status: 0 - Not Locked, 1 - Locked.
            3 - Link mode: 0 - HDMI mode, 1 - DVi mode.
            4..6 - Line lock bits.

        Returns
        -------
        result : int
            link status data

        """
        return self._link.hdrx_get_link_status()

    def hdrx_get_error_counters(self) -> int:
        """

        Return error counters for each lane.

        Returns
        -------
        result : int
            Error counter

        """

        return self._link.hdrx_get_error_counters()

    # Link Block: HPD
    def hdrx_set_link_control(self, state: bool) -> TSI_RESULT:
        """

        Set control the HDMI HPD signal:
            0 - will de-assert the HDP signal
            1 - will assert the HPD signal.

        Parameters
        ----------
        state : bool
            False(0) - de-assert the HDP signal, True(1) - assert the HPD signal

        Returns
        -------
        result : TSI_RESULT
            Result of operation.
        """

        return self._link.hdrx_set_link_control(state)

    def hdrx_get_hpd_status(self) -> bool:
        """

        Return HPD signal logical status:
            False(0) - HPD de-asserted
            True(1) - HPD asserted.

        Returns
        -------
        result : bool
            HPD status.
        """

        result = TSIX_TS_GetConfigItem(self.get_handle(), TSI_HDRX_HPD_STATUS_R, c_int)

        return (result[1] & 1) != 0

    # Link Block: TMDS
    def hdrx_get_input_stream_lock_status(self) -> bool:
        """

        Return current input stream lock status.

        Returns
        -------
        result : bool
            Status.

        """

        return self._link.tmds.hdrx_get_input_stream_lock_status()

    def hdrx_get_clock_rate(self) -> tuple:
        """

        Return current clock rate.

        Returns
        -------
        result : tuple
            Clock rate status, Displaying status as a string (1/10 3G mode" or "1/40 6G mode").
        """

        return self._link.tmds.hdrx_get_clock_rate()

    def hdrx_get_link_mode(self) -> tuple:
        """

        Return current link mode.

        Returns
        -------
        result : tuple
            Link mode, Displaying link mode as a string ("DVI" or "HDMI").

        """

        return self._link.tmds.hdrx_get_link_mode()

    def hdrx_get_lines_locked(self) -> tuple:
        """

        Returned current status of line lock bits.

        Returns
        -------
        result : tuple
            Lock bits values (bool).
        """

        return self._link.tmds.hdrx_get_lines_locked()

    def hdrx_set_arc_control(self, single_mode: bool, arc_loopback_audio_source: int):
        """

        Set-up and control ARC features on HDMI Inputs.

        Parameters
        ----------
        single_mode : bool
            ARC mode
        arc_loopback_audio_source : int
            ARC Data
        """
        self._link.tmds.hdrx_set_arc_control(single_mode, arc_loopback_audio_source)

    def hdrx_set_behavior(self, behavior: int):
        """

        Set HDMI behavior.

        Parameters
        ----------
        behavior : int
            0 - HDMI 1.4 Behavior
            1 - HDMI 2.0 Behavior
            2 - HDMI 2.1 Behavior

        """

        self._link.tmds.hdrx_set_behavior(behavior)

    def hdrx_get_behavior(self) -> int:
        """

        Return HDMI behavior.

        Returns
        -------
        result : int
            0 - HDMI 1.4 Behavior
            1 - HDMI 2.0 Behavior
            2 - HDMI 2.1 Behavior

        """

        return self._link.tmds.hdrx_get_behavior()

    def hdrx_get_arc_value_supported(self) -> bool:
        """

        Return to current ARC status information (ARC Supported).

        Returns
        -------
        result : bool
            True = Supported, False = Not supported
        """

        return self._link.tmds.hdrx_get_arc_value_supported()

    def hdrx_get_arc_value_supported_tpg(self) -> bool:
        """

        Return to current ARC status information.
        Internal ARC Audio generator is available.

        Returns
        -------
        result : bool
            True = Available, False = Not available
        """

        return self._link.tmds.hdrx_get_arc_value_supported_tpg()

    def hdrx_get_arc_value_supported_hdmi(self) -> bool:
        """

        Return to current ARC status information.
        Loop back from HDMI RX port supported.

        Returns
        -------
        result : bool
            True = Supported, False = Not supported
        """

        return self._link.tmds.hdrx_get_arc_value_supported_hdmi()

    def hdrx_get_arc_value_supported_dvi(self) -> bool:
        """

        Return to current ARC status information.
        Loop back from DVI RX port supported.

        Returns
        -------
        result : bool
            True = Supported, False = Not supported
        """

        return self._link.tmds.hdrx_get_arc_value_supported_dvi()

    def hdrx_get_arc_value_supported_dp(self) -> bool:
        """

        Return to current ARC status information.
        Loop back from DP RX port supported.

        Returns
        -------
        result : bool
            True = Supported, False = Not supported
        """

        return self._link.tmds.hdrx_get_arc_value_supported_dp()

    def hdrx_get_arc_value_supported_sdpif(self) -> bool:
        """

        Return to current ARC status information.
        Loop back from SPDIF RX port supported.

        Returns
        -------
        result : bool
            True = Supported, False = Not supported
        """

        return self._link.tmds.hdrx_get_arc_value_supported_sdpif()

    def hdrx_get_arc_value_supported_enabled(self) -> bool:
        """

        Return to current ARC status information. ARC Enabled.

        Returns
        -------
        result : bool
            True = ARC Is currently enabled, False = ARC Is disabled.
        """

        return self._link.tmds.hdrx_get_arc_value_supported_enabled()

    # Capture Block
    def hdrx_start_event_capture(self, event_types: tuple):
        """

        Starts capturing events.

        Parameters
        ----------
        event_types: tuple
            list of one or more of the following values:
                'HPD': hpd events
                'Packets': 'INFO' packets
                'I2C': I2C packets
        """

        self._capture.hdrx_start_event_capture(event_types)

    def hdrx_stop_event_capture(self):
        """

        Stops capture.

        """

        self._capture.hdrx_stop_event_capture()

    def hdrx_download_captured_frames(self, count, frame_type='RAW') -> list:
        """

        Downloads captured video frames.

        Parameters
        ----------
        count : int
            Number of frames to download
        frame_type : str
            'RGB', 'RAW' or 'Native'

        Returns
        ------
        frames_list : list
            Value (List) of the captured video frames (see struct of each frame in class Frame)

        """

        count = check_frame_size(self.hdrx_get_h_active(), self.hdrx_get_v_active(), self.hdrx_get_color_mode(),
                                 count, self._memory_size)

        return self._capture.hdrx_download_captured_frames(count, frame_type)

    def hdrx_buffered_captured_frames(self, path: str, count: int = 1, frame_type: str = 'RAW', save_to_bin=True,
                                      save_to_bmp=False, save_to_ppm=False):
        """

        Capturing and saving frames to files.
        Available extensions for files: bin, bmp, ppm.

        Parameters
        ----------
        path : str
            Path to save captured frames
        count : int
            Number of frames to download
        frame_type : str
            'RGB', 'RAW' or 'Native'
        save_to_bin : bool
            Flag for saving to bin file
        save_to_bmp : bool
            Flag for saving to bmp file
        save_to_ppm : bool
            Flag for saving to ppm file
        """

        count = check_frame_size(self.hdrx_get_h_active(), self.hdrx_get_v_active(), self.hdrx_get_color_mode(),
                                 count, self._memory_size)

        self._capture.hdrx_buffered_captured_frames(path, count, frame_type, save_to_bin, save_to_bmp, save_to_ppm)

    def hdrx_start_capture_frames(self, count):
        """

        A sample usecase of frame capture.
        Captures a number of video frames along with their MSA and SDP.

        Parameters
        ----------
        count : int
            Number of frames to be captured
        """
        count = check_frame_size(self.hdrx_get_h_active(), self.hdrx_get_v_active(), self.hdrx_get_color_mode(),
                                 count, self._memory_size)

        self._capture.hdrx_start_capture_frames(count)

    def hdrx_stop_capture_frames(self):
        """

        Stop capture frames.

        """

        self._capture.hdrx_stop_capture_frames()

    def hdrx_download_captured_events(self, save_to_bin=True, save_to_txt=False, path_to_save="") -> list:
        """

        Download all captured events to current moment.

        Parameters
        ----------
        save_to_bin : bool
            Flag for saving captured events to bin files
        save_to_txt : bool
            Flag for saving captured events to txt files
        path_to_save : str
            Path to save all events

        Returns
        -------
        result : list
            Value (list) with captured events.

        """
        return self._capture.hdrx_download_captured_events(save_to_bin, save_to_txt, path_to_save)

    def hdrx_capture_events_selected_packets(self, list_packets: tuple, time_for_capture: int = 1, save_to_bin=True,
                                             save_to_txt=False, path_to_save=""):
        """

        Starts capturing all selected packets.

        Parameters
        ----------
        list_packets : tuple
            Selected packets
        time_for_capture : int
            How long time to capture events
        save_to_bin : bool
            Flag for saving captured events to bin files
        save_to_txt : bool
            Flag for saving captured events to txt files
        path_to_save : str
            Path to save all events

        Returns
        -------
        result : list
            Value (List) of captured events. Each event is a tuple.
            (result, timestamp, typeStr, briefStr, contentStr, eventSourceStr, data)

        """

        return self._capture.hdrx_capture_events_selected_packets(list_packets, time_for_capture, save_to_bin,
                                                                   save_to_txt, path_to_save)

    # Pattern Generator Block
    def hdrx_get_h_total(self) -> int:
        """

        Return data of HTotal resolution.

        Returns
        -------
        result : int
            HTotal resolution
        """
        return self._pg.hdrx_get_h_total()

    def hdrx_get_v_total(self) -> int:
        """

        Return data of VTotal resolution.

        Returns
        -------
        result : int
            VTotal resolution
        """
        return self._pg.hdrx_get_v_total()

    def hdrx_get_resolution_total(self) -> tuple:
        """

        Return data of HTotal and VTotal (Total) resolution.

        Returns
        -------
        result : tuple
            Total resolution
        """
        return self._pg.hdrx_get_resolution_total()

    def hdrx_get_h_active(self) -> int:
        """

        Return data of HActive resolution.

        Returns
        -------
        result : int
            HActive resolution
        """
        return self._pg.hdrx_get_h_active()

    def hdrx_get_v_active(self) -> int:
        """

        Return data of VActive resolution.

        Returns
        -------
        result : int
            VActive resolution
        """
        return self._pg.hdrx_get_v_active()

    def hdrx_get_resolution_active(self) -> tuple:
        """

        Return data of HActive and VActive resolution.

        Returns
        -------
        result : tuple
            Active resolution
        """
        return self._pg.hdrx_get_resolution_active()

    def hdrx_get_h_sync(self) -> int:
        """

        Return data of HSync resolution.

        Returns
        -------
        result : int
            HSync resolution
        """
        return self._pg.hdrx_get_h_sync()

    def hdrx_get_v_sync(self) -> int:
        """

        Return data of VSync resolution.

        Returns
        -------
        result : int
            VSync resolution
        """
        return self._pg.hdrx_get_v_sync()

    def hdrx_get_resolution_sync(self) -> tuple:
        """

        Return data of HSync and VSync resolution.

        Returns
        -------
        result : tuple
            Sync resolution
        """
        return self._pg.hdrx_get_resolution_sync()

    def hdrx_get_h_start(self) -> int:
        """

        Return data of HStart resolution.

        Returns
        -------
        result : int
            HStart resolution
        """
        return self._pg.hdrx_get_h_start()

    def hdrx_get_v_start(self) -> int:
        """

        Return data of VStart resolution.

        Returns
        -------
        result : int
            VStart resolution
        """
        return self._pg.hdrx_get_v_start()

    def hdrx_get_resolution_start(self) -> tuple:
        """

        Return data of HStart and VStart resolution.

        Returns
        -------
        result : tuple
            Start resolution
        """
        return self._pg.hdrx_get_resolution_start()

    def hdrx_get_frame_rate(self) -> float:
        """

        Return data of current frame rate.

        Returns
        -------
        result : float
            Frame rate

        """
        return self._pg.hdrx_get_frame_rate()

    def hdrx_get_color_depth(self) -> int:
        """

        Return data of current color depth, bits per pixel (BPP).

        Returns
        -------
        result : int
            Color depth

        """
        return self._pg.hdrx_get_color_depth()

    def hdrx_get_bpc(self) -> int:
        """

        Return data of current color depth, bits per component (BPC).

        Returns
        -------
        result : int
            Color depth

        """
        return self._pg.hdrx_get_bpc()

    def hdrx_get_color_mode(self) -> int:
        """

        Return data of current color mode.

        Returns
        -------
        result : int
            Color mode

        """
        return self._pg.hdrx_get_color_mode()

    def hdrx_get_colorimetry(self) -> int:
        """

        Return data of current colorimetry.

        Returns
        -------
        result : int
            Colorimetry

        """
        return self._pg.hdrx_get_colorimetry()

    def hdrx_set_tim_command(self, value=1):
        """

        Update video timing info. Need to call before reading PG info.

        Returns
        -------
        result : int
            Command for updating (default = 1).

        """

        self._pg.hdrx_set_tim_command(value)

    def hdrx_pg_get_all_info(self) -> list:
        """

        Return all Pattern Generator information.

        Returns
        -------
        result : list
            PG info

        """
        return self._pg.hdrx_pg_get_all_info()

    def hdrx_calculate_pixel_clock(self) -> float:
        """

        Calculate and return Pixel Clock.

        Returns
        -------
        result : float
            Pixel clock

        """

        return self._pg.hdrx_calculate_pixel_clock()

    def hdrx_calculate_tmds_clock(self) -> float:
        """

        Calculate and return TMDS Clock.

        Returns
        -------
        result : float
            TMDS clock

        """

        return self._pg.hdrx_calculate_tmds_clock()

    # InfoFrame Block
    def hdrx_get_info_frame(self) -> str:
        """

        Return HDMI frame information.

        Returns
        -------
        result : str
            Frame info

        """
        return self._sdp.hdrx_get_info_frame()
