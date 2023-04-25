from .tsi_dp_tx400 import *
from .modules.Link.LinkDP.link_dp20tx import *


class DPTX500(DPTX400):

    def __init__(self, device: TSIDevice):
        """

        General class for DP device 500 series TX(source) side. Inherited from class DPTX400.

        The class contains the following fields:
        linkdp20 - Object of LinkDP20Rx class. Needed to interact with Link of DP 2.0.

        Parameters
        ----------
        device : TSIDevice
            Indicates the device on which the operation is to be carried out
        """
        super().__init__(device)
        self._linkdp20 = LinkDP20Tx(device)

    def dptx_set_dp20_link_rate(self, value: int):
        """

        Set DP 2.0 link rate.

        Parameters
        ----------
        value : int
            Link rate

        """
        self._linkdp20.dptx_set_dp20_link_rate(value)

    def dptx_get_dp20_link_rate(self) -> int:
        """

        Return DP 2.0 link rate.

        Returns
        -------
        value : int
            Link rate

        """
        return self._linkdp20.dptx_get_dp20_link_rate()

    def dptx_set_dp20_lane_count(self, value: int):
        """

        Set DP 2.0 lane count.

        Parameters
        ----------
        value : int
            Lane count

        """
        self._linkdp20.dptx_set_dp20_lane_count(value)

    def dptx_get_dp20_lane_count(self) -> int:
        """

        Return DP 2.0 lane count.

        Returns
        -------
        Result : int
            Lane count

        """
        return self._linkdp20.dptx_get_dp20_lane_count()
