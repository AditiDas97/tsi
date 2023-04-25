from tsi.tsi_devices.libs.lib_tsi.tsi import *


class Status:

    def __init__(self):
        self.statusDataRole = None
        self.statusPowerRole = None
        self.statusVconn = None

    def print_info(self):
        info = "Status\n" \
               "Data role:  {}\n" \
               "Power role: {}\n" \
               "VConn:      {}\n".format(self.statusDataRole, self.statusPowerRole, self.statusVconn)
        return info


class DUTStatus:

    def __init__(self):
        self.dutDataRole = None
        self.dutPowerRole = None
        self.dutVconn = None

    def print_info(self):
        info = "DUT Status\n" \
               "Data role:  {}\n" \
               "Power role: {}\n" \
               "VConn:      {}\n".format(self.dutDataRole, self.dutPowerRole, self.dutVconn)
        return info


class PDContract:

    def __init__(self):
        self.PDOType = None
        self.PDOVoltage = None
        self.PDOMaxCurr = None
        self.RDOMaxCurr = None
        self.RDOOperCurr = None
        self.usbSuspend = None
        self.capMismatch = None
        self.usbCommCapable = None
        self.giveBack = None

    def print_info(self):
        info = "PD Contract\n" \
               "Power Source\n" \
               "-PDO Type:              {}\n" \
               "-PDO voltage:           {}\n" \
               "-PDO max current:       {}\n" \
               "Power Sink\n" \
               "-RDO max current:       {}\n" \
               "-RDO oper current:      {}\n" \
               "-Nn USB suspend:        {}\n" \
               "-Capability mismatch:   {}\n" \
               "-Give back:             {}\n"\
            .format(self.PDOType, self.PDOVoltage, self.PDOMaxCurr, self.RDOMaxCurr, self.RDOOperCurr, self.usbSuspend,
                    self.usbCommCapable, self.capMismatch, self.giveBack)
        return info


class BusElectricalStatus:

    def __init__(self):
        self.vbusVoltage = None
        self.vbusCurrent = None
        self.cc1Voltage = None
        self.cc2Voltage = None
        self.vconnVoltage = None
        self.vconnCurrent = None
        self.sbu1Voltage = None
        self.sbu2Voltage = None

    def print_info(self):
        info = "Bus Electrical Status\n" \
               "Vbus voltage:   {}\n" \
               "Vbus current:   {}\n" \
               "CC1 voltage:    {}\n" \
               "CC2 voltage:    {}\n" \
               "VCONN voltage:  {}\n" \
               "VCONN current:  {}\n" \
               "SBU-1 voltage:  {}\n" \
               "SBU-2 voltage:  {}\n"\
            .format(self.vbusVoltage, self.vbusCurrent, self.cc1Voltage, self.cc2Voltage, self.vconnVoltage,
                    self.vconnCurrent, self.sbu1Voltage, self.sbu2Voltage)
        return info


class DUTDiscovery:

    def __init__(self):
        self.hostCapable = None
        self.deviceCapable = None
        self.prodTypeDFP = None
        self.prodTypeUFP = None
        self.usbVendorID = None
        self.usbProdID = None
        self.BCDDevice = None
        self.SVID0 = None
        self.SVID1 = None
        self.cnt = None
        self.vdo = []

    def print_info(self):
        info = "DUT Discovery\n" \
               "Data Capable as Host:   {}\n" \
               "Data Capable as Device: {}\n" \
               "Product Type DFP:       {}\n" \
               "Product Type UFP:       {}" \
               "USB Vendor ID:          {}\n" \
               "USB Product ID:         {}\n" \
               "BCD Device:             {}\n" \
               "SVID0:                  {}\n" \
               "SVID1:                  {}\n"\
            .format(self.hostCapable, self.deviceCapable, self.prodTypeDFP, self.prodTypeUFP, self.usbVendorID,
                    self.usbProdID, self.BCDDevice, self.SVID0, self.SVID1)
        return info


class DPAltModeSupport:

    def __init__(self):
        self.supportDP1_3 = None
        self.supportUSBgen2 = None
        self.DFP_D = None
        self.UFP_D = None

    def print_info(self):
        info = "DP Alt Mode support\n" \
               "Supports Dp v1.3:           {}\n" \
               "Supports USB gen2:          {}\n" \
               "Pin Assignment supported\n" \
               "- DFP_D:                    {}\n" \
               "- UFP_D:                    {}\n".\
            format(self.supportDP1_3, self.supportUSBgen2, self.DFP_D, self.UFP_D)
        return info


class TEDPAltModeStatus:

    def __init__(self):
        self.teStatus = None
        self.teMultifuncPrefered = None  # TSI_VR_PDC_DPAM_CAPS2
        self.teHPDState = None
        self.selectDP1_3 = None
        self.selectUSBgen2 = None
        self.pins = None

    def print_info(self):
        info = "TE DP Alt Mode Status\n" \
               "Status:                     {}\n" \
               "Multi-function preferred:   {}\n" \
               "HPD state:                  {}\n" \
               "Select DP v1.3:             {}\n" \
               "Select USB gen2:            {}\n" \
               "Pin Assignment:             {}\n"\
            .format(self.teStatus, self.teMultifuncPrefered, self.teHPDState, self.selectDP1_3, self.selectUSBgen2,
                    self.pins)
        return info


class DUTDpAltModeStatus:

    def __init__(self):
        self.status = None
        self.multifuncPrefered = None
        self.HPDState = None
        self.powerLow = None

    def print_info(self):
        info = "DUT DP Alt Mode Status\n" \
               "Status:                     {}\n" \
               "Multi-function preferred:   {}\n" \
               "HPD state:                  {}\n" \
               "Power Low:                  {}\n".\
            format(self.status, self.multifuncPrefered, self.HPDState, self.powerLow)
        return info


class USBCStatus:

    def __init__(self):
        self.plugged = None
        self.orientation = None
        self.unigrafCable = None
        self.status = Status()
        self.dutStatus = DUTStatus()
        self.pdContract = PDContract()
        self.busElectricalStatus = BusElectricalStatus()
        self.dutDiscovery = DUTDiscovery()
        self.dpAltModeSupport = DPAltModeSupport()
        self.teDpAltModeStatus = TEDPAltModeStatus()
        self.dutDpAltModeStatus = DUTDpAltModeStatus()

    def get_info_about_class(self):
        return self.plugged, self.orientation, self.unigrafCable, [self.status.__dict__, self.dutStatus.__dict__,
                                                                   self.pdContract.__dict__,
                                                                   self.busElectricalStatus.__dict__,
                                                                   self.dutDiscovery.__dict__,
                                                                   self.dpAltModeSupport.__dict__,
                                                                   self.teDpAltModeStatus.__dict__,
                                                                   self.dutDpAltModeStatus.__dict__]

    def print_info(self):
        info = "Status Info" \
               "Plugged:        {}\n" \
               "Orientation:    {}\n" \
               "Unigraf cable:  {}\n" \
               "{}{}{}{}{}{}{}{}" \
            .format(self.plugged, self.orientation, self.unigrafCable, self.status.print_info(),
                    self.dutStatus.print_info(), self.pdContract.print_info(), self.busElectricalStatus.print_info(),
                    self.dutDiscovery.print_info(), self.dpAltModeSupport.print_info(),
                    self.teDpAltModeStatus.print_info(), self.dutDpAltModeStatus.print_info())
        print(info)


class StatusForm:

    def __init__(self, device):
        self.device = device

    def usbc_get_pdc_type(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_PDC_TYPE_R, c_int32)
        return result[1]

    def usbc_set_cable_control(self, command: int):

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_W_USBC_CABLE_CONTROL, command, c_int32)

    def usbc_set_pdc_control(self, command: int):

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_PDC_CONTROL, command, c_int32)

    def usbc_set_pdc_hw_control(self, command: int):

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_PDC_HW_CTRL, command, c_int32)

    def usbc_reconnect(self):

        result = self.usbc_get_pdc_type()

        if result == 2:
            self.usbc_set_pdc_control(0x0A)
        else:
            self.usbc_set_pdc_hw_control(0x16)

    def usbc_detach(self):

        self.usbc_set_cable_control(6)

    def usbc_set_reject_dr_swap(self, value: bool):

        command = 0x22 if value else 0x23
        self.usbc_set_pdc_control(command)

    def usbc_set_reject_pr_swap(self, value: bool):

        command = 0x20 if value else 0x21
        self.usbc_set_pdc_control(command)

    def usbc_set_reject_vconn_swap(self, value: bool):

        command = 0x1e if value else 0x1f
        self.usbc_set_pdc_control(command)

    def usbc_set_toggle_audio_accessory(self, value: bool):

        command = 0x27 if value else 0x26
        self.usbc_set_pdc_control(command)

    def usbc_set_toggle_debug_accessory(self, value: bool):

        command = 0x25 if value else 0x24
        self.usbc_set_pdc_control(command)

    def usbc_get_cable_status(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_USBC_CABLE_STATUS, c_uint32)
        assert result[0] >= TSI_SUCCESS
        return result[1]

    def usbc_get_role_status(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_USBC_ROLE_STATUS, c_uint32)
        assert result[0] >= TSI_SUCCESS
        return result[1]

    def usbc_get_pdo_source_data(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_USBC_POWER_SOURCE_PDO, c_int32)
        return result[1]

    def usbc_get_rdo_sink_data(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_USBC_POWER_SINK_RDO, c_int32)
        return result[1]

    def usbc_get_bus_electrical_status(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_ADC_VBUS_VOLTAGE, c_int32,
                                       TSI_R_USBC_ADC_BLOCK_SIZE)
        return result[1]

    def usbc_get_current_bus_electrical_status(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_ADC_VBUS_CURRENT, c_int32)

        return result[1]

    def usbc_get_voltage_on_cc1(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_ADC_VCC1_VOLTAGE, c_int32)

        return result[1]

    def usbc_get_voltage_on_cc2(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_ADC_VCC2_VOLTAGE, c_int32)

        return result[1]

    def usbc_get_vconn_voltage(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_ADC_VCONN_VOLTAGE, c_int32)

        return result[1]

    def usbc_get_vconn_current(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_ADC_VCONN_CURRENT, c_int32)

        return result[1]

    def usbc_get_id_vdo(self):

        try:
            cnt = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_PDC_RX_ID_VDO_CNT_R, c_int32)
            assert cnt[0] >= TSI_SUCCESS and cnt[1] >= 1 and ((self.usbc_get_cable_status() & 4) != 0)
            result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_PDC_RX_ID_VDO_RW, c_int8, cnt[1] * 4)
            assert result[0] >= TSI_SUCCESS
            vdos = [0 for i in range(cnt[1])]
            for i in range(0, cnt[1] * 4, 4):
                vdos[i // 4] = (
                        result[1][i] + (result[1][i + 1] << 8) + (result[1][i + 2] << 16) + (result[1][i + 3] << 24))
                if vdos[i // 4] < 0:
                    vdos[i // 4] += (1 << 32)
            return cnt[1], vdos
        except AssertionError:
            return -1, -1

    def usbc_get_svid(self):

        try:
            cnt = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_PDC_RX_SVID_CNT_R, c_int32)
            assert cnt[0] >= TSI_SUCCESS and cnt[1] >= 1
            result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_PDC_RX_SVID_RW, c_int32, cnt[1] * 4)
            assert result[0] >= TSI_SUCCESS
            svids = []
            for i in range(0, cnt[1] * 4, 4):
                svids.append(
                    result[1][i] + (result[1][i + 1] << 8) + (result[1][i + 2] << 16) + (result[1][i + 3] << 24))
                if svids[i // 4] < 0:
                    svids[i // 4] += (1 << 32)
            return cnt[1], svids
        except AssertionError:
            return -1, -1

    def usbc_get_dp_alt_mode_support(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_PDC_DPAM_DISC_MODES_R, c_int32)
        assert result[0] >= TSI_SUCCESS
        return result[1]

    def usbc_get_dp_alt_mode_status(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_USBC_DP_ALT_MODE_STATUS, c_uint32)

        return result[1]

    def usbc_get_dut_alt_mode_status(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_PDC_DPAM_RECV_STS_R, c_int32)

        return result[1]

    def usbc_get_pd_status(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_USBC_PD_STATUS, c_int32)
        return result[1]

    def usbc_get_data_role(self):
        return int(self.usbc_get_role_status() & 1)

    def usbc_get_power_role(self):
        return int(self.usbc_get_role_status() & 2)

    def usbc_get_vconn_status(self):
        return int(self.usbc_get_role_status() & 4)

    def usbc_get_status_all_info(self) -> USBCStatus:

        usbc_status = USBCStatus()

        cable_status = self.usbc_get_cable_status()
        usbc_status.plugged = (cable_status & 1) != 0
        usbc_status.orientation = (cable_status & 2) != 0
        usbc_status.unigrafCable = (cable_status & 16) != 0

        usbc_status.status.statusDataRole = self.usbc_get_data_role()
        usbc_status.status.statusPowerRole = self.usbc_get_power_role()
        usbc_status.status.statusVconn = self.usbc_get_vconn_status()

        usbc_status.dutStatus.dutDataRole = not usbc_status.status.statusDataRole
        usbc_status.dutStatus.dutPowerRole = not usbc_status.status.statusPowerRole
        usbc_status.dutStatus.dutVconn = not usbc_status.status.statusVconn

        pdo = self.usbc_get_pdo_source_data()
        rdo = self.usbc_get_rdo_sink_data()
        usbc_status.pdContract.PDOType = ((pdo >> 30) & 3)
        usbc_status.pdContract.PDOVoltage = ((pdo >> 10) & 0x3FF) * 0.05
        usbc_status.pdContract.PDOMaxCurr = ((pdo & 0x3FF) * 0.01)
        usbc_status.pdContract.RDOMaxCurr = ((rdo & 0x3FF) * 0.01)
        usbc_status.pdContract.RDOOperCurr = ((rdo >> 10) & 0x3FF) * 0.01
        usbc_status.pdContract.usbSuspend = (rdo >> 24) & 1
        usbc_status.pdContract.usbCommCapable = ((rdo >> 25) & 1)
        usbc_status.pdContract.capMismatch = ((rdo >> 26) & 1)
        usbc_status.pdContract.giveBack = ((rdo >> 27) & 1)

        bus_status = self.usbc_get_bus_electrical_status()
        usbc_status.busElectricalStatus.vbusVoltage = bus_status[0] / 1000.0
        usbc_status.busElectricalStatus.vbusCurrent = bus_status[1] / 1000.0
        usbc_status.busElectricalStatus.cc1Voltage = bus_status[2] / 1000.0
        usbc_status.busElectricalStatus.cc2Voltage = bus_status[3] / 1000.0
        usbc_status.busElectricalStatus.vconnVoltage = bus_status[4] / 1000.0
        usbc_status.busElectricalStatus.vconnCurrent = bus_status[5] / 1000.0
        usbc_status.busElectricalStatus.sbu1Voltage = bus_status[6] / 1000.0
        usbc_status.busElectricalStatus.sbu2Voltage = bus_status[7] / 1000.0

        cnt, vdo = self.usbc_get_id_vdo()
        if cnt != -1:
            usbc_status.dutDiscovery.cnt = cnt
            usbc_status.dutDiscovery.vdo = vdo
            usbc_status.dutDiscovery.hostCapable = ((vdo[0] >> 31) & 1)
            usbc_status.dutDiscovery.deviceCapable = ((vdo[0] >> 30) & 1)
            usbc_status.dutDiscovery.prodTypeDFP = ((vdo[0] >> 23) & 7)
            usbc_status.dutDiscovery.prodTypeUFP = ((vdo[0] >> 27) & 7)
            usbc_status.dutDiscovery.usbVendorID = vdo[0] & 0xFFFF
            if cnt >= 3:
                usbc_status.dutDiscovery.usbProdID = vdo[2] >> 16
                usbc_status.dutDiscovery.BCDDevice = vdo[2] & 0xFFFF

        cnt, svid = self.usbc_get_svid()
        if cnt != -1:
            usbc_status.dutDiscovery.SVID0 = svid[0] & 0xFFFF
            usbc_status.dutDiscovery.SVID1 = svid[0] >> 16

        dp_alt_mode_sup = self.usbc_get_dp_alt_mode_support()
        usbc_status.dpAltModeSupport.supportDP1_3 = ((dp_alt_mode_sup >> 2) & 1)
        usbc_status.dpAltModeSupport.supportUSBgen2 = ((dp_alt_mode_sup >> 2) & 2)
        usbc_status.dpAltModeSupport.UFP_D = dp_alt_mode_sup & 1
        usbc_status.dpAltModeSupport.DFP_D = dp_alt_mode_sup & 2

        dp_alt_mode_status = self.usbc_get_dp_alt_mode_status()
        sig_data = ((dp_alt_mode_status >> 3) & 0x0F)
        usbc_status.teDpAltModeStatus.teStatus = ((dp_alt_mode_status & 1) != 0)
        usbc_status.teDpAltModeStatus.teHPDState = 1 & self.usbc_get_cable_status()
        usbc_status.teDpAltModeStatus.selectDP1_3 = sig_data & 1
        usbc_status.teDpAltModeStatus.selectUSBgen2 = sig_data & 2
        usbc_status.teDpAltModeStatus.pins = 7 if ((dp_alt_mode_status >> 8) & 0x0F) > 7 else \
            ((dp_alt_mode_status >> 8) & 0x0F)

        dut_alt_mode_status = self.usbc_get_dut_alt_mode_status()
        usbc_status.dutDpAltModeStatus.status = dut_alt_mode_status & 0x03
        if usbc_status.dutDpAltModeStatus.status:
            usbc_status.dutDpAltModeStatus.multifuncPrefered = (dut_alt_mode_status >> 4) & 1
            usbc_status.dutDpAltModeStatus.HPDState = 1 & self.usbc_get_cable_status()
            usbc_status.dutDpAltModeStatus.powerLow = not ((dut_alt_mode_status >> 2) & 1)

        return usbc_status
