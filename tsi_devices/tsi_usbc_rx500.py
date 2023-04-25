from .tsi_dp_rx500 import *
from .tsi_usbc import *


class USBCRX500(DPRX500, USBC):

    def __init__(self, device: TSIDevice):
        """

        General class for USBC device RX(sink) side. Inherited from class USBC and DPRX500.
        Class has all available methods from USBC class and DPRX500 class.

        Parameters
        ----------
        device : TSIDevice
            Indicates the device on which the operation is to be carried out
        """
        DPRX500.__init__(self, device)
        USBC.__init__(self, device)
