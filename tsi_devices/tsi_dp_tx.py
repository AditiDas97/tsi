from .tsi_tx import *
from .modules.DPCD.dpcd_tx import *
from .modules.Link.LinkDP.link_dptx import *
from .modules.Capture.capture_dptx import *


class DPTX(TX):

    def __init__(self, device: TSIDevice):
        """

        General class for DP device TX(source) side. Inherited from class TX.

        The class contains the following fields:
        dpcd - Object of DpcdTx class. Needed for reading, writing, saving and loading DPCD information.
        link - Object of LinkTx class. Contain some control link device methods.
        capturer - Object of CapturerDpTx class. Needed to capture, downloading and saving events and video frames.

        Parameters
        ----------
        device : TSIDevice
            Indicates the device on which the operation is to be carried out
        """

        index = -1
        dev_type = "DP"
        role = "TX"
        type_c = str(self.__class__.__name__).find("USBC") != -1
        if type_c:
            dev_type = "USBC"
            for item in device.get_ports_and_roles():
                if item[0] == "USBC" and item[1] == "TX":
                    index = item[2]
        else:
            for item in device.get_ports_and_roles():
                if item[0] == "DP" and item[1] == "TX":
                    index = item[2]
        if index == -1:
            raise AssertionError("Selected incorrect device: Incorrect device type or role")
        port_id = 0 if (len(device.get_ports_and_roles()) < 2) else index
        super().__init__(device)
        self.open_port(port_id, role, dev_type)
        self.read_info_from_device(self, port_id)
        self._dpcd = DpcdTx(device)
        self._link = LinkTx(device)
        self._capture = CapturerDpTx(device)

    # Link Block
    def dptx_get_link_status_all_info(self) -> LinkStatusDptx:
        """

        Return the object of LinkStatusDptx class. It contains information about device link status.

        Available info:
            assertedHPD - flag of asserted HPD (type : bool)
            sscEnabled - flag of SSC enable (type : bool)
            sscSupported - flag of SSC support (type : bool)
            dscEnabled - flag of DSC enable (type : bool)
            dscSupported - flag of DSC support (type : bool)
            lanesCount - count of lanes (type : int)
            linkRate - count of link rate (type : float)
            interlaneAlignStatus - state of inter lane align status (type: bool)
            framing - type of framing: 'Enhanced' or 'Normal' (type : str)
            multiStream - flag of multistream status(type : bool)
            linkPattern - if of link pattern(type : int)
            lanes - information about each lane (type : list):
                clock_recovery (type : bool)
                channel_equalization (type : bool)
                symbol_link (type : bool)
                voltage_swing (type : int)
                pre_emphasis (type : int)

        Returns
        -------
        result : LinkStatusDptx
            Link status DpTx data

        """
        link_status = LinkStatusDptx()
        link_status.linkPattern = self.dptx_get_dp_link_pattern()
        link_status.assertedHPD = self.dptx_get_hpd_status()
        link_status.lanesCount = self.dptx_get_link_status_lane_count()
        rate = self.dptx_get_link_status_bit_rate()
        link_status.linkRate = '{:.3f}'.format(rate) + ' Gbps'
        link_status.framing = "Enhanced" if self.dptx_get_enhanced_framing() != 0 else \
            "Normal"
        link_status.multiStream = None  # TSI_VR_DPTX_MST_STATUS

        current_link_status = self.dptx_get_link_status_bits()

        for i in range(4):
            link_status.lanes[i].clock_recovery = (((current_link_status >> (0 + 4 * i)) & 1) != 0)
            link_status.lanes[i].channel_equalization = (((current_link_status >> (1 + 4 * i)) & 1) != 0)
            link_status.lanes[i].symbol_link = (((current_link_status >> (2 + 4 * i)) & 1) != 0)

        current_swing = self.dptx_get_link_status_volt_swing()
        current_pre_emp = self.dptx_get_link_status_pre_emp()
        for i in range(4):
            link_status.lanes[i].voltage_swing = str(((current_swing >> (8 * i)) & 3))
            link_status.lanes[i].pre_emphasis = str(((current_pre_emp >> (8 * i)) & 3))

        dsc_status = self.dptx_get_dsc_status()
        link_status.dscEnabled = (dsc_status & 0x1)
        link_status.dscSupported = ((dsc_status >> 1) & 0x1)

        ssc_status = self.dptx_get_downspread_status()
        link_status.sscEnabled = ssc_status & 0x1
        link_status.sscSupported = (ssc_status >> 1) & 0x1

        return link_status

    def link_training(self):
        """

        Make a link training.

        """
        self._link.link_configuration.link_training()

    def dptx_set_command(self, value):
        """

        Carry out commands on the source.

        List of commands:
            0 - No operation. Writing this has no effect.
            1 - Begin link-training.
            2 - Apply bit-rate and lane count settings without performing link-training.
            3 - Enable MST mode
            4 - Disable MST mode

        Parameters
        ----------
        value : int
            Command ID.
        """
        self._link.link_configuration.dptx_set_command(value)

    # DPCD Block
    def dptx_write_dpcd(self, base: int, count: int, data: bytearray) -> int:
        """

        Write data to dpcd register.

        Parameters
        ----------
        base : int
            Start address of DPCD register
        count : int
            Number of registers to write
        data : bytearray
            data to be written into DPCD register

        Returns
        -------
        result : int
             Return a result of operation

        """

        return self._dpcd.write_dpcd(base, count, data)

    def dptx_read_dpcd(self, base: int, count: int) -> bytearray:
        """

        Read data from DPCD register.

        Parameters
        ----------
        base : int
            Start address of DPCD register
        count : int
            Number of registers being read (Each DPCD register is one byte (8 bits))

        Returns
        -------
        list : bytearray
            list of DPCD data

        """

        return self._dpcd.read_dpcd(base, count)

    def dptx_load_dpcd(self, path: str) -> list:
        """

        Loading, parse and return DPCD data from file.

        Parameters
        ----------
        path : str
            Path to input dpcd file.

        Returns
        -------
        result : list
            Return EDID data from file.

        """
        return self._dpcd.load_dpcd(path)

    def dptx_save_dpcd(self, base_address_range_1: int, size_range_1: int, data_range_1: bytearray,
                       base_address_range_2: int, size_range_2: int, data_range_2: bytearray, path: str):
        """

        Saving DPCD block(s) from device.

        Parameters
        ----------
        base_address_range_1 : int
            Base address of DPCD data
        size_range_1 : int
            Size of DPCD data
        data_range_1 : int
            DPCD date
        base_address_range_2 : int
            Base address of DPCD data
        size_range_2 : int
            Size of DPCD data
        data_range_2 : int
            DPCD date
        path : str
            Path to save files.

        """
        self._dpcd.save_dpcd(base_address_range_1, size_range_1, data_range_1, base_address_range_2, size_range_2,
                              data_range_2, path)

    # Link Block: Link Overrides
    def dptx_set_pre_emphasis(self, pre_emp: int):
        """

        Writing this CI will override the pre emphasis values.

        Parameters
        ----------
        pre_emp : int
            0 = 0 dB pre-emphasis
            1 = 3.5 dB pre-emphasis
            2 = 6 dB pre-emphasis
            3 = 9.5 dB pre-emphasis
        """

        self._link.link_status.dptx_set_pre_emphasis(pre_emp)

    def dptx_get_pre_emphasis(self) -> int:
        """

        Reading the info from device will return the previous values written.

        Returns
        -------
        result : int
            0 = 0 dB pre-emphasis
            1 = 3.5 dB pre-emphasis
            2 = 6 dB pre-emphasis
            3 = 9.5 dB pre-emphasis
        """

        return self._link.link_status.dptx_get_pre_emphasis()

    def dptx_set_voltage(self, voltage: int):
        """

        Writing this info will override the voltage swing values.

        Parameters
        ----------
        voltage : int
            0 = 400 mVpp
            1 = 600 mVpp
            2 = 800 mVpp
            3 = 1200 mVpp
        """

        self._link.link_status.dptx_set_voltage(voltage)

    def dptx_get_voltage(self) -> int:
        """

        If no override values have been written reading the info will fail.

        Returns
        -------
        result : int
            0 = 400 mVpp
            1 = 600 mVpp
            2 = 800 mVpp
            3 = 1200 mVpp
        """

        return self._link.link_status.dptx_get_voltage()

    def dptx_get_dsc_status(self) -> int:
        """

        Return full DSC status:
        0 bit -	0 DSC disabled, 1 DSC enabled.
        1 bit - 0 DSC not supported, 1 DSC supported.

        Returns
        -------
        result : int
            DSC info
        """

        return self._link.link_status.dptx_get_dsc_status()

    def dptx_get_hw_caps(self) -> int:
        """

        Return DPTX HW capability information.

        Returns
        -------
        result : int
            HW capabilities info
        """

        return self._link.dptx_get_hw_caps()

    def dptx_get_crc_values(self) -> dict:
        """

        Read red, green and blue CRC values for current input video stream.

        Returns
        -------
        result : dict
            Function returns status of TSI operations
            dict:
                crc_red : int
                    CRC value for red component 0 - 63365
                crc_green : int
                    CRC value for green component 0 - 63365
                crc_blue : int
                    CRC value for blue component 0 - 63365
        """

        return self._link.dptx_get_crc_values()

    def dptx_set_dp_link_pattern(self, value: int):
        """

        Force device to output a pattern that is typically used only with Link Training.

        Parameters
        ----------
        value : int
            0 = Active video, 1 = Idle pattern, 2 = Training pattern 1, 3 = Training pattern 2,
            4 = Training pattern 3, 5 = Training pattern 4, 6 = PRBS7, 7 = HBR2, 8 = SER

        """
        self._link.link_status.dptx_set_dp_link_pattern(value)

    def dptx_get_dp_link_pattern(self) -> int:
        """

        Return a pattern that is typically used only with Link Training.

        Returns
        -------
        result : int
            0 = Active video, 1 = Idle pattern, 2 = Training pattern 1, 3 = Training pattern 2, 4 = Training pattern 3,
            5 = Training pattern 4, 6 = PRBS7, 7 = HBR2, 8 = SER
        """

        return self._link.link_status.dptx_get_dp_link_pattern()

    def dptx_get_hpd_status(self) -> bool:
        """

        Return HPD signal logical status.

        Returns
        -------
        result : bool
            False - HPD de-asserted, True - HPD asserted
        """

        return bool(self._link.dptx_get_hpd_status())

    def dptx_get_link_status_lane_count(self) -> int:
        """

        Return number of lanes achieved in the previous link training.

        Returns
        -------
        result : int
            Number of lanes
        """

        return self._link.link_status.dptx_get_link_status_lane_count()

    def dptx_get_link_status_bit_rate(self) -> float:
        """

        Return link bit-rate achieved during the previous link training as multiple of 0.27Gbps.

        Returns
        -------
        result : float
            Link bit-rate

        """

        return self._link.link_status.dptx_get_link_status_bit_rate() * 0.27

    def dptx_get_link_status_bits(self) -> int:
        """

        Return Clock Recovery, Channel equalization and symbol locks states for each lane.
        The status is the result of the previous link training.

        Bits
        0  - Clock Recovery done for Lane 0.
        1  - Channel EQ done for Lane 0.
        2  - Symbol lock for Lane 0.
        4  - Clock Recovery done for Lane 1.
        5  - Channel EQ done for Lane 1.
        6  - Symbol lock for Lane 1.
        8  - Clock Recovery done for Lane 2.
        9  - Channel EQ done for Lane 2.
        10 - Symbol lock for Lane 2.
        12 - Clock Recovery done for Lane 3.
        13 - Channel EQ done for Lane 3.
        14 - Symbol lock for Lane 3.
        29 - MST Support flag (1 = MST Supported).
        30 - MST / SST Status (1 = MST, 0 = SST).
        31 - ILA info.

        Returns
        -------
        result : int
            Link status bits status

        """

        return self._link.link_status.dptx_get_link_status_bits()

    def dptx_get_link_status_volt_swing(self) -> int:
        """

        Return voltage swing values for each lane. The state is the result of the previous link training.

        Bits (for each lane in byte: 1 byte - 0 lane, 2 byte - 1 lane and so on.)
        0 - 400 mVpp
        1 - 600 mVpp
        2 - 800 mVpp
        3 - 1200 mVpp

        Returns
        -------
        result : int
            Voltage swing value

        """

        return self._link.link_status.dptx_get_link_status_volt_swing()

    def dptx_get_link_status_pre_emp(self) -> int:
        """

        Return the pre-emphasis setting achieved during the previous link training.

        Bits (for each lane in byte: 1 byte - 0 lane, 2 byte - 1 lane and so on.)
        0 = 0 dB pre-emphasis
            1 = 3.5 dB pre-emphasis
            2 = 6 dB pre-emphasis
            3 = 9.5 dB pre-emphasis

        Returns
        -------
        result : int
            Pre-emphasis value

        """

        return self._link.link_status.dptx_get_link_status_pre_emp()

    # Link Block: Link Configuration
    def dptx_get_link_setup_all_info(self) -> LinkSetupDpTx:
        """

        Return the object of LinkSetupDpTx class. It contains information about device link setup.

        Available info:
            maxSupportedLinkRate - count of maximum supported link rate (type : int)
            lanesCount - count of lanes (type : int)
            linkRate - count of link rate (type : int)
            enhancedFraming - type of framing selection (type : int)

        Returns
        -------
        result : LinkSetupDpTx
            Link setup value

        """
        link_setup = LinkSetupDpTx()

        link_setup.maxSupportedLinkRate = (self.dptx_get_hw_caps() >> 16) & 0xFF
        if link_setup.maxSupportedLinkRate == 0:
            link_setup.maxSupportedLinkRate = 20
        link_setup.lanesCount = self.dptx_get_link_cfg_lanes()
        link_setup.linkRate = self.dptx_get_link_cfg_bit_rate()
        link_setup.enhancedFraming = self.dptx_get_enhanced_framing()

        return link_setup

    def dptx_set_link_cfg_lanes(self, value):
        """

        Set the number lanes to be used on the DisplayPort link.
        The configured value is used the next time there is a link training,
        or when the command to apply setting without LT is issued.

        Parameters
        ----------
        value : int
            Valid settings are 1, 2 and 4 lanes.

        """
        self._link.link_configuration.dptx_set_link_cfg_lanes(value)

    def dptx_get_link_cfg_lanes(self) -> int:
        """

        Return the number lanes to be used on the DisplayPort link.

        Returns
        -------
        result : int
            Valid value are 1, 2 and 4.
        """

        return self._link.link_configuration.dptx_get_link_cfg_lanes()

    def dptx_set_link_cfg_bit_rate(self, value=1.62):
        """

        Defines the bit rate as multiplier of 0.27Gbps. The configured value is used the next
        time there is a link training, or when the command to apply setting without LT is issued.

        Parameters
        ----------
        value : float
             Valid settings are 6, 10 and 20.

        """
        self._link.link_configuration.dptx_set_link_cfg_bit_rate(value)

    def dptx_get_link_cfg_bit_rate(self) -> int:
        """

        Return the bit rate.

        Returns
        -------
        result : int
            Valid value are 6, 10 and 20.
        """

        return self._link.link_configuration.dptx_get_link_cfg_bit_rate()

    def dptx_get_downspread_status(self) -> int:
        """

        Return downspread status:
            0 bit -	0 Down-spread is disabled, 1 Down-spread is enabled.
            1 bit - 0 SSC not supported, 1 SSC supported

        Returns
        -------
        result : int
            Value of downspread status
        """

        return self._link.link_configuration.dptx_get_downspread_status()

    def dptx_set_enhanced_framing(self, value: int):
        """

        Set type of framing selection:
            0 - Standard framing
            1 -  Enhanced framing

        Parameters
        ----------
        value : int
             Framing type.
        """

        self._link.link_configuration.dptx_set_enhanced_framing(value)

    def dptx_get_enhanced_framing(self) -> int:
        """
        Return  type of framing selection:
            0 - Standard framing
            1 -  Enhanced framing

        Returns
        -------
        result : int
            Value of downspread status
        """

        return self._link.link_configuration.dptx_get_enhanced_framing()

    # Capture block
    def dptx_start_event_capture(self, event_types: tuple):
        """

        Starts capturing events.

        Parameters
        ----------
        event_types: tuple
            list of one or more of the following values:
                'AUX': AUX transaction or signal
                'HPD': hpd events
        """

        self._capture.dptx_start_event_capture(event_types)

    def dptx_stop_event_capture(self):
        """

        Stops capture and downloads all captured events.

        """

        self._capture.dptx_stop_event_capture()

    def dptx_download_captured_events(self, save_to_bin=True, save_to_txt=False, path_to_save="") -> list:
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

        return self._capture.dptx_download_captured_events(save_to_bin, save_to_txt, path_to_save)

    def dptx_capture_events_selected_packets(self, list_packets: tuple, time_for_capture=1, save_to_bin=True,
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

        return self._capture.dptx_capture_events_selected_packets(list_packets, time_for_capture, save_to_bin,
                                                                   save_to_txt, path_to_save)
