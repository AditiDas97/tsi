from .tsi_dp_rx import *
from .modules.FEC.fec_rx import *
from .modules.Capture.bulk_capture import *
from .modules.DSC.dsc_caps_dprx import *


class DPRX400(DPRX):

    def __init__(self, device: TSIDevice):
        """

        General class for DP device 400 series TX(source) side. Inherited from class DPTX.

        The class contains the following fields:
        fec - Object of FecTx class. Needed to interact with FEC.
        bulk_capturer - Object of BulkCapturer class. Needed to capture, downloading and saving bulk data.
        dsc_caps - Object of DscProperties class. Contain information of DSC capability on Sink side.

        Parameters
        ----------
        device : TSIDevice
            Indicates the device on which the operation is to be carried out
        """
        super().__init__(device)
        self._fec = FecRx(self)
        self._bulk_capturer = BulkCapturer(device)
        self._dsc_caps = DscProperties(device)

    def dprx_get_link_capabilities_all_info(self) -> LinkCapabilitiesDprx:
        """

        Return the object of LinkCapabilitiesDprx class. It it contain information about device link capabilities.

        Available info:
            hwSupportMST - Flag of hardware support MST (type: bool)
            forceLinkCfgSupport - Flag of supporting force link configuration (type: bool)
            eDp14bSupport - Flag of supporting eDp14b (type: bool)
            sscSupported - Flag of supporting SSC (type: bool)
            sscEnabled - Flag of enabling SSC (type: bool)
            dscSupported - Flag of supporting DSC (type: bool)
            dscEnabled - Flag of enabling DSC (type: bool)
            dscLinkEstablished - Flag of Establishing DSC Link(type: bool)
            maxLanes - Count of maximum lanes (type: int)
            maxLinkRate - Count of maximum link rate (type: int)
            maxSupportedLinkRate - Count of maximum supported link rate (type: int)
            enableFastLT - Flag of enabling Fast Link Training (type: bool)
            forceCableStatusToPlugged - Flag of plugged force cable status (type: bool)
            supportTPS3 - Flag of supporting TPS3 (type: bool)
            supportMST - Flag of supporting MST (type: bool)
            supportTPS4 - Flag of supporting TPS4 (type: bool)
            eDpRates - eDp rates for 8 items (type: list)

        Returns
        -------
        linkCapabilities : LinkCapabilitiesDprx
            Object of class LinkCapabilitiesDprx

        """

        link_capabilities = LinkCapabilitiesDprx()
        hw_caps = self.dprx_get_hw_caps()

        link_capabilities.maxSupportedLinkRate = hw_caps.maxLinkRate

        dsc_status = self.dprx_get_dsc_status()
        link_capabilities.dscSupported = (dsc_status & 1) != 0
        link_capabilities.dscLinkEstablished = (dsc_status >> 1) & 1

        if link_capabilities.dscSupported:
            link_capabilities.dscEnabled = "Enabled" if self.dprx_get_dsc() & 1 else "Disabled"

        ssc_status = self.dprx_get_ssc_status()
        link_capabilities.sscEnabled = "Enabled" if ssc_status[0] != 0 else "Disabled"
        link_capabilities.sscSupported = ssc_status[1]

        link_capabilities.hwSupportMST = hw_caps.mst
        link_capabilities.forceLinkCfgSupport = hw_caps.forceLinkCongiguration
        link_capabilities.maxLanes = self.dprx_get_max_lanes()
        link_capabilities.maxLinkRate = self.dprx_get_max_link_rate()
        link_capabilities.eDpRates = self.dprx_get_edp_link_rates()

        int_value = self.dprx_get_link_flags()
        link_capabilities.supportMST = (int_value & 1) != 0
        link_capabilities.supportTPS3 = (int_value >> 1) & 1
        link_capabilities.supportTPS4 = (int_value >> 2) & 1
        link_capabilities.eDp14bSupport = (int_value >> 3) & 1

        link_capabilities.forceCableStatusToPlugged = self.dprx_get_cable_force()

        return link_capabilities

    def start_bulk_capture(self, requested_capture_size, bulk_10bit=True) -> int:
        """

        Initializes main link bulk data capture.

        Parameters
        ----------
        requested_capture_size : int
            Count of bytes to read
        bulk_10bit : bool
            Flag for enabling 8 bit (False) or 10 bit bulk capture (True)

        Returns
        ------
        result : int
            Actual number of bytes to read (can be less than read_data)

        """

        return self._bulk_capturer.start_bulk_capture(requested_capture_size, bulk_10bit)

    def bulk_capture_is_ready(self) -> bool:
        """

        Return current status if bulk capture.

        Returns
        ------
        result : bool
            Actual status of bulk capture

        """

        return self._bulk_capturer.bulk_capture_is_ready()

    def download_bulk_capture(self, capture_size, filename='') -> list:
        """

        Download bulk data into binary file.

        Parameters
        ----------
        capture_size : int
            Count of bytes to read
        filename : str
            The path to the bulk file.

        Returns
        ------
        result : list
            Bulk data

        """

        return self._bulk_capturer.download_bulk_capture(capture_size, filename)

    def stop_bulk_capture(self):
        """

        Stop bulk data capture and free allocated memory.

        """

        self._bulk_capturer.stop_bulk_capture()

    def bulk_capture(self, capture_size, path='', bulk_10bit=True, params=None):
        """

        A sample usecase of bulk capture.
        Performs main link bulk data capture and stores bulk data into binary file.
        Bulk data and AUX BW events are stored into folder, where filename starts with prefix capture
        followed with timestamp (year, month, date, hour, minute, second).

        Parameters
        ----------
        capture_size : int
            Count of bytes to read. Actual size may be smaller depending on device's memory.
        path : str
            The path to the directory where the data will be saved.
        bulk_10bit : bool
            Flag for enabling 8 bit (false) or 10 bit bulk capture (true)
        params : None
            Can be used to more accurately generate a file name. Contain follow info:
            Video resolution, color mode and BPC.

        Returns
        ------
        filepath : str
            Path to the bulk data file

        """

        return self._bulk_capturer.bulk_capture(capture_size, path, bulk_10bit, params)

    # FEC Block
    def dprx_get_error_counters_fec(self) -> FECCounters:
        """

        Return the object of FECCounters class. It contains information about device FEC errors.

        The class contains the following fields:
            uncorrectedBlockErrors - info of uncorrected Block Errors (type: list), each item in list has type int
            correctedBlockErrors - info of corrected Block Errors (type: list), each item in list has type int
            bitErrors - info of bit Errors (type: list), each item in list has type int
            parityBlockErrors - info of parity Block Errors (type: list), each item in list has type int
            parityBitErrors - info of parity Bit Errors (type: list), each item in list has type int

        Returns
        ------
        filepath : FECCounters
           FECCounters data
        """
        return self._fec.dprx_get_error_counters_fec()

    def dprx_clear_counters_fec(self):
        """

        Clear FEC counters.

        """
        self._fec.dprx_clear_counters_fec()

    def dprx_capable_fec(self, capable: bool, generate_hpd: bool = False):
        """

        Set FEC control.

        Parameters
        ----------
        capable : bool
            Enables output of FEC framing and parity data, sends FEC enable sequence
        generate_hpd : bool
            Generate HPD pulse

        """
        self._fec.dprx_capable_fec(capable, generate_hpd)

    def dprx_get_status_fec(self) -> tuple:
        """

        Returns
        ------
        Result : tuple
            Return tuple of values: enabled fec, ready fec, capable fec

        """
        return self._fec.dprx_get_status_fec()

    # PatternGenerator Block
    def dprx_set_stream(self, stream: int):
        """

        Set currently selected stream. The setting can take effect only while MST is enabled by
        the source. Any stream can be selected regardless of it is presence as long as the sink side
        hardware can receive it.

        Parameters
        ----------
        stream: int
            Currently selected stream.
        """

        self._pg.dprx_set_stream(stream)

    def dprx_get_stream(self) -> int:
        """

        Return currently selected stream.

        Returns
        -------
        result : int
            Stream
        """
        return self._pg.dprx_get_stream()

    def dprx_get_dsc_status(self) -> int:
        """

        Return current DSC status: DSC enabled and DSC supported.

        Returns
        -------
        result : int
            Status

        """

        return self._pg.dprx_get_dsc_status()

    def dprx_set_dsc(self, value: bool):
        """

        Enable or disable DSC.

        Parameters
        ----------
        value: bool
            Flag of dsc

        """

        self._pg.dprx_set_dsc(value)

    def dprx_update_dsc_properties(self, value: DscPropertiesStruct):
        """

        Update current DSC capability. Class DscPropertiesStruct contain following fields.
        DscPropertiesStruct info:
            major_version - Current major dsc version
            minor_version - Current minor dsc version
            rc_block_size - Information of RC block size. Available size: (type: int)
                0 - 1024 KB
                1 - 4096 KB
                2 - 16384 KB
                3 - 65536 KB
            rc_buffer_size - Information of RC buffer size in blocks. Available size: 1 - 256 (type: int)
            support_1_slice - Flag of support 1 slice image (type: bool)
            support_2_slice - Flag of support 2 slice image (type: bool)
            support_4_slice - Flag of support 4 slice image (type: bool)
            support_6_slice - Flag of support 6 slice image (type: bool)
            support_8_slice - Flag of support 8 slice image (type: bool)
            support_10_slice - Flag of support 10 slice image (type: bool)
            support_12_slice - Flag of support 12 slice image (type: bool)
            support_16_slice - Flag of support 16 slice image (type: bool)
            support_20_slice - Flag of support 20 slice image (type: bool)
            support_24_slice - Flag of support 24 slice image (type: bool)
            line_buffer_depth - Information of available buffer depth. Available value: (type: int)
                1 - 10 bits.
                2 - 11 bits.
                3 - 12 bits.
                4 - 13 bits.
                5 - 14 bits.
                6 - 15 bits.
                7 - 16 bits.
                8 - 8 bits.
            block_prediction - Flag of support block prediction (type: bool)
            support_rgb - Flag of support rgb format (type: bool)
            support_ycbcr_444 - Flag of support ycbcr 444 format (type: bool)
            support_simple_422 - Flag of support simple 422 format (type: bool)
            support_native_422 - Flag of support native 422 format (type: bool)
            support_ycbcr_420 - Flag of support ycbcr 420 format (type: bool)
            support_8bpc - Flag of support 8 bpc (type: bool)
            support_10bpc - Flag of support 10 bpc (type: bool)
            support_12bpc - Flag of support 12 bpc (type: bool)
            throughput_mode_0 - Information of Decoding of three pixels per clock in units of megapixels per second
            for 4:4:4 and Simple 4:2:2 modes. Available value: (type: int)
                0 - Not supported.
                1 - 340MP/s.
                2 - 400MP/s.
                3 - 450MP/s.
                4 - 500MP/s.
                5 - 550MP/s.
                6 - 600MP/s.
                7 - 650MP/s.
                8 - 700MP/s.
                9 - 750MP/s.
                10 - 800MP/s.
                11 - 850MP/s.
                12 - 900MP/s.
                13 - 950MP/s.
                14 - 1000MP/s.
                15 - 170MP/s
            throughput_mode_1 - Informatino of Decoding of six pixels per clock in units of megapixels per second for
            Native 4:2:2 (DSC v1.2 or higher) and Native 4:2:0 modes (DSC v1.2a or higher). Available value:
            The same of throughput_mode_0 (type: int)
            max_slice_width - Number of maximum slice width support (type: int)
            bpp_inc - Information of Bits per Pixel Increment. Available value: (type: int)
                0 - 1/16
                1 - 1/8
                2 - 1/4
                3 - 1/2
                4 - 1

        Parameters
        ----------
        value : DscPropertiesStruct
            Object of DscPropertiesStruct class
        """

        self._dsc_caps.update_dsc_properties(value)

    def dprx_get_dsc_properties(self) -> DscPropertiesStruct:
        """

        Return current information of dsc capabilities.

        Returns
        -------
            dsc_caps : DscPropertiesStruct
            Object of class DscPropertiesStruct
        """

        return self._dsc_caps.get_dsc_properties()

    def dprx_reset_dsc_properties(self):
        """

        Reset dsc capabilities to default.

        """

        self._dsc_caps.reset_dsc_properties()
