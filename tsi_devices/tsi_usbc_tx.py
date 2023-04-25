from .tsi_dp_tx import *
from .tsi_usbc import *


class USBCTX(DPTX, USBC):

    def __init__(self, device: TSIDevice):
        """

        General class for USBC device TX(source) side. Inherited from class USBC and DPTX.
        Class has all available methods from USBC class and DPTX class.

        Parameters
        ----------
        device : TSIDevice
            Indicates the device on which the operation is to be carried out
        """
        DPTX.__init__(self, device)
        USBC.__init__(self, device)
        self.usbc_enable_adc_data_scanner()
