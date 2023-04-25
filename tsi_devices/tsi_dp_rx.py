from .tsi_rx import *
from .modules.DPCD.dpcd_rx import *
from .modules.PatternGenerator.PGDPRX import *
from .modules.Link.LinkDP.link_dprx import *
from .modules.SDP.sdp_dprx import *
from .modules.Capture.capture_dprx import *


class DPRX(RX):

    def __init__(self, device: TSIDevice):
        """

        General class for DP device RX(sink) side. Inherited from class RX.

        The class contains the following fields:
        dpcd - Object of DpcdRx class. Needed for reading, writing, saving and loading DPCD information.
        pg - Object of PatternGeneratorDpRx class. Allow to get some video information (video resolution, bpc,
        colorimetry, color mode and so on)
        link - Object of LinkRx class. Contain some control link device methods.
        sdp - Object of SdpDpRx class. Allow getting SDP frames.
        capturer - Object of CapturerDpRx class. Needed to capture, downloading and saving events and video frames.

        Parameters
        ----------
        device : TSIDevice
            Indicates the device on which the operation is to be carried out
        """

        index = -1
        dev_type = "DP"
        role = "RX"
        type_c = str(self.__class__.__name__).find("USBC") != -1
        if type_c:
            dev_type = "USBC"
            for item in device.get_ports_and_roles():
                if item[0] == "USBC" and item[1] == "RX":
                    index = item[2]
        else:
            for item in device.get_ports_and_roles():
                if item[0] == "DP" and item[1] == "RX":
                    index = item[2]
        if index == -1:
            raise AssertionError("Selected incorrect device: Incorrect device type or role")
        port_id = 0 if (len(device.get_ports_and_roles()) < 2) else index
        super().__init__(device)
        self.open_port(port_id, role, dev_type)
        self._dpcd = DpcdRx(device)
        self._pg = PatternGeneratorDpRx(device)
        self._link = LinkRx(device)
        self._sdp = SdpDpRx(device)
        self._capturer = CapturerDpRx(device)
        self.read_info_from_device(self, port_id)

    def __del__(self):
        pass

    # Link Block: Link Status
    def dprx_get_link_status_all_info(self) -> LinkStatusDprx:
        """

        Return the object of LinkStatusDprx class. It contains information about device link status.
        
        Available info:
            lanesCount - count of lanes in device (type : int)
            lanes - information about each lane (type: list). Contain following info for each lane (type: LaneStatus):
                clock_recovery (type: bool)
                channel_equalization (type: bool)
                symbol_link (type: bool)
                voltage_swing (type: int)
                pre_emphasis (type: int)
                errorCount (type: int)
                ffe_preset (type: int)
            interlaneAlignStatus - state of inter lane align status (type: bool)
            linkRate - link rate on device (type: str)
            framing - state of framing: Enhanced/Normal (type: str)
            scrambling - state of scrambling: Enabled/Disabled (type: str)
            asserted (type: bool)
            fail128_132_LT - state of 128/132 LT (type: bool)
            CDS_ILA - state of CDS_ILA (type: bool)
            EQ_ILA - state of EQ_ILA (type: bool)
            isDp2LinkMode - DP 2.0 Link mode active (type: bool)
            multiStream - state of multi stream (type: bool)
            cableStatus - state of cable status (type: bool)
            hpdRawStatus - state of hpd raw status (type: bool)
            eDpBitRate - value of eDp bit rate (type: str)
            enabledSSC - state of enabledSSC (type: bool)
            supportedSSC - state of supportedSSC (type: bool)
            initial - information about initial state (type: InitialLinkStatus). Contain following fields:
                linkTraining - state of link training (type: int)
                lanesCount - count of lanes in device (type : int)
                lanes - information about each lane (type: list). See info above.
                interlaneAlignStatus - state of inter lane align status (type: bool)
                crPatternDurationUs - state of cr pattern duration us (type: int)
                eqPattern - pattern type (type: int)
                eqPatternDurationUs - state of eq pattern duration us (type: int)
                eDpBitRate - value of eDp bit rate (type: str)
                BitRateGbps - value of bit rate (type: str)

        Returns
        -------
        result : LinkStatusDprx
            Link status DpRx data

        """

        link_status = LinkStatusDprx()

        link_status.asserted = self.dprx_get_hpd_status() & 1
        link_status.cableStatus = self.dprx_get_hpd_status() & 4

        link_status.lanesCount = self.dprx_get_lane_count()
        link_status.linkRate = str(self.dprx_get_link_rate() * 0.27) + " Gbps"

        current_link_status = self.dprx_get_link_status()
        link_status.interlaneAlignStatus = (((current_link_status >> 16) & 1) != 0)
        link_status.framing = "Enhanced" if (((current_link_status >> 17) & 1) != 0) else "Normal"
        link_status.scrambling = "Enabled" if (((current_link_status >> 18) & 1) != 0) else "Disabled"
        link_status.multiStream = (((current_link_status >> 19) & 1) != 0)
        link_status.fail128_132_LT = (((current_link_status >> 28) & 1) != 0)
        link_status.CDS_ILA = (((current_link_status >> 29) & 1) != 0)
        link_status.EQ_ILA = (((current_link_status >> 30) & 1) != 0)

        initial_link_status = self.dprx_get_lt_status()
        link_status.initial.interlaneAlignStatus = (((initial_link_status >> 16) & 1) != 0)
        for ln in range(4):
            link_status.initial.lanes[ln].clock_recovery = (((initial_link_status >> (0 + 4 * ln)) & 1) != 0)
            link_status.initial.lanes[ln].channel_equalization = (((initial_link_status >> (1 + 4 * ln)) & 1) != 0)
            link_status.initial.lanes[ln].symbol_link = (((initial_link_status >> (2 + 4 * ln)) & 1) != 0)

        initial_lt_info = [0 for i in range(5)]
        initial_lt_info[0] = self.dprx_get_lt_info()
        link_status.initial.eqPattern = (initial_lt_info[0] & 0xFF)
        link_status.initial.linkTraining = LinkTrainingEnum.get(((initial_lt_info[0] >> 8) & 0xFF))
        link_status.initial.crPatternDurationUs = initial_lt_info[2]
        link_status.initial.eqPatternDurationUs = initial_lt_info[3]

        voltage_swing = self.dprx_get_lt_voltage_swing()
        for i in range(4):
            link_status.initial.lanes[i].voltage_swing = voltage_swing[i]

        pre_emphasis = self.dprx_get_lt_pre_emphasis()
        for j in range(4):
            link_status.initial.lanes[j].pre_emphasis = pre_emphasis[j]

        link_status.initial.BitRateGbps = str(self.dprx_get_lt_bit_rate() * 0.27)
        link_status.initial.lanesCount = self.dprx_get_lt_lane_count() & 0xFF
        link_status.initial.eDpBitRate = '{:.2f}'.format(self.dprx_get_edp_link())

        lt_info = self.dprx_get_iop()
        if type(lt_info) == list and len(lt_info) > 0:
            link_status.alpm.trainPattern = (lt_info[0] & 0xFF)
            link_status.alpm.sleepPattern = ((lt_info[0] >> 16) & 0xF)
            link_status.alpm.wakeupPattern = ((lt_info[0] >> 20) & 0xF)
            link_status.alpm.alpmSequenceLocation = ((lt_info[0] >> 28) & 0xF)
            link_status.alpm.crPatternDurationUs = lt_info[2]
            link_status.alpm.eqPatternDurationUs = lt_info[3]
            link_status.alpm.eieosPatternDurationUs = lt_info[4]
            link_status.alpm.alpmSequenceCounter = lt_info[5]
            link_status.alpm.bitrateGbps = ((lt_info[20 * 3 + 18]) / 1000000.0)

        for i in range(4):
            link_status.lanes[i].clock_recovery = (((current_link_status >> (0 + 4 * i)) & 1) != 0)
            link_status.lanes[i].channel_equalization = (((current_link_status >> (1 + 4 * i)) & 1) != 0)
            link_status.lanes[i].symbol_link = (((current_link_status >> (2 + 4 * i)) & 1) != 0)
            if link_status.isDp2LinkMode:
                link_status.lanes[i].voltage_swing = (self.dprx_get_swing() >> (8 * i)) & 3
                link_status.lanes[i].pre_emphasis = (self.dprx_get_pre_emphasis() >> (8 * i)) & 3

        link_status.eDpBitRate = '{:.2f}'.format(self.dprx_get_link_rate())

        error_counts = self.dprx_get_error_counts()
        for i in range(4):
            link_status.lanes[i].errorCount = error_counts[i]

        if self.__type.find("400") != -1 or self.__type.find("424") != -1:
            value = self.dprx_get_ssc_status()
            link_status.enabledSSC = value[0]
            link_status.supportedSSC = value[1]

        return link_status

    # HPD
    def dprx_set_assert_status(self, value: bool):
        """

        Set assert status.

        Parameters
        ----------
        value : bool
            State of assert status: True/False

        """

        self._link.dprx_set_assert_status(value)

    def dprx_set_hpd_pulse(self, pulse=1000000):
        """

        Set HPD pulse.

        Parameters
        ----------
        pulse : int
            Value for hpd pulse (default value = 1000000)

        """

        self._link.dprx_set_hpd_pulse(pulse)

    def dprx_set_cable_force_state(self, state: bool):
        """

        Set cable force state.

        Parameters
        ----------
        state : bool
            Cable force state: True/False

        """

        self._link.dprx_set_cable_force_state(state)

    def dprx_get_cable_force(self) -> int:
        """

        Indicates current cable force status.

        Cable status (bits 2:3):
            0 or 1 No force applied.
            2 Force cable status to un-plugged.
            3 Force cable status to plugged.
        Power status (bits 4:5):
            0 or 1 No force applied.
            2 Force power status to un-powered.
            3 Force power status to powered.

        Returns
        -------
        result : int
            Cable force state

        """

        return self._link.dprx_get_cable_force()

    def dprx_get_cable_status(self) -> int:
        """

        Indicates current cable status.

        Returns
        -------
        result : int
            Cable status

        """

        return self._link.dprx_get_cable_status()

    def dprx_get_hpd_status(self) -> int:
        """

        Indicates current HPD status.

        HPD logical status:
            0 - HPD is de-asserted.
            1 - HPD is asserted.
        HPD raw status:
            0 - HPD line level is zero.
            1 - HPD line level is one.
        Cable status:
            0 - Cable is unplugged.
            1 - Cable is plugged.

        Returns
        -------
        result : int
            HPD status

        """

        return self._link.dprx_get_hpd_status()

    def dprx_get_hw_caps(self) -> HWCapabilities:
        """

        Return hardware capabilities for device.
        HWCapabilities contain following fields:
            mst - supports MST
            hdcp1 - supports HDCP 1.x
            hdcp2 - supports HDCP 2.x
            fec - supports FEC for 8/10 link
            dsc - supports DSC for 8/10 link
            alpm - supports ALPM
            lanecount3 - support ‘3 lane’ link configuration
            edp - support eDP link rates
            mstStreamCount - Number of MST streams supported
            maxLinkRate - Maximum link rate supported
            forceLinkCongiguration - supports forced link configuration
            dpPower - can provide power on DP_PWR pin of receptacle connector
            auxSwing - supports AUX output voltage swing control
            dp2CustomRates - supports custom DP2 rates
            customRateEx - supports custom bit rates
            dp2Fec - supports FEC for 128/132 link
            dp2Dsc - supports DSC for 128/132 link
            dp2SupportRates = (value >> 32) & 0xFF

        Returns
        -------
        result : HWCapabilities
            Hardware capabilities

        """

        return self._link.dprx_get_hw_caps()

    # End HPD

    def dprx_set_msa_command(self, command: int):
        """

        Update MSA all attributes. Need to call before reading MSA data.

        Parameters
        ----------
        command : int
            Update command

        """

        self._link.link_status.dprx_set_msa_command(command)

    def dprx_get_error_counts(self) -> list:
        """

        Return error counts for each used DP Lane.

        Returns
        -------
        result : list
            Error counts

        """

        result = self._link.link_status.dprx_get_error_counts()

        errors = []
        for i in range(4):
            errors.append(result[i])

        return errors

    def dprx_clear_errors(self):
        """

        Clear errors count.

        """

        self._link.link_status.dprx_clear_errors()

    def dprx_get_iop_errors(self) -> list:
        """

        Return IOP error counters.
        Every time an IOP requirement is not satisfied the respective counter is increased.
        All counters are saturated at 0x7fff.

        Returns
        -------
        result : list
            Error counts

        """

        result = self._link.link_status.dprx_get_iop_errors()

        errors = []
        for i in range(12):
            errors.append(result[i])

        return errors

    def dprx_clear_iop_errors(self):
        """

        Clear iop errors.

        """

        self._link.link_status.dprx_clear_iop_errors()

    def dprx_get_iop(self):
        """

        Return information about recent ALPM events.
        See info in ALPMLinkStatus class.

        Returns
        -------
        result : list
            IOP information

        """

        return self._link.link_status.dprx_get_iop()

    def dprx_get_link_status(self) -> int:
        """

        Indicates current link flags as defined below (See spec)

        Returns
        -------
        result : int
            link_status data

        """
        return self._link.link_status.dprx_get_link_status()

    def dprx_get_max_stream_count(self) -> int:
        """

        Return max stream count.

        Returns
        -------
        result : int
            Stream count

        """

        return self._link.link_status.dprx_get_max_stream_count()

    def dprx_get_lt_status(self) -> int:
        """

        Link status as achieved during previous link-training. (See spec)

        Returns
        -------
        result : int
            Link Status Flags

        """

        return self._link.link_status.dprx_get_lt_status()

    def dprx_get_lt_info(self) -> int:
        """

        The function presents information about recent non ALPM Link Training

        Returns
        -------
        result : int
            Link Training info value

        """

        return self._link.link_status.dprx_get_lt_info()

    def dprx_get_lt_pre_emphasis(self) -> list:
        """

        Return last LT pre-emphasis for lane 0

        Returns
        -------
        result : int
            Return value:
                0 = 0 dB
                1 = 3.5 dB
                2 = 6 dB
                3 = 9.5 dB
        """

        return self._link.link_status.dprx_get_lt_pre_emphasis()

    def dprx_get_lt_lane_count(self):
        """

        Return last LT count of lanes was reached during recent link training.

        Returns
        -------
        result : int
            Return value: 1, 2 or 4
        """

        return self._link.link_status.dprx_get_lt_lane_count()

    def dprx_get_lt_bit_rate(self):
        """

        Return last standard (non EDP) bit rate that has been reached during recent link training.
        If eDP bit rate was reached this function will return 0.

        Returns
        -------
        result : int
            Return value: 6, 10 or 20 for DP1.4. and 1, 2 or 4 for DP2.0.
        """

        return self._link.link_status.dprx_get_lt_bit_rate()

    def dprx_get_edp_link(self):
        """

        Return current eDP bit rate, in 200 kbps units. If current bit rate is standard this function will return 0.

        Returns
        -------
        result : int
            eDP bit rate

        """
        return self._link.link_status.dprx_get_edp_link()

    def dprx_get_swing(self):
        """

        Return current voltage swing for lane 0

        Returns
        -------
        result : int
            Return value:
                0 = 400 mVpp
                1 = 600 mVpp
                2 = 800 mVpp
                3 = 1200 mVpp
        """

        return self._link.link_status.dprx_get_swing()

    def dprx_get_pre_emphasis(self):
        """

        Return current pre-emphasis for lane 0

        Returns
        -------
        result : int
            Return value:
                0	0 dB
                1	3.5 dB
                2	6 dB
                3	9.5 dB
        """

        self._link.link_status.dprx_get_pre_emphasis()

    def dprx_get_lt_voltage_swing(self) -> list:
        """

        Indicates DP link voltage swing value for all active lanes

        Returns
        -------
        result : list
            DP link voltage swing data for active lanes

        """
        return self._link.link_status.dprx_get_lt_voltage_swing()

    def dprx_get_lane_count(self) -> int:
        """

        Indicates number of currently active lanes

        Returns
        -------
        result : int
            Lane count. Possible values: 1, 2, 4

        """
        return self._link.link_status.dprx_get_lane_count()

    def dprx_get_link_rate(self) -> float:
        """

        Indicates the current link rate as multiple of 0.27Gbps as in DP1.4a Standard.
        Typical values are 6 (1.62 Gbps), 10 (2.7 Gbps), 20 (5.4 Gbps) or 30 (8.1 Gbps).
        Indicates also eDP bit rate 6.25 Gbps. In this case returned link rate value is (31250)

        Returns
        -------
        result : float
            Typical values are 6 (1.62 Gbps), 10 (2.7 Gbps), 20 (5.4 Gbps) or 30 (8.1 Gbps).

        """
        return self._link.link_status.dprx_get_link_rate()

    def dprx_get_edp_bit_rate(self):
        """

        Current standard bit rate. If current bit rate is eDP, will return 0.

        Returns
        -------
        result : int
            6, 10, 20 or 30.
        """
        return self._link.link_status.dprx_get_edp_bit_rate()

    def dprx_get_ssc_status(self) -> (bool, bool):
        """

        Returned SSC status (SSC Enabled and SSC Supported)

        Returns
        -------
        result : tuple
            SSC Enabled : bool
                SSC Enabled info
            SSC Supported : bool
                SSC Supported info
        """
        return self._link.link_status.dprx_get_ssc_status()

    def dprx_start_capture(self, config: int):
        """

        Start capture with specific configuration.

        Parameters
        ----------
        config : int
            Specific configuration for capture:
                CAP_OPTION_AUDIO = 1 - start audio capture
                CAP_OPTION_VIDEO = 1 << 1 - start video capture
                CAP_OPTION_EVENTS = 1 << 2 - start event capture
                CAP_OPTION_MODE_LIVE = 1 << 3 - live capture

        """
        self._capturer.start_capture(config)

    def dprx_stop_capture(self):
        """

        Stop capture.

        """
        self._capturer.stop_capture()

    def dprx_get_crc_values(self) -> dict:
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
        return self._link.dprx_get_crc_values()

    def dprx_get_list_crc_values(self, number: int) -> list:
        """

        Return red, green and blue CRC list values for current input video stream.

        Parameters
        ----------
        number : int
            Number of CRC values to capture

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
        return self._link.dprx_get_list_crc_values(number)

    # DPCD Block
    def dprx_write_dpcd(self, base: int, count: int, data: bytearray) -> int:
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

    def dprx_read_dpcd(self, base: int, count: int) -> bytearray:
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

    def dprx_load_dpcd(self, path: str) -> list:
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

    def dprx_save_dpcd(self, base_address_range_1: int, size_range_1: int, data_range_1: bytearray,
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

    # Pattern Generator Block
    def dprx_set_msa_stream_select(self, value: int = 0):
        """

        Used to select which MSA data block is accessed with field decoded CI’s.
        MSA Blocks are numbered starting from zero (0), up to number of available streams minus one.

        Parameters
        ----------
        value : int
             Stream count

        """

        self._pg.dprx_set_msa_stream_select(value)

    def dprx_get_msa_stream_count(self) -> int:
        """

        Return number of MSA parameter blocks received from the device on previous update command.

        Returns
        -------
        result : int
            Stream count

        """

        return self._pg.dprx_get_msa_stream_count()

    def dprx_get_frame_rate(self, stream: int = 0) -> float:
        """

        Reads current frame rate in Hz.

        Parameters
        ----------
        stream : int
            Indicates the current stream
        Returns
        -------
        frame_rate : float
            current frame rate in Hz.

        """

        return self._pg.dprx_get_frame_rate(stream)

    def dprx_get_v_total(self, stream: int = 0) -> int:
        """

        Return VTOTAL field of the MSA data block.

        Parameters
        ----------
        stream : int
            Indicates the current stream

        Returns
        -------
        result : int
            HTotal resolution
        """
        return self._pg.dprx_get_v_total(stream)

    def dprx_get_h_total(self, stream: int = 0) -> int:
        """

        Return HTOTAL field of the MSA data block.

        Parameters
        ----------
        stream : int
            Indicates the current stream

        Returns
        -------
        result : int
            HTotal resolution

        """
        return self._pg.dprx_get_h_total(stream)

    def dprx_get_resolution_total(self, stream: int = 0) -> tuple:
        """

        Return TOTAL resolution.

        Parameters
        ----------
        stream : int
            Indicates the current stream

        Returns
        -------
        result : tuple
            Total resolution

        """

        return self._pg.dprx_get_resolution_total(stream)

    def dprx_get_v_active(self, stream: int = 0) -> int:
        """

        Return VACTIVE field of the MSA data block.

        Parameters
        ----------
        stream : int
            Indicates the current stream

        Returns
        -------
        result : int
            VActive resolution

        """

        return self._pg.dprx_get_v_active(stream)

    def dprx_get_h_active(self, stream: int = 0) -> int:
        """

        Return HACTIVE field of the MSA data block.

        Parameters
        ----------
        stream : int
            Indicates the current stream

        Returns
        -------
        result : int
            HActive resolution

        """

        return self._pg.dprx_get_h_active(stream)

    def dprx_get_resolution_active(self, stream: int = 0) -> tuple:
        """

        Return ACTIVE resolution.

        Parameters
        ----------
        stream : int
            Indicates the current stream

        Returns
        -------
        result : tuple
            Active resolution

        """

        return self._pg.dprx_get_resolution_active(stream)

    def dprx_get_v_start(self, stream: int = 0) -> int:
        """

        Return VSTART field of the MSA data block.

        Parameters
        ----------
        stream : int
            Indicates the current stream

        Returns
        -------
        result : int
            VStart resolution

        """

        return self._pg.dprx_get_v_start(stream)

    def dprx_get_h_start(self, stream: int = 0) -> int:
        """

        Return HSTART field of the MSA data block.

        Parameters
        ----------
        stream : int
            Indicates the current stream

        Returns
        -------
        result : int
            HStart resolution

        """

        return self._pg.dprx_get_h_start(stream)

    def dprx_get_resolution_start(self, stream: int = 0) -> tuple:
        """

        Return Start resolution.

        Parameters
        ----------
        stream : int
            Indicates the current stream

        Returns
        -------
        result : tuple
            Start resolution

        """

        return self._pg.dprx_get_resolution_start(stream)

    def dprx_get_v_sync(self, stream: int = 0) -> int:
        """

        Return VSYNC_WIDTH field of the MSA data block.

        Parameters
        ----------
        stream : int
            Indicates the current stream

        Returns
        -------
        result : int
            VSync_width resolution

        """

        return self._pg.dprx_get_v_sync(stream)

    def dprx_get_h_sync(self, stream: int = 0) -> int:
        """

        Return MSA_HSYNC_WIDTH field of the MSA data block.

        Parameters
        ----------
        stream : int
            Indicates the current stream

        Returns
        -------
        result : int
            HSync_width resolution

        """

        return self._pg.dprx_get_h_sync(stream)

    def dprx_get_resolution_sync(self, stream: int = 0) -> tuple:
        """

        Return Sync_width resolution.

        Parameters
        ----------
        stream : int
            Indicates the current stream

        Returns
        -------
        result : tuple
            Sync_width resolution

        """

        return self._pg.dprx_get_resolution_sync(stream)

    def dprx_get_color_mode(self, stream: int = 0) -> int:
        """

        Return color mode.

        Parameters
        ----------
        stream : int
            Indicates the current stream

        Returns
        -------
        result : int
            Color mode value

        """

        return self._pg.dprx_get_color_mode(stream)

    def dprx_get_color_depth(self, stream: int = 0) -> int:
        """

        Return color depth value.

        Parameters
        ----------
        stream : int
            Indicates the current stream

        Returns
        -------
        result : int
            Color depth value

        """

        return self._pg.dprx_get_color_depth(stream)

    def dprx_get_colorimetry(self, stream: int = 0) -> int:
        """

        Return colorimetry value.

        Parameters
        ----------
        stream : int
            Indicates the current stream

        Returns
        -------
        result : int
            Colorimetry value

        """

        return self._pg.dprx_get_colorimetry(stream)

    def dprx_get_msa_port_number(self, stream: int = 0) -> int:
        """

        Return PORT_NUMBER field of the MSA data block.

        Parameters
        ----------
        stream : int
            Indicates the current stream

        Returns
        -------
        result : int
            Port number (PG)

        """

        return self._pg.dprx_get_msa_port_number(stream)

    def dprx_get_n_video(self, stream: int = 0) -> int:
        """

        Return N_VIDEO field of the MSA data block.

        Parameters
        ----------
        stream : int
            Indicates the current stream

        Returns
        -------
        result : int
            NVideo value

        """

        return self._pg.dprx_get_n_video(stream)

    def dprx_get_m_video(self, stream: int = 0) -> int:
        """

        Return M_VIDEO field of the MSA data block.

        Parameters
        ----------
        stream : int
            Indicates the current stream

        Returns
        -------
        result : int
            MVideo value

        """

        return self._pg.dprx_get_m_video(stream)

    def dprx_get_vbid(self, stream: int = 0) -> int:
        """

        Reads VBID field of the MSA data block.

        Parameters
        ----------
        stream : int
            Indicates the current stream

        Returns
        -------
        result : int
            VBid value

        """

        return self._pg.dprx_get_vbid(stream)

    def dprx_pg_get_all_info(self) -> list:
        """

        Return all Pattern Generator information.

        Returns
        -------
        result : list
            PG info

        """

        return self._pg.dprx_pg_get_all_info()

    def dprx_get_msa_data(self, stream: int) -> int:
        """

        Allows reading native MSA data as it was received from the device. All available MSA data blocks can
        be read with a single read.

        Parameters
        ----------
        stream : int
            Indicates the current stream

        Returns
        -------
        result : int
            MSA data

        """

        return self._pg.dprx_get_msa_data(stream)

    def dprx_get_misc(self, stream: int = 0) -> int:
        """

        Reads MISC field (MISC0 in bits 7:0 and MISC1 in bits 15:8) of the MSA data block.

        Parameters
        ----------
        stream : int
            Indicates the current stream

        Returns
        -------
        result : int
            MVideo value

        """

        return self._pg.dprx_get_misc(stream)

    # SDP Block
    def dprx_get_sdp_frames(self) -> str:
        """

        Return SDP parsed string.

        Returns
        -------
        result : str
            SDP string

        """

        return self._sdp.dprx_get_sdp_frames()

    # Capture events and frames Block
    def dprx_config_event_filter(self, event_types=('AUX',)) -> int:
        """

        Configure filter for events. See description 'dprx_start_event_capture' for detail of available events.

        Parameters
        ----------
        event_types : tuple
            Events

        Returns
        -------
        result : int
            Configured value

        """

        return self._capturer.dprx_config_event_filter(event_types)

    def dprx_start_event_capture(self, event_types=('AUX',)):
        """

        Starts capturing events.

        Parameters
        ----------
        event_types: tuple
            list of one or more of the following values:
                'AUX': AUX transaction or signal
                'AUX_BW': AUX transaction or signal, raw Manchester-II codes
                'HPD': hpd events
                'VBID_CHANGE': changes in VBID values
                'MSA_CHANGE': changes in MSA
                'MSA_ALL': all MSA
                'SDP': SDP
                'LINK_PAT': link patterns

        """

        self._capturer.dprx_start_event_capture(event_types)

    def dprx_stop_event_capture(self):
        """

        Stops capture and downloads all captured events.

        """

        self._capturer.dprx_stop_event_capture()

    def dprx_download_captured_frames(self, count, frame_type='RAW') -> list:
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

        count = check_frame_size(self.dprx_get_h_active(0), self.dprx_get_v_active(0), self.dprx_get_color_mode(0),
                                 count, self._memory_size)

        return self._capturer.dprx_download_captured_frames(count, frame_type)

    def dprx_buffered_captured_frames(self, path: str, count: int = 1, frame_type: str = 'RAW', save_to_bin=True,
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

        count = check_frame_size(self.dprx_get_h_active(0), self.dprx_get_v_active(0), self.dprx_get_color_mode(0),
                                 count, self._memory_size)

        self._capturer.dprx_buffered_captured_frames(path, count, frame_type, save_to_bin, save_to_bmp, save_to_ppm)

    def dprx_start_capture_frames(self, count):
        """

        A sample usecase of frame capture.
        Captures a number of video frames along with their MSA and SDP.

        Parameters
        ----------
        count : int
            Number of frames to be captured
        """

        count = check_frame_size(self.dprx_get_h_active(0), self.dprx_get_v_active(0), self.dprx_get_color_mode(0),
                                 count, self._memory_size)

        self._capturer.dprx_start_capture_frames(count)

    def dprx_stop_capture_frames(self):
        """

        Stop capture frames.

        """

        self._capturer.dprx_stop_capture_frames()

    def dprx_download_captured_events(self, save_to_bin=True, save_to_txt=False, path_to_save="") -> list:
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

        return self._capturer.dprx_download_captured_events(save_to_bin, save_to_txt, path_to_save)

    def dprx_capture_events_selected_packets(self, list_packets: tuple, time_for_capture=1, save_to_bin=True,
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

        return self._capturer.dprx_capture_events_selected_packets(list_packets, time_for_capture, save_to_bin,
                                                                   save_to_txt, path_to_save)

    # Link Block: Link Capabilities
    def dprx_set_link_flags(self, supportMST: bool = True, supportTPS3: bool = True, supportTPS4: bool = True,
                            eDp14bSupport: bool = True,
                            enableDP2: bool = True, supportSsSBM: bool = True):
        """

        Setting link flags.

        Parameters
        ----------
        supportMST : bool
            Flag for indicating support MST
        supportTPS3 : bool
             Flag for indicating support TPS3
        supportTPS4 : bool
             Flag for indicating support TPS4
        eDp14bSupport : bool
             Flag for indicating support eDp14
        enableDP2 : bool
             Flag for indicating enable DP2
        supportSsSBM : bool
             Flag for indicating support SsSBM

        """

        self._link.link_capabilities.dprx_set_link_flags(supportMST, supportTPS3, supportTPS4, eDp14bSupport, enableDP2,
                                                         supportSsSBM)

    def dprx_get_link_flags(self) -> int:
        """

        Return link flags.

        Returns
        -------
        result : int
            Value of flags

        """

        return self._link.link_capabilities.dprx_get_link_flags()

    def dprx_get_edp_link_rates(self) -> int:
        """

        Return eDP link rate.

        Returns
        -------
        result : int
            Link rate

        """

        return self._link.link_capabilities.dprx_get_edp_link_rates()

    def dprx_set_crd_features(self, value: int):
        """

        Set CRD features.

        Parameters
        ----------
        value : int
            CRD features

        """

        self._link.link_capabilities.dprx_set_crd_features(value)

    def dprx_set_force_link_conf(self, value):
        """

        Settings for lane count, bitrate, VS and PE.

        Parameters
        ----------
        value : int
            settings

        """

        self._link.link_capabilities.dprx_set_force_link_conf(value)

    def dprx_get_max_lanes(self) -> int:
        """

        Reads maximum number of lanes for link training. Valid values are 1, 2 and 4.

        Returns
        -------
        result : int
            Maximum number of lanes

        """
        return self._link.link_capabilities.dprx_get_max_lanes()

    def dprx_set_max_lanes(self, lanes: int):
        """

        Defines maximum number of lanes for link training. Valid settings are 1, 2 and 4.

        Parameters
        ----------
        lanes : int
            Count of lanes

        """
        self._link.link_capabilities.dprx_set_max_lanes(lanes)

    def dprx_get_max_link_rate(self) -> int:
        """

        Reads maximum link rate for link training. Setting is multipler for 0.27 Gbps.
        Typical values are 6 (1.62 Gbps), 10 (2.7 Gbps), 20 (5.4 Gbps), 25 (6.5 Gbps) or 30 (8.1 Gbps).

        Returns
        -------
        link_rate : int
            Maximum link rate

        """
        link_rate = self._link.link_capabilities.dprx_get_max_link_rate()
        return link_rate

    def dprx_set_max_link_rate(self, rate):
        """

        Defines maximum link rate for link training. Setting is multipler for 0.27 Gbps.
        Typical values are 6 (1.62 Gbps), 10 (2.7 Gbps), 20 (5.4 Gbps) , 25 (6.5 Gbps) or 30 (8.1 Gbps).

        Parameters
        ----------
        rate : float
            Link rate to be set

        """
        self._link.link_capabilities.dprx_set_max_link_rate(rate)

    def dprx_get_link_capabilities_all_info(self) -> LinkCapabilitiesDprx:
        """

        Return the object of LinkCapabilitiesDprx class. It it contain information about device link capabilities.

        Available info:
            hwSupportMST - Flag of hardware support MST (type: bool)
            forceLinkCfgSupport - Flag of supporting force link configuration (type: bool)
            eDp14bSupport - Flag of supporting eDp14b (type: bool)
            maxLanes - Count of maximum lanes (type: int)
            maxLinkRate - Count of maximum link rate (type: int)
            maxSupportedLinkRate - Count of maximum supported link rate (type: int)
            supportTPS3 - Flag of supporting TPS3 (type: bool)
            supportMST - Flag of supporting MST (type: bool)
            supportTPS4 - Flag of supporting TPS4 (type: bool)
            eDpRates - eDp rates for 8 items (type: list)

        Returns
        -------
        linkCapabilities : LinkCapabilitiesDprx
            Object of class LinkCapabilitiesDprx
        """

        hw_caps = self.dprx_get_hw_caps()

        link_capabilities = LinkCapabilitiesDprx()
        link_capabilities.maxSupportedLinkRate = hw_caps.maxLinkRate
        link_capabilities.hwSupportMST = hw_caps.mst
        link_capabilities.forceLinkCfgSupport = hw_caps.forceLinkCongiguration
        link_capabilities.maxLanes = self.dprx_get_max_lanes()
        link_capabilities.maxLinkRate = self.dprx_get_max_link_rate()
        link_capabilities.eDpRates = self.dprx_get_edp_link_rates()

        int_value = self.dprx_get_link_flags()
        link_capabilities.supportMST = int_value & 1
        link_capabilities.supportTPS3 = (int_value >> 1) & 1
        link_capabilities.supportTPS4 = (int_value >> 2) & 1
        link_capabilities.eDp14bSupport = (int_value >> 3) & 1

        link_capabilities.forceCableStatusToPlugged = self.dprx_get_cable_force()

        return link_capabilities
