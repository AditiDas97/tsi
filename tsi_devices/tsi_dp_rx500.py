from .tsi_dp_rx400 import *
from .modules.Link.LinkDP.link_dp20rx import *


class DPRX500(DPRX400):

    def __init__(self, device: TSIDevice):
        """

        General class for DP device 500 series RX(sink) side. Inherited from class DPRX400.

        The class contains the following fields:
        linkdp20 - Object of LinkDP20Rx class. Needed to interact with Link of DP 2.0.

        Parameters
        ----------
        device : TSIDevice
            Indicates the device on which the operation is to be carried out
        """
        super().__init__(device)
        self._linkdp20 = LinkDP20Rx(device)

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
        link_status.linkRate = str(dict_usbc_bit_rate_rev_values.get(self.dprx_get_link_rate())) + " Gbps"

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

        preset = self.dprx_get_dp20_ffe_preset()
        for i in range(4):
            link_status.initial.lanes[i].ffe_preset = ((preset >> (i * 8)) & 0xFF)

        pre_emphasis = self.dprx_get_lt_pre_emphasis()
        for j in range(4):
            link_status.initial.lanes[j].pre_emphasis = pre_emphasis[j]

        link_status.initial.BitRateGbps = str(dict_usbc_bit_rate_rev_values.get(self.dprx_get_lt_bit_rate())) + " Gbps"
        link_status.initial.lanesCount = self.dprx_get_lt_lane_count() & 0xFF
        link_status.initial.eDpBitRate = '{:.2f}'.format(self.dprx_get_edp_link())

        ltInfo = self.dprx_get_iop()
        if type(ltInfo) == list and len(ltInfo) > 0:
            link_status.alpm.trainPattern = (ltInfo[0] & 0xFF)
            link_status.alpm.sleepPattern = ((ltInfo[0] >> 16) & 0xF)
            link_status.alpm.wakeupPattern = ((ltInfo[0] >> 20) & 0xF)
            link_status.alpm.alpmSequenceLocation = ((ltInfo[0] >> 28) & 0xF)
            link_status.alpm.crPatternDurationUs = ltInfo[2]
            link_status.alpm.eqPatternDurationUs = ltInfo[3]
            link_status.alpm.eieosPatternDurationUs = ltInfo[4]
            link_status.alpm.alpmSequenceCounter = ltInfo[5]
            link_status.alpm.bitrateGbps = ((ltInfo[20 * 3 + 18]) / 1000000.0)

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

        if self.__type.find("400") != -1 or self.__type.find("424") != -1 or self.__type.find("500") != -1:
            value = self.dprx_get_ssc_status()
            link_status.enabledSSC = value[0]
            link_status.supportedSSC = value[1]

        return link_status

    def dprx_set_dp20_link_rate(self, value: int):
        """

        Set DP 2.0 link rate.

        Parameters
        ----------
        value : int
            Link rate

        """
        self._linkdp20.dprx_set_dp20_link_rate(value)

    def dprx_get_dp20_link_rate(self) -> int:
        """

        Return DP 2.0 link rate.

        Returns
        -------
        result : int
            Link rate

        """
        return self._linkdp20.dprx_get_dp20_link_rate()

    def dprx_get_dp20_ffe_preset(self) -> int:
        """

        Return DP2.0 FFE pre-set was achieved during Link Training.

        Returns
        -------
        result : int
            FFE pre-set

        """
        return self._linkdp20.dprx_get_dp20_ffe_preset()
