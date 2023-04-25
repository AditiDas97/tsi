from .tsi_dp_rx import *
from .tsi_usbc import *


class USBCRX(DPRX, USBC):

    def __init__(self, device: TSIDevice):
        """

        General class for USBC device RX(sink) side. Inherited from class USBC and DPRX.
        Class has all available methods from USBC class and DPRX class.

        Parameters
        ----------
        device : TSIDevice
            Indicates the device on which the operation is to be carried out
        """
        DPRX.__init__(self, device)
        USBC.__init__(self, device)
        self.usbc_enable_adc_data_scanner()
