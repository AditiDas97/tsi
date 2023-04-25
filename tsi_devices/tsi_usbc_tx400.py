from .tsi_dp_tx400 import *
from .tsi_usbc import *


class USBCTX400(DPTX400, USBC):

    def __init__(self, device: TSIDevice):
        """

        General class for USBC device TX(source) side. Inherited from class USBC and DPTX400.
        Class has all available methods from USBC class and DPTX400 class.

        Parameters
        ----------
        device : TSIDevice
            Indicates the device on which the operation is to be carried out
        """
        DPTX400.__init__(self, device)
        USBC.__init__(self, device)
        self.usbc_enable_adc_data_scanner()
