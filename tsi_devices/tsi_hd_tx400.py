from .tsi_hd_tx import HDTX, TSIDevice, LinkControlFRLHdtx, LinkStatusFRLHdtx
from .modules.CEC.cec_hdtx import *


class HDTX400(HDTX):

    def __init__(self, device: TSIDevice):
        """

        General class for HDMI device 400 series RX(source) side. Inherited from class HDTX.

        The class contains the following fields:
        cec - Object of CecHdTx class. Contain some information about CEC.

        Parameters
        ----------
        device : TSIDevice
            Indicates the device on which the operation is to be carried out
        """
        super().__init__(device)
        self._cec = CecHdTx(device)

    # Link Block: Frl Control
    def hdtx_get_link_control_frl_all_info(self) -> LinkControlFRLHdtx:
        """

        Return the object of LinkControlFRLHdtx class. It contains information about device link status.

        Available info:
            linkModeFRLMax - info of FRL link mode (type: int)
            ltTimeout - info of Link Training timeout (type: int)
            ltPollTimeout - info fo Link Training POLL timeout (type: int)
            ffeMax - info of FFE Max (type: list)

        Returns
        -------
        result : LinkControlFRLHdtx
            Link status HdTx data
        """
        _linkControlFRL = LinkControlFRLHdtx()

        hdtx_frl_caps = self.hdtx_get_frl_capability()
        _linkControlFRL.linkModeFRLMax = hdtx_frl_caps[0]
        for i in range(1, len(hdtx_frl_caps)):
            _linkControlFRL.ffeMax[i - 1] = hdtx_frl_caps[i]

        hdtx_frl_timers = self.hdtx_get_frl_timers()
        _linkControlFRL.ltTimeout = hdtx_frl_timers[0]
        _linkControlFRL.ltPollTimeout = hdtx_frl_timers[1]

        return _linkControlFRL

    def hdtx_get_link_status_frl_all_info(self) -> LinkStatusFRLHdtx:
        """

        Return the object of LinkStatusFRLHdtx class. It contains information about device link status.

        Available info:
            frlMode - info of FRL mode (type: int)
            channelLock - info of Channel Lock for each lane (type: list)
            pattern - info of patter for each lane (type: list)
            lastPattern - info of last patter for each lane (type: list)
            ffeLevel - info of FFe level for each lane (type: list)
            ltStatus - info of Link training status (type: int)
            errorCounters - info of error counters for each lane (type: list)
            fltUpdate - FLT update state (type: bool)
            fltReady - FLT Ready state (type: bool)
            frlStart - FRL Start state (type: bool)
            fltNoTimeout - FLT No timeout state (type: bool)
            frlMax - FRL Max state (type: bool)

        Returns
        -------
        result : LinkStatusFRLHdtx
            Link status HdTx data

        """
        linkStatusFRL = LinkStatusFRLHdtx()

        error_counters = self.hdtx_get_lanes_error_counters()
        for i in range(len(error_counters)):
            linkStatusFRL.errorCounters[i] = error_counters[i]

        hdtx_frl_status = self.hdtx_get_frl_status()
        linkStatusFRL.frlMode = hdtx_frl_status & 0xF
        linkStatusFRL.fltReady = (hdtx_frl_status >> 4) & 0x1
        linkStatusFRL.frlStart = (hdtx_frl_status >> 5) & 0x1
        linkStatusFRL.fltNoTimeout = (hdtx_frl_status >> 6) & 0x1
        linkStatusFRL.fltUpdate = (hdtx_frl_status >> 7) & 0x1
        linkStatusFRL.frlMax = (hdtx_frl_status >> 8) & 0x1

        chx_lnx = (hdtx_frl_status >> 25) & 0xF
        for i in range(4):
            linkStatusFRL.channelLock[i] = (chx_lnx >> i) & 0x1

        lnx_ltp_req = (hdtx_frl_status >> 9) & 0xFFFF
        for i in range(4):
            linkStatusFRL.ffeLevel[i] = (lnx_ltp_req >> (i * 4)) & 0xF

        lnx_ltp_req = self.hdtx_get_pattern()
        for i in range(4):
            linkStatusFRL.pattern[i] = lnx_ltp_req[i]

        last_lnx_ltp_req = self.hdtx_get_last_pattern()
        for i in range(4):
            linkStatusFRL.lastPattern[i] = last_lnx_ltp_req[i]

        linkStatusFRL.ltStatus = (self.hdtx_get_sink_status() >> 2) & 0xF

        return linkStatusFRL

    def hdtx_get_ffe_max(self) -> tuple:
        """

        Return current values of FFE max.

        Returns
        -------
        result : tuple
            FFE max
        """
        return self._link.frl_control.hdtx_get_ffe_max()

    def hdtx_get_lt_timeout(self) -> int:
        """

        Return Link Training timeout.

        Returns
        -------
        result : int
            Timeout
        """
        return self._link.frl_control.hdtx_get_lt_timeout()

    def hdtx_get_lt_poll_timeout(self) -> int:
        """

        Return Link Training POLL timeout.

        Returns
        -------
        result : int
            POLL timeout

        """
        return self._link.frl_control.hdtx_get_lt_poll_timeout()

    def hdtx_set_sink_feature(self, value: int):
        """

        Set Sink feature (Change state of a feature.
        Each change of feature state means communication with Sink device and may fail).

        Parameters
        ----------
        value : int
            0 - Does nothing
            1 - Enabled scrambler.
            2 - Disable scrambler.
            3 - Set 3G mode link mode.
            4 - Set 6G mode link mode.
            5 - Do FRL Link Training

        """
        self._link.frl_control.hdtx_set_sink_feature(value)

    def hdtx_set_frl_capability(self, link_mode_frl_max: int, ffe_max: list):
        """

        Set FRL mode configuration.

        Parameters
        ----------
        link_mode_frl_max : int
            0 - FRL_Disable
            1 - FRL_3L_03G
            2 - FRL_3L_06G
            3 - FRL_4L_06G
            4 - FRL_4L_08G
            5 - FRL_4L_10G
            6 - FRL_4L_12G
        ffe_max : list
            MAX FFE LEVEL FOR Each Mode 1..6.
                2 bits per each mode
                5..6 bits for 3G3Lane
                7..8 bits for 6G3Lane
                9..10 bits for 6G4Lane
                11..12 bits for 8G4Lane
                13..14 bits for 10G4Lane
                15..16 bits for 12G4Lane

        """
        self._link.frl_control.hdtx_set_frl_capability(link_mode_frl_max, ffe_max)

    def hdtx_get_frl_capability(self) -> tuple:
        """

        Return current FRL mode configuration.

        Returns
        -------
        result : tuple
            FRL mode configuration
        """
        return self._link.frl_control.hdtx_get_frl_capability()

    def hdtx_set_frl_timers(self, lt_timeout: int, lt_poll_timeout: int):
        """

        Set FRL timers.

        Parameters
        ----------
        lt_timeout : int
            Link Training timeout
        lt_poll_timeout : int
            Link Training POLL timeout

        """
        self._link.frl_control.hdtx_set_frl_timers(lt_timeout, lt_poll_timeout)

    def hdtx_get_frl_timers(self) -> tuple:
        """

        Return current FRL timers.
        If you want to get one of frl timers, please, see function 'hdtx_get_lt_timeout'
        and 'hdtx_get_lt_poll_timeout'

        Returns
        -------
        Result : tuple
            FRL timers
        """
        return self._link.frl_control.hdtx_get_frl_timers()

    # Link Block: FRL Status
    def hdtx_get_link_mode_frl(self) -> int:
        """

        Return current FRL mode.

        Returns
        -------
        Result : int
            FRL mode
        """
        return self._link.frl_status.hdtx_get_link_mode_frl()

    def hdtx_get_link_status_frl(self, value: int) -> int:
        """

        Get link status FRL.

        Parameters
        ----------
        value : int
            4 - get FLT Ready
            5 - get FRL Start
            6 - get FLT NoTimeout
            7 - get FLTUpdate
            8 - get FRL Max

        Returns
        -------
        Result : int
            Link status FRL
        """

        return self._link.frl_status.hdtx_get_link_status_frl(value)

    def hdtx_get_channel_lock(self) -> tuple:
        """

        Return current channel lock (channel lock for each lane,
        one element in tuple per lane)

        Returns
        -------
        channel_lock : tuple
            Channel lock
        """

        return self._link.frl_status.hdtx_get_channel_lock()

    def hdtx_get_ffe_level(self) -> tuple:
        """

        Return current FFE level.
        FFE level has 4 gradations:
            0 - TFFE 0
            1 - TFFE 1
            2 - TFFE 2
            3 - TFFE 3

        Returns
        -------
        ffe_level : list
            FFE level values
        """

        return self._link.frl_status.hdtx_get_ffe_level()

    def hdtx_get_pattern(self) -> tuple:
        """

        Return Link Pattern on each lane.
        Link Pattern has gradation:
            0x00 - No Link Pattern
            0x01 - All 1’s
            0x02 - All 0’s
            0x03 - Nyquist clock pattern
            0x04 - Source TxFFE Compliance Test Pattern
            0x05 - LFSR 0
            0x06 - LFSR 1
            0x07 - LFSR 2
            0x08 - LFSR 3
            0x0F - Special coded message

        Returns
        -------
        Result : tuple
            Link pattern
        """

        return self._link.frl_status.hdtx_get_pattern()

    def hdtx_get_last_pattern(self) -> tuple:
        """

        Return Last Link Pattern on each lane.
        Link Pattern has gradation:
            0x00 - No Link Pattern
            0x01 - All 1’s
            0x02 - All 0’s
            0x03 - Nyquist clock pattern
            0x04 - Source TxFFE Compliance Test Pattern
            0x05 - LFSR 0
            0x06 - LFSR 1
            0x07 - LFSR 2
            0x08 - LFSR 3
            0x0F - Special coded message

        Returns
        -------
        Result : tuple
            Link pattern
        """

        return self._link.frl_status.hdtx_get_last_pattern()

    # CEC Block
    def hdtx_get_capability(self) -> int:
        """

        Return HDTX Capability.

        Returns
        -------
        Result : int
            Capability

        """

        return self._cec.hdtx_get_capability()

    def hdtx_get_cec_status(self) -> bool:
        """

        Return current CEC state.

        Returns
        -------
        Result : bool
            True - supported
            False - not supported

        """

        return self._cec.hdtx_get_cec_status()

    def hdtx_get_cec_log(self) -> int:
        """

        Return CEC log.

        Returns
        -------
        Result : bool
            True - Enabled CEC frames logging
            False - Disabled CEC frames logging

        """

        return self._cec.hdtx_get_cec_log()

    def hdtx_set_cec_state(self, value: bool):
        """

        Set CEC state.

        Parameters
        ----------
        value: bool
            False - Disable CEC
            True - Enable CEC

        """

        self._cec.hdtx_set_cec_state(value)

    def hdtx_get_cec_version(self) -> int:
        """

        Return CEC version.

        Returns
        -------
        Result : int
            CEC version

        """
        return self._cec.hdtx_get_cec_version()

    def hdtx_set_cec_logical_address(self, value):
        """

        Set CEC logical address.

        Parameters
        -------
        value : int
            CEC logical address

        """
        self._cec.hdtx_set_cec_logical_address(value)

    def hdtx_get_cec_logical_address(self) -> int:
        """

        Return CEC logical address.

        Returns
        -------
        result : int
            CEC logical address

        """
        return self._cec.hdtx_get_cec_logical_address()

    def hdtx_set_cec_phy_address(self, value):
        """

        Set CEC physical address.

        Parameters
        -------
        value : int
            CEC physical address

        """
        self._cec.hdtx_set_cec_phy_address(value)

    def hdtx_get_cec_phy_address(self) -> int:
        """

        Return CEC physical address.

        Returns
        -------
        result : int
            CEC logical address

        """
        return self._cec.hdtx_get_cec_phy_address()

    def hdtx_set_cec_op_code(self, value):
        """

        Set CEC OP code.

        Parameters
        -------
        value : int
            CEC OP code

        """
        self._cec.hdtx_set_cec_op_code(value)

    def hdtx_get_cec_op_code(self) -> int:
        """

        Return CEC OP code.

        Returns
        -------
        result : int
            CEC OP code

        """
        return self._cec.hdtx_get_cec_op_code()

    def hdtx_set_cec_op_code_param(self, value):
        """

        Set CEC OP code parameters.

        Parameters
        -------
        value : int
            CEC OP code parameters

        """
        self._cec.hdtx_set_cec_op_code_param(value)

    def hdtx_get_cec_op_code_param(self):
        """

        Return CEC OP code parameters.

        Returns
        -------
        result : int
            CEC OP code parameters

        """
        return self._cec.hdtx_get_cec_op_code_param()

    def hdtx_set_cec_device_type(self, value):
        """

        Set CEC device type.
        Bit 7 – TV
        Bit 6 – Rec Dev
        Bit 5 – Tuner
        Bit 4 – PB Device
        Bit 3 – Audio System
        Bit 2 – CEC Switc

        Parameters
        -------
        value : int
            CEC device type

        """
        self._cec.hdtx_set_cec_device_type(value)

    def hdtx_get_cec_device_type(self) -> int:
        """

        Return CEC device type.
        Bit 7 – TV
        Bit 6 – Rec Dev
        Bit 5 – Tuner
        Bit 4 – PB Device
        Bit 3 – Audio System
        Bit 2 – CEC Switc

        Returns
        -------
        result : int
            CEC device type

        """
        return self._cec.hdtx_get_cec_device_type()
