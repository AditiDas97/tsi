from .tsi_dp_tx import *
from .modules.FEC.fec_tx import *


class DPTX400(DPTX):

    def __init__(self, device: TSIDevice):
        """

        General class for DP device 400 series TX(source) side. Inherited from class DPTX.

        The class contains the following fields:
        fec - Object of FecTx class. Needed to interact with FEC.

        Parameters
        ----------
        device : TSIDevice
            Indicates the device on which the operation is to be carried out
        """

        super().__init__(device)
        self._fec = FecTx(device)

    # FEC Block
    def dptx_get_error_counters_fec(self) -> FECCounters:
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
        result = FECCounters()
        nl = self.dptx_get_link_status_lane_count()

        for i in range(nl):
            address = 0x120
            dpcd = self.dptx_read_dpcd(address, 1)
            dpcd[0] &= 1
            dpcd[0] |= (i << 4)
            for j in range(6):
                v = dpcd[0] | (j << 1)
                self.dptx_write_dpcd(address, 1, bytearray(v))
                val = self.dptx_read_dpcd(0x281, 1)
                if val[0] & 0x8000:
                    val = val[0] & 0x7FFF

                if j == 1:
                    result.uncorrectedBlockErrors[i] = val
                elif j == 2:
                    result.correctedBlockErrors[i] = val
                elif j == 3:
                    result.bitErrors[i] = val
                elif j == 4:
                    result.parityBlockErrors[i] = val
                elif j == 5:
                    result.parityBitErrors[i] = val

        return result

    def dptx_clear_counters_fec(self):
        """

        Clear FEC errors.

        """
        self._fec.dptx_clear_counters_fec()

    def dptx_generate_errors_fec(self, settings: FECGeneratorSettings):
        """

        Generate FEC errors.

        errorType = type of error (type: int)
        lanesCounts = [0, 0, 0, 0] (type: list)
        delayMs = count of delay Ms (type: int)

        Parameters
        ----------
        settings : FECGeneratorSettings
            FEC errors (object of FECGeneratorSettings)
        """
        self._fec.dptx_generate_errors_fec(settings)

    def dptx_prefer_enabled_fec(self, enable: bool):
        """

        Set prefer enabled FEC.

        Parameters
        ----------
        enable : bool
            Enable FEC flag

        """
        self._fec.dptx_prefer_enabled_fec(enable)

    def dptx_enable_fec(self, enable: bool):
        """

        Enable FEC mode.

        Parameters
        ----------
        enable : bool
            Enable FEC flag
        """
        self._fec.dptx_enable_fec(enable)

    def dptx_intent_to_enable_fec(self, enable: bool):
        """

        Intend to enable FEC mode.

        Parameters
        ----------
        enable : bool
            Enable FEC flag
        """
        self._fec.dptx_intent_to_enable_fec(enable)

    def dptx_get_status_fec(self) -> tuple:
        """

        Return FEC status.

        Returns
        ----------
        Result : tuple
            enabled_status_fec : bool
            enabled_fec : bool
        """

        return self._fec.dptx_get_status_fec()

    # PatterGenerator Block
    def dptx_set_mst(self, value: bool):
        """

        Enable MST mode.

        Parameters
        ----------
        value : bool
            Enable MST flag
        """
        self._pg.dptx_set_mst(value)

    # Link configuration Block
    def dptx_get_link_setup_all_info(self) -> LinkSetupDpTx:
        """

        Return the object of LinkSetupDpTx class. It contains information about device link setup.

        Available info:
            maxSupportedLinkRate - count of maximum supported link rate (type : int)
            lanesCount - count of lanes (type : int)
            linkRate - count of link rate (type : int)
            enhancedFraming - type of framing selection (type : int)
            supportedSSC = flag of SSC support (type : bool)
            enabledSSC = flag of SSC enable (type : bool)
            downspreadAMP = count of down spread AMP (type : int)
            downspreadFREQ = count of down spread FREQ (type : int)

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
        value = self.dptx_get_downspread_status()
        link_setup.enabledSSC = value & 0x1
        link_setup.supportedSSC = (value >> 1) & 0x1
        link_setup.downspreadAMP = self.dptx_get_downspread_amp()
        link_setup.downspreadFREQ = self.dptx_get_downspread_freq()

        return link_setup

    def dptx_set_enable_ssc(self, value: bool):
        """

        Set enable SSC.

        Parameters
        ----------
        value : bool
            Flag of SSC enabled

        """

        self._link.link_configuration.dptx_set_enable_ssc(value)

    def dptx_set_downspread_amp(self, value: int):
        """

        Amplitude of down-spread, x10 %. Default 0.5%, maximum 5%, minimum 0.1%, step 0.1%.
        (I.e. register value from 1 to 50).

        Parameters
        ----------
        value : int
            value from 1 to 50

        """
        return self._link.link_configuration.dptx_set_downspread_amp(value)

    def dptx_get_downspread_amp(self) -> int:
        """

        Return downspread AMP.

        Returns
        -------
        result : int
            value from 1 to 50
        """

        return self._link.link_configuration.dptx_get_downspread_amp()

    def dptx_set_downspread_freq(self, value: int):
        """

        Set Frequency of down-spread. Default value = 31500Hz.

        Parameters
        ----------
        value : int
            Frequency of down-spread(Hz). Maximum 63000Hz, minimum 30000Hz.

        """

        self._link.link_configuration.dptx_set_downspread_freq(value)

    def dptx_get_downspread_freq(self) -> int:
        """

        Return Frequency of down-spread.

        Returns
        -------
        result : int
            value from 30000 to 630000
        """

        return self._link.link_configuration.dptx_get_downspread_freq()
