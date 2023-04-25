from .tsi_hd_rx import *
from .modules.CEC.cec_hdrx import *


class HDRX400(HDRX):

    def __init__(self, device: TSIDevice):
        """

        General class for HDMI device 400 series RX(source) side. Inherited from class HDRX.

        The class contains the following fields:
        cec - Object of CecHdRx class. Contain some information about CEC.

        Parameters
        ----------
        device : TSIDevice
            Indicates the device on which the operation is to be carried out
        """
        super().__init__(device)
        self._cec = CecHdRx(device)

    def hdrx_get_link_control_frl_all_info(self) -> LinkControlFRL:
        """

        Return the object of LinkControlFRL class. It contains information about device link control FRL.

        Available info:
            linkModeFRLMax - info of link mode FRL(type: int)
            frlStart - info of FRL Start (type: bool)
            fltReady - info of FRL Ready (type: bool)
            fltNoTimeout - info of FRL No Timeout (type: bool)
            frlMax - info of FRL Max (type: bool)
            checkPatterns - flag of check patterns (type: bool)
            ltpAdd - list of LTP add (type: list)

        Returns
        -------
        result : LinkControlFRL
            Link Control FRL HdRx data

        """

        _linkControlFRL = LinkControlFRL()

        frl_cap = self.hdrx_get_frl_capability()
        _linkControlFRL.linkModeFRLMax = frl_cap & 0xF
        _linkControlFRL.frlStart = ((frl_cap >> 4) & 0x1)
        _linkControlFRL.fltReady = ((frl_cap >> 5) & 0x1)
        _linkControlFRL.fltNoTimeout = ((frl_cap >> 6) & 0x1)
        _linkControlFRL.frlMax = ((frl_cap >> 7) & 0x1)
        _linkControlFRL.checkPatterns = ((frl_cap >> 8) & 0x1)
        lnx_ltp_add = (self.hdrx_get_frl_pattern() >> 16) & 0xFFFF
        for i in range(4):
            _linkControlFRL.ltpAdd[i] = (lnx_ltp_add >> (i * 4)) & 0xF

        return _linkControlFRL

    # Link Block: FRL
    def hdrx_get_link_mode_frl(self) -> int:
        """

        Return current link mode FRL.

        Returns
        -------
        result : int
            Link mode FRL

        """

        return self._link.frl_status.hdrx_get_link_mode_frl()

    def hdrx_get_lt_status(self) -> int:
        """

        Return current LT status.

        Returns
        -------
        result : int
            LT status

        """

        return self._link.frl_status.hdrx_get_lt_status()

    def hdrx_get_flt_update(self) -> int:
        """

        Return FLT info.

        Returns
        -------
        result : int
            FLT

        """

        return self._link.frl_status.hdrx_get_flt_update()

    def hdrx_get_flt_no_retrain(self) -> int:
        """

        Return FLT no retrain info.

        Returns
        -------
        result : int
            FLT

        """

        return self._link.frl_status.hdrx_get_flt_no_retrain()

    def hdrx_get_channel_lock(self) -> tuple:
        """

        Return current channel lock.

        Returns
        -------
        result : tuple
            Channel lock

        """

        return self._link.hdrx_get_channel_lock()

    def hdrx_get_frl_data(self) -> tuple:
        """

        Return current FRL data.

        Returns
        -------
        result : tuple
            FRL data

        """

        return self._link.frl_status.hdrx_get_frl_data()

    def hdrx_get_frl_capability(self) -> int:
        """

        Return current FRL capability.

        Returns
        -------
        result : int
            FRL capability

        """

        return self._link.frl_control.hdrx_get_frl_capability()

    def hdrx_set_frl_capability(self, link_mode_frl_max, value: list):
        """

        Set FRL capability.

        Parameters
        -------
        link_mode_frl_max : int
            Link mode FRL max info
                0 - Disable FRL
                1 - 3Gbps 3-lane
                2 - 6Gbps 3-lane
                3 - 6Gbps 4-lane
                4 - 8Gbps 4-lane
                5 - 10Gbps 4-lane
                6 - 12Gbps 4-lane
                7-15 - unused
        value : list
            frl_start - frl start info
            flt_ready - frl ready info
            flt_no_timeout - frl no timeout info
            frl_max - frl max info
            check_pattern - check pattern info

        """
        self._link.frl_control.hdrx_set_frl_capability(link_mode_frl_max, value)

    def hdrx_get_frl_pattern(self) -> int:
        """

        Return current FRL pattern.

        Returns
        -------
        result : int
            FRL pattern

        """

        return self._link.frl_status.hdrx_get_frl_pattern()

    def hdrx_set_frl_pattern(self, value: int):
        """

        Set FRL pattern.
            0..15	Lnx_LTP_Req
                LTP Pattern request values.
                0 = No Link Pattern
                1=All 1’s
                2=All 0’s
                3=Nyquist clock pattern
                4=Source TxFFE Compliance Test Pattern
                5=LFSR 0
                6=LFSR 1
                7=LFSR 2
                8=LFSR 3
                9-14=Reserved
                15=Special coded message
                16=Special coded message
            16..31	Lnx_LTPAdditional
                LTP Pattern request. 4-bits for each channel
                0 = No Link Pattern
                1=All 1’s
                2=All 0’s
                3=Nyquist clock pattern
                4=Source TxFFE Compliance Test Pattern
                5=LFSR 0
                6=LFSR 1
                7=LFSR 2
                8=LFSR 3
                9-14=Reserved
                15=Special coded message
                16=Special coded message

        Parameters
        -------
        value : int
            FRL pattern
        """

        self._link.frl_status.hdrx_set_frl_pattern(value)

    def hdrx_get_link_mode_frl_max(self) -> int:
        """

        Return current link mode FRL max.

        Returns
        -------
        result : int
            Link mode FRL
        """

        return self._link.frl_control.hdrx_get_link_mode_frl_max()

    def hdrx_get_frl_start(self) -> int:
        """

        Return current FRL start info.

        Returns
        -------
        result : int
            FRL start info
        """

        return self._link.frl_control.hdrx_get_frl_start()

    def hdrx_get_frl_ready(self) -> int:
        """

        Return current FRL ready info.

        Returns
        -------
        result : int
            FRL ready info
        """

        return self._link.frl_control.hdrx_get_frl_ready()

    def hdrx_get_frl_no_timeout(self) -> int:
        """

        Return current FRL no timeout info.

        Returns
        -------
        result : int
            FRL no timeout info
        """

        return self._link.frl_control.hdrx_get_frl_no_timeout()

    def hdrx_get_frl_max(self) -> int:
        """

        Return current FRL max info.

        Returns
        -------
        result : int
            FRL max info
        """

        return self._link.frl_control.hdrx_get_frl_max()

    def hdrx_get_frl_check_patterns(self) -> int:
        """

        Return current FRL check patterns info.

        Returns
        -------
        result : int
            FRL check patterns info

        """

        return self._link.frl_control.hdrx_get_frl_check_patterns()

    def hdrx_get_frl_ffe(self) -> int:
        """

        Return current FRL FFE info.

        Returns
        -------
        result : int
            FRL check patterns info

        """

        return self._link.frl_status.hdrx_get_frl_ffe()

    def hdrx_get_ltp_req(self) -> tuple:
        """

        Return current LTP req info.

        Returns
        -------
        result : tuple
            LTP req info

        """

        return self._link.frl_status.hdrx_get_ltp_req()

    def hdrx_get_ltp_add(self) -> tuple:
        """

        Return current LTP add info.

        Returns
        -------
        result : tuple
            LTP add info

        """

        return self._link.frl_status.hdrx_get_ltp_add()

    # CEC Block
    def hdrx_set_cec_ctrl(self, value):
        """

        Enable or Disable CEC.

        Parameters
        -------
        value : int
            CEC status: 0 - Disable, 1 - Enable

        """
        self._cec.hdrx_set_cec_ctrl(value)

    def hdrx_get_cec_ctrl(self) -> int:
        """

        Return CEC status.

        Returns
        -------
        result : int
            CEC status: 0 - Disable, 1 - Enable

        """
        return self._cec.hdrx_get_cec_ctrl()

    def hdrx_set_cec_cmd(self, value):
        """

        Send CEC command.

        Parameters
        -------
        value : int
            CEC command

        """
        self._cec.hdrx_set_cec_cmd(value)

    def hdrx_get_cec_cmd(self):
        """

        Return CEC command.

        Returns
        -------
        result : int
            CEC command

        """
        return self._cec.hdrx_get_cec_cmd()

    def hdrx_get_cec_version(self) -> int:
        """

        Return CEC version

        Returns
        -------
        result : int
            CEC version

        """
        return self._cec.hdrx_get_cec_version()

    def hdrx_set_cec_logical_address(self, value):
        """

        Set CEC logical address.

        Parameters
        -------
        value : int
            CEC logical address

        """
        self._cec.hdrx_set_cec_logical_address(value)

    def hdrx_get_cec_logical_address(self) -> int:
        """

        Return CEC logical address.

        Returns
        -------
        result : int
            CEC logical address

        """
        return self._cec.hdrx_get_cec_logical_address()

    def hdrx_set_cec_phy_address(self, value):
        """

        Set CEC physical address.

        Parameters
        -------
        value : int
            CEC physical address

        """
        self._cec.hdrx_set_cec_phy_address(value)

    def hdrx_get_cec_phy_address(self) -> int:
        """

        Return CEC physical address.

        Returns
        -------
        result : int
            CEC logical address

        """
        return self._cec.hdrx_get_cec_phy_address()

    def hdrx_set_cec_op_code(self, value):
        """

        Set CEC OP code.

        Parameters
        -------
        value : int
            CEC OP code

        """
        self._cec.hdrx_set_cec_op_code(value)

    def hdrx_get_cec_op_code(self) -> int:
        """

        Return CEC OP code.

        Returns
        -------
        result : int
            CEC OP code

        """
        return self._cec.hdrx_get_cec_op_code()

    def hdrx_set_cec_op_code_param(self, value):
        """

        Set CEC OP code parameters.

        Parameters
        -------
        value : int
            CEC OP code parameters

        """
        self._cec.hdrx_set_cec_op_code_param(value)

    def hdrx_get_cec_op_code_param(self):
        """

        Return CEC OP code parameters.

        Returns
        -------
        result : int
            CEC OP code parameters

        """
        return self._cec.hdrx_get_cec_op_code_param()

    def hdrx_set_cec_device_type(self, value):
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
        self._cec.hdrx_set_cec_device_type(value)

    def hdrx_get_cec_device_type(self) -> int:
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
        return self._cec.hdrx_get_cec_device_type()
