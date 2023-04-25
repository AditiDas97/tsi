from .tsi_tx import *
from .modules.SCDC.scdc_tx import *
from .modules.Link.LinkHDMI.link_hdtx import *
from .modules.Capture.capture_hdtx import *


class HDTX(TX):

    def __init__(self, device: TSIDevice):
        """

        General class for HDMI device TX(source) side. Inherited from class TX.

        The class contains the following fields:
        link - Object of LinkTx class. Contain some control link device methods.
        scdc - Object of ScdcTx class. Needed for reading, writing, saving and loading SCDC information.
        capturer - Object of CapturerHdRx class. Needed to capture, downloading and saving events and video frames.

        Parameters
        ----------
        device : TSIDevice
            Indicates the device on which the operation is to be carried out
        """

        index = -1
        dev_type = "HD"
        role = "TX"
        for item in device.get_ports_and_roles():
            if item[0] == "HD" and item[1] == "TX":
                index = item[2]
        if index == -1:
            raise AssertionError("Selected incorrect device: Incorrect device type or role")
        port_id = 0 if (len(device.get_ports_and_roles()) < 2) else index
        super().__init__(device)
        self.open_port(port_id, role, dev_type)
        self.read_info_from_device(self, port_id)
        self._scdc = ScdcTx(device)
        self._link = LinkTx(device)
        self._capture = CapturerHdTx(device)

    def hdtx_get_link_status_all_info(self) -> LinkStatusHdtx:
        """

        Return the object of LinkStatusHdtx class. It contains information about device link status.

        Available info:
            linkMode - info of HDMO link mode (type: int)
            videoEnabled - current state of video: enabled/disabled (type: bool)
            supportedScrambler - current state of Scrambler: supported/unsupported (type: bool)
            supportedSCDC - current state of SCDC: supported/unsupported (type: bool)
            scrambler - current state of Scrambler: enabled/disabled (type: bool)
            clockRate - info of clock rate mode (type: int)
            hpd_status - current state of HPD: asserted/de-asserted (type: bool)
            linkModeFRL - info of FRL link mode (type: int)

        Returns
        -------
        result : LinkStatusHdtx
            Link status HdTx data
        """
        link_status = LinkStatusHdtx()

        status = self.hdtx_get_status_r()
        link_status.linkMode = 1 if (status & 1) != 0 else 0
        link_status.videoEnabled = (status & 2) != 0

        sink_caps = self.hdtx_get_sink_caps()
        link_status.supportedScrambler = (sink_caps & 2) != 0
        link_status.supportedSCDC = (sink_caps & 1) != 0

        sink_status = self.hdtx_get_sink_status()
        link_status.scrambler = (sink_status & 1) != 0
        link_status.clockRate = 1 if (sink_status & 2) != 0 else 0

        link_status.hpd_status = (self.hdtx_get_hpd_status() & 1) != 0
        link_status.linkModeFRL = (self.hdtx_get_frl_status() & 0xF)

        return link_status

    # Link Block
    def hdtx_set_behavior(self, behavior: int):
        """

        Set HDMI behavior.

        Parameters
        ----------
        behavior : int
            1 - HDMI 1.4 Behavior
            2 - HDMI 2.1 Behavior

        """
        self._link.hdtx_set_behavior(behavior)

    def hdtx_get_behavior(self) -> int:
        """

        Return HDMI behavior.

        Returns
        -------
        result : int
            0 - HDMI 2.0 Behavior
            1 - HDMI 1.4 Behavior
            2 - HDMI 2.1 Behavior

        """

        return self._link.hdtx_get_behavior()

    def hdtx_set_mode(self, mode: int):
        """

        Set HDMI mode.

        Parameters
        ----------
        mode : int
            0 - HDMI
            1 - DVI

        """
        self._link.hdtx_set_mode(mode)

    def hdtx_get_mode(self) -> int:
        """

        Get HDMI mode.

        Returns
        ----------
        result : int
            0 - HDMI
            1 - DVI

        """

        return self._link.hdtx_get_mode()

    def hdtx_get_video_enable(self) -> bool:
        """

        Return current video state.

        Returns
        -------
        result : bool
            True - enabled
            False - disabled
        """

        return self._link.hdtx_get_video_enable()

    def hdtx_get_hpd_status(self) -> bool:
        """

        Return current HPD status.

        Returns
        -------
        result : bool
            True - HPD is asserted
            False - HPD is de-asserted.
        """
        return self._link.hdtx_get_hpd_status()

    def hdtx_get_lanes_error_counters(self) -> tuple:
        """

        Return current hdmi lanes error counters.

        Returns
        -------
        result : tuple
            Error counters

        """

        return self._link.hdtx_get_lanes_error_counters()

    # Link Block: TMDS
    def hdtx_get_status_r(self) -> int:
        """

        Return HDTX Transmitter status.

        Returns
        -------
        result : int
            Transmitter status
        """

        return self._link.tmds.hdtx_get_status_r()

    def hdtx_get_sink_caps(self) -> int:
        """

        Return HDTX Sink device capabilities.

        Returns
        -------
        result : int
            Capabilities
        """
        return self._link.tmds.hdtx_get_sink_caps()

    def hdtx_get_supported_scrambler(self) -> bool:
        """

        Return state of scrambler.

        Returns
        -------
        result : bool
            True - supported
            False - not supported

        """

        return self._link.tmds.hdtx_get_supported_scrambler()

    def hdtx_get_supported_scdc(self) -> bool:
        """

        Return state of SCDC.

        Returns
        -------
        result : bool
            True - supported
            False - not supported

        """

        return self._link.tmds.hdtx_get_supported_scdc()

    def hdtx_get_sink_status(self) -> int:
        """

        Check and return state of Sink’s features.

        Returns
        -------
        result : int
            State
        """
        return self._link.tmds.hdtx_get_sink_status()

    def hdtx_get_scrambler(self) -> bool:
        """

        Return current state of Scrambler.

        Returns
        -------
        result : bool
            True - enabled
            False - disabled

        """

        return self._link.tmds.hdtx_get_scrambler()

    def hdtx_get_clock_rate(self) -> int:
        """

        Return current clock rate mode.

        Returns
        -------
        result : int
            0 - 3G mode
            1 - 6G mode

        """

        return self._link.tmds.hdtx_get_clock_rate()

    # SCDC Block
    def hdtx_write_scdc(self, base: int, count: int, data: bytearray) -> int:
        """

        Write data to SCDC register.

        Parameters
        ----------
            base : int
                Start address of SCDC register
            count : int
                Number of registers to write
            data : bytearray
                data to be written into SCDC register

        Returns
        -------
        result : int
             Return a result of operation

        """

        return self._scdc.write_scdc(base, count, data)

    def hdtx_read_scdc(self, base: int, count: int) -> bytearray:
        """

        Read data from SCDC register.

        Parameters
        ----------
            base : int
                Start address of SCDC register
            count : int
                Number of registers being read (Each SCDC register is one byte (8 bits))

        Returns
        -------
        result : bytearray
            array of SCDC data

        """
        return self._scdc.read_scdc(base, count)

    def hdtx_save_scdc(self, base_address_range_1: int, size_range_1: int, data_range_1: bytearray,
                       base_address_range_2=0, size_range_2=0, data_range_2=bytearray(), path=""):
        """

        Saving SCDC block(s) from device.

        Parameters
        ----------
        base_address_range_1 : int
            Base address of SCDC data
        size_range_1 : int
            Size of SCDC data
        data_range_1 : bytearray
            SCDC date
        base_address_range_2 : int
            Base address of SCDC data
        size_range_2 : int
            Size of SCDC data
        data_range_2 : bytearray
            SCDC date
        path : str
            Path to save files.


        """

        self._scdc.save_scdc(base_address_range_1, size_range_1, data_range_1, base_address_range_2, size_range_2,
                              data_range_2, path)

    def hdtx_load_scdc(self, path: str) -> list:
        """

        Loading, parse and return SCDC data from file.

        Parameters
        ----------
        path : str
            Path to input SCDC file.

        Returns
        -------
        result : list
            Return SCDC data from file.

        """

        return self._scdc.load_scdc(path)

    # Get FRL Status
    def hdtx_get_frl_status(self) -> int:
        """

        Return current FRL status

        Returns
        -------
        result : int
            FRL status.
        """
        return self._link.frl_status.hdtx_get_frl_status()

    # Capture block
    def hdtx_start_event_capture(self, event_types: tuple):
        """

        Starts capturing events.

        Parameters
        ----------
        event_types : tuple
            list of one or more of the following values:
                'HPD': hpd events
                'CEC': 'CEC' events
                'I2C': I2C packets
        """
        self._capture.hdtx_start_event_capture(event_types)

    def hdtx_stop_event_capture(self):
        """

        Stop event capture.

        """
        self._capture.hdtx_stop_event_capture()

    def hdtx_download_captured_events(self, save_to_bin=True, save_to_txt=False, path_to_save="") -> list:
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
        return self._capture.hdtx_download_captured_events(save_to_bin, save_to_txt, path_to_save)

    def hdtx_capture_events_selected_packets(self, list_packets: tuple, time_for_capture=1, save_to_bin=True,
                                             save_to_txt=False, path_to_save="") -> list:
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

        return self._capture.hdtx_capture_events_selected_packets(list_packets, time_for_capture, save_to_bin,
                                                                   save_to_txt, path_to_save)
