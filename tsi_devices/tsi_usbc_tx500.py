from .tsi_dp_tx500 import *
from .tsi_usbc import *


class USBCTX500(DPTX500, USBC):

    def __init__(self, device: TSIDevice):
        """

        General class for USBC device TX(source) side. Inherited from class USBC and DPTX500.
        Class has all available method, type_c=True
        device : TSIDevice
            Indicates the device on which the operation is to be carried out
        """
        DPTX500.__init__(self, device)
        USBC.__init__(self, device)
        self.usbc_enable_adc_data_scanner()
