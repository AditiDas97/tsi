from .modules.PDC.pdc import *
from .modules.Capture.capture_usbc import *


class USBC:

    def __init__(self, device):
        """

        General class for USBC device. Contain common methods for USBC devices.

        The class contains the following fields:
        pdc - Object of Pdc class. Contain general methods for interacting with PDC.
        capturer - Object of CapturerHdRx class. Needed to capture, downloading and saving events and video frames.

        Parameters
        ----------
        device : TSIDevice
            Indicates the device on which the operation is to be carried out

        """

        self._device = device
        self._pdc = Pdc(self._device)
        self._capture = CapturerUsbc(self._device)

    # Capabilities Block
    def usbc_get_pdc_state(self) -> int:
        """

        Return info of PDC state system.

        Returns
        -------
        result : int
            PDC state

        """
        return self._pdc.capabilities.usbc_get_pdc_state()

    def usbc_get_initial_role(self) -> int:
        """

        Return info of USBC initial role:
            0 - InitialRoleUFP
            1 - InitialRoleDFP
            2 - InitialRoleDRP

        Returns
        -------
        result : int
            Initial role

        """
        return self._pdc.capabilities.usbc_get_initial_role()

    def usbc_get_cc_pull_up(self) -> int:
        """

        Return info of CC pull up state:
            0 - CCPullUpDefault
            1 - CCPullUp_1_5
            2 - CCPullUp_3_0

        Returns
        -------
        result : int
            PDC state

        """
        return self._pdc.capabilities.usbc_get_cc_pull_up()

    def usbc_get_reject_dr_swap(self) -> bool:
        """

        Return state of DR_Swap message processing:
            True - enabled
            False - disabled

        Returns
        -------
        result : bool
            State

        """
        return self._pdc.capabilities.usbc_get_reject_dr_swap()

    def usbc_get_reject_pr_swap(self) -> bool:
        """

        Return state of PR_Swap message processing:
            True - enabled
            False - disabled

        Returns
        -------
        result : bool
            State

        """
        return self._pdc.capabilities.usbc_get_reject_pr_swap()

    def usbc_get_reject_vconn_swap(self) -> bool:
        """

        Return state of VCONN_Swap message processing:
            True - enabled
            False - disabled

        Returns
        -------
        result : int
            State

        """
        return self._pdc.capabilities.usbc_get_reject_vconn_swap()

    def usbc_get_reject_fr_swap(self) -> bool:
        """

        Return state of FR_Swap message processing:
            True - enabled
            False - disabled

        Returns
        -------
        result : int
            State

        """
        return self._pdc.capabilities.usbc_get_reject_fr_swap()

    def usbc_get_audio_accessory(self) -> bool:
        """

        Return state of Audio accessory support:
            True - enabled
            False - disabled

        Returns
        -------
        result : int
            State

        """
        return self._pdc.capabilities.usbc_get_audio_accessory()

    def usbc_get_debug_accessory(self) -> bool:
        """

        Return state of Debug accessory support:
            True - enabled
            False - disabled

        Returns
        -------
        result : int
            State

        """
        return self._pdc.capabilities.usbc_get_debug_accessory()

    def usbc_get_try_behavior(self) -> int:
        """

        Return info of DRP try mode:
            0 - TryBehaviorNONE
            1 - TryBehaviorSNK
            2 - TryBehaviorSRC
            3 - TryBehaviorRESERVED

        Returns
        -------
        result : int
            Mode

        """
        return self._pdc.capabilities.usbc_get_try_behavior()

    def usbc_get_pdc_caps(self) -> int:
        """

        Return Power delivery controller capabilities.

        Returns
        -------
        result : int
            Capabilities

        """
        return self._pdc.capabilities.usbc_get_pdc_caps()

    def usbc_get_try_behavior_snk(self) -> bool:
        """

        Return state of PD Controller supported Try.SNK Feature.
            True - supported
            False - not supported

        Returns
        -------
        result : bool
            State
        """
        return self._pdc.capabilities.usbc_get_try_behavior_snk()

    def usbc_get_try_behavior_src(self) -> bool:
        """

        Return state of PD Controller supported Try.SRC Feature.
            True - supported
            False - not supported

        Returns
        -------
        result : bool
            State
        """
        return self._pdc.capabilities.usbc_get_try_behavior_src()

    def usbc_get_fr_swap(self) -> bool:
        """

        Return state of PD Controller supported Fast Role Swap.
            True - supported
            False - not supported

        Returns
        -------
        result : bool
            State
        """
        return self._pdc.capabilities.usbc_get_fr_swap()

    def usbc_get_cable_sim(self) -> bool:
        """

        Return state of PD Controller supported Cable Simulation.
            True - supported
            False - not supported

        Returns
        -------
        result : bool
            State
        """
        return self._pdc.capabilities.usbc_get_cable_sim()

    def usbc_get_hw_status(self) -> int:
        """

        Return current hardware status.

        Returns
        -------
        result : int
            Status
        """
        return self._pdc.capabilities.usbc_get_hw_status()

    def usbc_get_usb_2_bypass(self) -> bool:
        """

        Return state of USB 2.0 PHY:
            True - enabled
            False - disabled

        Returns
        -------
        result : bool
            Status

        """
        return self._pdc.capabilities.usbc_get_usb_2_bypass()

    def usbc_get_usb_3_bypass(self) -> bool:
        """

        Return state of USB 3.0 PHY:
            True - enabled
            False - disabled

        Returns
        -------
        result : bool
            Status

        """
        return self._pdc.capabilities.usbc_get_usb_3_bypass()

    def usbc_get_capability_info(self) -> CapabilitiesInfo:
        """

        Return the object of CapabilitiesInfo class. It contains information about device capabilities.

        Available info:
            initialRole - info of USBC initial role (type: int)
            rejectPR_Swap - state of PR_Swap message processing (type: bool)
            rejectDR_Swap - state of DR_Swap message processing (type: bool)
            rejectFR_Swap - state of FR_Swap message processing (type: bool)
            rejectVconnSwap - state of Vconn_Swap message processing (type: bool)
            audioAccessory - state of Audio accessory support (type: bool)
            debugAccessory - state of Debug accessory support (type: bool)
            ccPullUp - info of CC pull up state (type: int)
            tryBehavior - info of DRP try mode (type: int)
            tryBehaviorSNK - state of PD Controller supported Try.SNK Feature (type: bool)
            tryBehaviorSRC - state of PD Controller supported Try.SRC Feature (type: bool)
            FRSwap - state of PD Controller supported Fast Role Swap (type: bool)
            CableSim - state of PD Controller supported Cable Simulation (type: bool)
            usb2Bypass - state of USB 2.0 PHY (type: bool)
            usb3Bypass - state of USB 3.0 PHY (type: bool)

        Returns
        -------
        result : CapabilitiesInfo
            Device capabilities

        """
        return self._pdc.capabilities.usbc_get_capability_info()

    def usbc_set_initial_role(self, command: int):
        """

        Used to control initial role settings and related configuration.

        Parameters
        ----------
        command : int
            Control command

        """
        self._pdc.capabilities.usbc_set_initial_role(command)

    def usbc_set_initial_role_ufp(self):
        """

        Set UFP initial role.

        """
        self._pdc.capabilities.usbc_set_initial_role_ufp()

    def usbc_set_initial_role_dfp(self):
        """

        Set DFP initial role.

        """
        self._pdc.capabilities.usbc_set_initial_role_dfp()

    def usbc_set_initial_role_drp(self):
        """

        Set DRP initial role.

        """
        self._pdc.capabilities.usbc_set_initial_role_drp()

    def usbc_set_pwr_command(self, command: int):
        """

        Used to write pending Power Data Objects (PDO’s) in USB-C enabled devices.

        Parameters
        ----------
        command : int
            Control command

        """
        self._pdc.usbc_set_pwr_command(command)

    def usbc_set_source_power_objects(self):
        """

        Write Power source data objects to device.

        """
        self._pdc.usbc_set_source_power_objects()

    def usbc_set_sink_power_objects(self):
        """

        Write Power sink data objects to device.

        """
        self._pdc.usbc_set_sink_power_objects()

    # Controls Block
    def usbc_get_pwr_contract_control(self) -> int:
        """

        Return current power contract control.

        Returns
        -------
        result : int
            Power contract
        """
        return self._pdc.controls.usbc_get_pwr_contract_control()

    def usbc_set_pwr_contract_control(self, data: int):
        """

        Set power contract control.

        Parameters
        ----------
        data : int
            Power contract
        """
        self._pdc.controls.usbc_set_pwr_contract_control(data)

    def usbc_get_data_role(self) -> int:
        """

        Return current device data role

        Returns
        -------
        result : int
            0 - Up Facing Port (UFP)
            1 - Down Facing Port (DFP)
        """
        return self._pdc.status.usbc_get_data_role()

    def usbc_get_power_role(self) -> int:
        """

        Return current device power role

        Returns
        -------
        result : int
            0 - Source
            1 - Sink
        """
        return self._pdc.status.usbc_get_power_role()

    def usbc_get_vconn_status(self) -> int:
        """

        Return current device VCONN status.

        Returns
        -------
        result : bool
            0 - Off
            1 - On
        """
        return self._pdc.status.usbc_get_vconn_status()

    def usbc_get_auto_negotiate_pc(self) -> int:
        """

        Return state of Auto negotiate flag.

        Returns
        -------
        result : int
            0 - Don’t auto-negotiate
            1 - Automatically negotiate power contract
        """
        return self._pdc.controls.usbc_get_auto_negotiate_pc()

    def usbc_get_use_battery_PDO(self) -> int:
        """

        Return state of use battery PDO.

        Returns
        -------
        result : int
            0 - Don’t use battery PDO for power contract
            1 - Use battery PDO for power contract negotiation

        """
        return self._pdc.controls.usbc_get_use_battery_PDO()

    def usbc_get_use_variable_PDO(self) -> int:
        """

        Return state of use variable PDO.

        Returns
        -------
        result : int
            0 - Don’t use variable PDO for power contract
            1 - Use variable PDO for power contract negotiation

        """
        return self._pdc.controls.usbc_get_use_variable_PDO()

    def usbc_get_contract_preference(self) -> int:
        """

        Return info of contract preference.

        Returns
        -------
        result : int
            0 - Prefer higher 'current' power contract
            1 - Prefer higher 'voltage' power contract
            2 - Prefer higher 'power' power contract

        """
        return self._pdc.controls.usbc_get_contract_preference()

    def usbc_get_rdo_no_usb_suspend(self) -> int:
        """

        Return state of No usb suspend flag.

        Returns
        -------
        result : int
            State of flag

        """
        return self._pdc.controls.usbc_get_rdo_no_usb_suspend()

    def usbc_get_rdo_give_back_flag(self) -> int:
        """

        Return state of give back flag.

        Returns
        -------
        result : int
            State of flag

        """
        return self._pdc.controls.usbc_get_rdo_give_back_flag()

    def usbc_get_auto_min_power(self) -> int:
        """

        Return state of automatic minimum power.

        Returns
        -------
        result : int
            0 - Don’t calculate minimum power
            1 - Automatically calculate minimum required power

        """
        return self._pdc.controls.usbc_get_auto_min_power()

    def usbc_get_manual_power_contract_selection(self) -> int:
        """

        Return info of manual power contract selection.

        Returns
        -------
        result : int
            0 - Auto-negotiate power contract
            1 - Power contract selected by index

        """
        return self._pdc.controls.usbc_get_manual_power_contract_selection()

    def usbc_get_min_power(self) -> int:
        """

        Return minimum required power.

        Returns
        -------
        result : int
            Power
        """
        return self._pdc.controls.usbc_get_min_power()

    def usbc_get_cable_diff_pairs_usb2(self):
        """

        Return info of cable E-Marking.

        Returns
        -------
        result : int
            1 - Unmarked cable is attached
            2 - E-Marked cable is attached

        """
        return self._pdc.controls.usbc_get_cable_diff_pairs_usb2()

    def usbc_get_controls_info(self) -> ControlsInfo:
        """

        Return the object of ControlsInfo class. It contains information about device controls.

        Available info:
            autoNegotiatePowerContract - state of Auto negotiate flag (type: int)
            rdoGiveBackFlag - state of give back flag (type: int)
            rdoNoUSBSuspend - state of No usb suspend flag (type: int)
            autoMinPower - state of automatic minimum power (type: int)
            minPower - value of minimum required power (type: int)
            cableDiffPairsUSB2 - info of cable E-Marking (type: int)
            externallyPowered - info of externally powered (will be returned False) (type: bool)
            capPDSource - info of capability PD Source (will be returned True) (type: bool)
            capPDSink - info of capability PD Sink (will be returned True) (type: bool)

        Returns
        -------
        result : ControlsInfo
            Device controls info

        """
        return self._pdc.controls.usbc_get_controls_info()

    def usbc_get_pdo_count(self) -> int:
        """

        Return count of PDO backed with hardware.

        Returns
        -------
        result : int
            PDO count

        """
        return self._pdc.controls.usbc_get_pdo_count()

    def usbc_set_pwr_contract_select(self, number: int):
        """

        Set number of PDO is used to establish the power contract with link partner.

        Parameters
        ----------
        number : int
            PDO number

        """
        self._pdc.controls.usbc_set_pwr_contract_select(number)

    def usbc_set_priority_and_index(self, selected_by_index: bool, index: int, priority: int):
        """

        Set priority and index of PDO which will be used.

        Parameters
        ----------
        selected_by_index : bool
            Flag of selected PDO by index: True or False
        index : int
            PDO index
        priority : int
            PDO priority

        """
        self._pdc.controls.usbc_set_priority_and_index(selected_by_index, index, priority)

    def usbc_set_local_sink_pdo_select(self, number: int):
        """

        Used to select the sink Power Data Object (PDO) by number: 0-6 (It depends on the device).

        Parameters
        ----------
        number : int
            Number of PDO
        """
        self._pdc.controls.usbc_set_local_sink_pdo_select(number)

    def usbc_set_local_sink_pdo_type(self, value: int):
        """

        Set type of the sink Power Data Object (PDO).
        Types:
            0 - Disabled PDO
            1 - Fixed PDO
            2 - Variable PDO
            3 - Battery PDO

        Parameters
        ----------
        value : int
            Type of PDO

        """
        self._pdc.controls.usbc_set_local_sink_pdo_type(value)

    def usbc_set_local_sink_pdo_max_current(self, value: int):
        """

        Set max current of the sink Power Data Object (PDO).

        Parameters
        ----------
        value : int
            Max current

        """
        self._pdc.controls.usbc_set_local_sink_pdo_max_current(value)

    def usbc_set_local_sink_pdo_voltage(self, value: int):
        """

        Set voltage of the sink Power Data Object (PDO).

        Parameters
        ----------
        value : int
            Voltage

        """
        self._pdc.controls.usbc_set_local_sink_pdo_voltage(value)

    def usbc_set_local_sink_pdo_fixed_bits(self, value: int):
        """

        Set fixed bits of the sink Power Data Object (PDO).

        Parameters
        ----------
        value : int
            Fixed bits

        """
        self._pdc.controls.usbc_set_local_sink_pdo_fixed_bits(value)

    def usbc_set_local_sink_pdo_max_voltage(self, value: int):
        """

        Set max voltage of the sink Power Data Object (PDO).

        Parameters
        ----------
        value : int
            Max voltage

        """
        self._pdc.controls.usbc_set_local_sink_pdo_max_voltage(value)

    def usbc_set_local_sink_pdo_min_voltage(self, value: int):
        """

        Set min voltage of the sink Power Data Object (PDO).

        Parameters
        ----------
        value : int
            Min voltage

        """
        self._pdc.controls.usbc_set_local_sink_pdo_min_voltage(value)

    def usbc_set_local_sink_pdo_max_power(self, value: int):
        """

        Set max power of the sink Power Data Object (PDO).

        Parameters
        ----------
        value : int
            Max power

        """
        self._pdc.controls.usbc_set_local_sink_pdo_max_power(value)

    def usbc_set_local_source_pdo_select(self, number: int):
        """

        Used to select the source Power Data Object (PDO) by number: 0-6 (It depends on the device).

        Parameters
        ----------
        number : int
            Number of PDO
        """
        self._pdc.controls.usbc_set_local_source_pdo_select(number)

    def usbc_set_local_source_pdo_type(self, value: int):
        """

        Set type of the source Power Data Object (PDO).
        Types:
            0 - Disabled PDO
            1 - Fixed PDO
            2 - Variable PDO
            3 - Battery PDO

        Parameters
        ----------
        value : int
            Type of PDO

        """
        self._pdc.controls.usbc_set_local_source_pdo_type(value)

    def usbc_set_local_source_pdo_max_current(self, value: int):
        """

        Set max current of the source Power Data Object (PDO).

        Parameters
        ----------
        value : int
            Max current

        """
        self._pdc.controls.usbc_set_local_source_pdo_max_current(value)

    def usbc_set_local_source_pdo_voltage(self, value: int):
        """

        Set voltage of the source Power Data Object (PDO).

        Parameters
        ----------
        value : int
            Voltage

        """
        self._pdc.controls.usbc_set_local_source_pdo_voltage(value)

    def usbc_set_local_source_pdo_peak_current(self, value: int):
        """

        Set peak current of the source Power Data Object (PDO).

        Parameters
        ----------
        value : int
            Peak current

        """
        self._pdc.controls.usbc_set_local_source_pdo_peak_current(value)

    def usbc_set_local_source_pdo_fixed_bits(self, value: int):
        """

        Set fixed bits of the source Power Data Object (PDO).

        Parameters
        ----------
        value : int
            Fixed bits

        """
        self._pdc.controls.usbc_set_local_source_pdo_fixed_bits(value)

    def usbc_set_local_source_pdo_max_voltage(self, value: int):
        """

        Set max voltage of the source Power Data Object (PDO).

        Parameters
        ----------
        value : int
            Max voltage

        """
        self._pdc.controls.usbc_set_local_source_pdo_max_voltage(value)

    def usbc_set_local_source_pdo_min_voltage(self, value: int):
        """

        Set min voltage of the source Power Data Object (PDO).

        Parameters
        ----------
        value : int
            Min voltage

        """
        self._pdc.controls.usbc_set_local_source_pdo_min_voltage(value)

    def usbc_set_local_source_pdo_max_power(self, value: int):
        """

        Set max power of the source Power Data Object (PDO).

        Parameters
        ----------
        value : int
            Max power

        """
        self._pdc.controls.usbc_set_local_source_pdo_max_power(value)

    # Cable info Block
    def usbc_get_ido_table(self) -> list:
        """

        Return to Identity Data Objects (IDO) which are received from near cable
        plug as the reply to Discover Identity request.

        Returns
        -------
        result : list
            IDO info

        """
        return self._pdc.cable.usbc_get_ido_table()

    def usbc_get_cable_info_all_info(self) -> CableInfoStruct:
        """

        Return the object of CableInfoStruct class. It contains information from IDO table in a parsed version.

        Available info:
            vdo - info of VDO (type: str)
            vendorID - info of Vendor ID (type: int)
            modalOpSupported - flag of supported modal Op (type: bool)
            prodType - info of production type (type: int):
                Product Type (UFP):
                    0 - Undefined
                    1 - PDUSB Hub
                    2 - PDUSB Peripheral
                    5 - Alternate Mode Adapter (AMA)
                Product Type (Cable Plug):
                    3 - Passive cable
                    4 - Active cable
            asDevice - flag of USB Communications Capable as a USB Device (type: bool)
            asHost - flag of USB Communications Capable as USB Host (type: bool)
            xID - (type: int)
            bcdDevice - info of BCd Device (type: int)
            prodID - info of USB Product ID (type: int)
            superSpeed - info of USB SuperSpeed Signalling Support (type: int):
                0 - USB 2.0 only, no SuperSpeed support
                1 - USB 3.1 Gen1
                2 - USB 3.1 Gen1 and Gen2
            vbusThrough - info of VBUS through cable: False - No, True - Yes (type: bool)
            vbusCurrentCable - info of VBUS Current Handling Capability: 1 - 3A, 2 - 5A (type: int)
            ssrx2 - info of SSRX2 Directionality Support: False - Fixed, True - Configurable (type: bool)
            ssrx1 - info of SSRX2 Directionality Support: False - Fixed, True - Configurable (type: bool)
            sstx2 - info of SSRX2 Directionality Support: False - Fixed, True - Configurable (type: bool)
            sstx1 - info of SSRX2 Directionality Support: False - Fixed, True - Configurable (type: bool)
            terminationType - info cable termination type (type: int):
                0 - VCONN not required
                1 - VCONN required
            latency - info of Cable Latency (includes latency of electronics in Active Cable) (type: int)
            captive - info of USB Type-C plug to USB Type-A/B/C/Captive (type: int):
                0 - USB Type-A
                1 - USB Type-B
                2 - USB Type-C
                3 - Captive
            fwVersion - number of firmware version (type: int)
            hwVersion - number of hardware version (type: int)

        Returns
        -------
        result : CableInfoStruct
            CableInfoStruct info
        """
        return self._pdc.cable.usbc_get_cable_info_all_info()

    # Power Sink Block
    def usbc_set_local_sink_pdo(self, pdos: list):
        """

        Set sink Power Data Object (PDO).

        Parameters
        ----------
        pdos : list
            Sink PDOs
        """
        self._pdc.power_sink.usbc_set_local_sink_pdo(pdos)

    def usbc_get_local_sink_pdo(self) -> tuple:
        """

        Return sink Power Data Object (PDO).

        Returns
        -------
        result : tuple
            Sink PDO info

        """
        return self._pdc.power_sink.usbc_get_local_sink_pdo()

    def usbc_get_local_sink_pdo_all_info(self) -> PdoInfo:
        """

        Return the object of PdoInfo class. It contains information about sink local PDO.

        Available info:
            role - info of current device role: False - Sink, True - Source (type: bool)
            pdo_selected - info of PDO index (type: int)
            pdo_type - info of PDO type (type: int)
            voltage - info of PDO voltage (type: int)
            max_voltage - info of PDO max voltage (type: int)
            min_voltage - info of PDO min voltage (type: int)
            max_current - info of PDO max current (type: int)
            peak_current - info of PDO peak current (type: int)
            max_power - info of PDO max power (type: int)
            fixed_bits - info of PDO fixed buts (type: int)
            usb_suspend_supported - flag of USB suspend supported (type: bool)
            externally_powered - flag of externally powered (type: bool)
            usb_communications_capable - flag of usb communications capable (type: bool)
            dual_role_data - flag of device dual role (type: bool)
            unchunked_extended_messages_supported - flag of unchunked extended messages supported (type: bool)
            higher_capability - flag of higher capability (type: bool)

        Returns
        -------
        result : PdoInfo
           Local PDO info
        """
        return self._pdc.power_sink.usbc_get_local_sink_pdo_all_info()

    def usbc_get_ext_resistance_status(self) -> int:
        """

        Return currently enabled external resistance in mΩ (milliohms).
        Returns 0 if no resistance set.

        Returns
        -------
        result : int
            External resistance value
        """
        return self._pdc.power_sink.usbc_get_ext_resistance_status()

    def usbc_get_int_resistance_status(self) -> int:
        """

        Return currently enabled internal resistance in mΩ (milliohms).
        Returns 0 if no resistance set.

        Returns
        -------
        result : int
            Internal resistance value
        """
        return self._pdc.power_sink.usbc_get_int_resistance_status()

    def usbc_get_power_status(self) -> int:
        """

        Return current power status.

        Returns
        -------
        result : int
            Power status
        """
        return self._pdc.power_sink.usbc_get_power_status()

    def usbc_get_current_index_and_resistance(self, epsu: bool) -> tuple:
        """

        Return info of current PDO index and value from resistor.

        Parameters
        ----------
        epsu : bool
            Type of resistor: False - Internal, True - External

        Returns
        -------
        result : tuple
            Index and resistor value

        """
        return self._pdc.power_sink.usbc_get_current_index_and_resistance(epsu)

    def usbc_get_power_sink_all_info(self) -> PowerSinkInfo:
        """

        Return the object of PowerSinkInfo class. It contains information about Power Sink.

        Available info:
            unigrafExternalPowerSupply - flag of external power supply (type: bool)
            powerContractSelectedByIndex - flag of selected power contract by index (type: bool)
            powerContractSelect - index of selected power contract (type: int)
            priority - state of PDO priority (type: int)
            szPDOsSupported - count of available PDO on device (type: int)
            external - state of External resistor (type: int)
            internal - state of Internal resistor (type: int)
            pdos - list with available PDOs (type: PDO)

        Returns
        -------
        result : PowerSinkInfo
            Power sink info
        """
        return self._pdc.power_sink.usbc_get_power_sink_all_info()

    def usbc_get_remote_sink_pdo_all_info(self) -> PdoInfo:
        """

        Return the object of PdoInfo class. It contains information about sink remote PDO.

        Available info:
            role - info of current device role: False - Sink, True - Source (type: bool)
            pdo_selected - info of PDO index (type: int)
            pdo_type - info of PDO type (type: int)
            voltage - info of PDO voltage (type: int)
            max_voltage - info of PDO max voltage (type: int)
            min_voltage - info of PDO min voltage (type: int)
            max_current - info of PDO max current (type: int)
            peak_current - info of PDO peak current (type: int)
            max_power - info of PDO max power (type: int)
            fixed_bits - info of PDO fixed buts (type: int)
            usb_suspend_supported - flag of USB suspend supported (type: bool)
            externally_powered - flag of externally powered (type: bool)
            usb_communications_capable - flag of usb communications capable (type: bool)
            dual_role_data - flag of device dual role (type: bool)
            unchunked_extended_messages_supported - flag of unchunked extended messages supported (type: bool)
            higher_capability - flag of higher capability (type: bool)

        Returns
        -------
        result : PdoInfo
           Remote PDO info
        """
        return self._pdc.power_sink.usbc_get_remote_sink_pdo_all_info()

    def usbc_set_sink_pdos(self, pwr_sink: PowerSinkInfo, set_pdos: list):
        """

        Set list of PDOs. PowerSinkIndo description:
            Available info:
            unigrafExternalPowerSupply - flag of external power supply (type: bool)
            powerContractSelectedByIndex - flag of selected power contract by index (type: bool)
            powerContractSelect - index of selected power contract (type: int)
            priority - state of PDO priority (type: int)
            szPDOsSupported - count of available PDO on device (type: int)
            external - state of External resistor (type: int)
            internal - state of Internal resistor (type: int)
            pdos - list with available PDOs (type: PDO) (In this case - PDOs with default values)

        Parameters
        ----------
        pwr_sink : PowerSinkInfo
            Power sink info
        set_pdos : list
            Value (list) with PDO
        """
        self._pdc.power_sink.usbc_set_sink_pdos(pwr_sink, set_pdos)

    def usbc_set_sink_pdo(self, pdo: PDO):
        """

        Set one sink PDO. PDO class description:
            role - info of current device role: False - Sink, True - Source (type: bool)
            pdo_selected - info of PDO index (type: int)
            pdo_type - info of PDO type (type: int)
            voltage - info of PDO voltage (type: int)
            max_voltage - info of PDO max voltage (type: int)
            min_voltage - info of PDO min voltage (type: int)
            max_current - info of PDO max current (type: int)
            peak_current - info of PDO peak current (type: int)
            max_power - info of PDO max power (type: int)
            fixed_bits - info of PDO fixed buts (type: int)
            usb_suspend_supported - flag of USB suspend supported (type: bool)
            externally_powered - flag of externally powered (type: bool)
            usb_communications_capable - flag of usb communications capable (type: bool)
            dual_role_data - flag of device dual role (type: bool)
            unchunked_extended_messages_supported - flag of unchunked extended messages supported (type: bool)
            higher_capability - flag of higher capability (type: bool)

        Parameters
        ----------
        pdo : PDO
            Type of resistor: False - Internal, True - External
        """
        self._pdc.power_sink.usbc_set_sink_pdo(pdo)

    def usbc_set_load_resistor(self, resistor_type: int, value: int, type_of_call=1):
        """

        Set value to resistor.

        Parameters
        ----------
        resistor_type : int
            Type of resistor: 0 - Internal, 1 - External
        value : int
            Resistor value
        type_of_call : int
            Autoapply changes flag
        """
        self._pdc.power_sink.usbc_set_load_resistor(resistor_type, value, type_of_call)

    def usbc_disable_load_resistor(self):
        """

        Disable load resistor.

        """
        self._pdc.power_sink.usbc_disable_load_resistor()

    # Power Source Block
    def usbc_get_local_source_pdo(self) -> tuple:
        """

        Return source Power Data Object (PDO).

        Returns
        -------
        result : tuple
            Source PDO info

        """
        return self._pdc.power_source.usbc_get_local_source_pdo()

    def usbc_set_local_source_pdo(self, pdos: list):
        """

        Set source Power Data Object (PDO).

        Parameters
        ----------
        pdos : list
            Source PDOs
        """
        self._pdc.power_source.usbc_set_local_source_pdo(pdos)

    def usbc_get_local_source_pdo_all_info(self) -> PdoInfo:
        """

        Return the object of PdoInfo class. It contains information about source local PDO.

        Available info:
            role - info of current device role: False - Sink, True - Source (type: bool)
            pdo_selected - info of PDO index (type: int)
            pdo_type - info of PDO type (type: int)
            voltage - info of PDO voltage (type: int)
            max_voltage - info of PDO max voltage (type: int)
            min_voltage - info of PDO min voltage (type: int)
            max_current - info of PDO max current (type: int)
            peak_current - info of PDO peak current (type: int)
            max_power - info of PDO max power (type: int)
            fixed_bits - info of PDO fixed buts (type: int)
            usb_suspend_supported - flag of USB suspend supported (type: bool)
            externally_powered - flag of externally powered (type: bool)
            usb_communications_capable - flag of usb communications capable (type: bool)
            dual_role_data - flag of device dual role (type: bool)
            unchunked_extended_messages_supported - flag of unchunked extended messages supported (type: bool)
            higher_capability - flag of higher capability (type: bool)

        Returns
        -------
        result : PdoInfo
           Local PDO info
        """
        return self._pdc.power_source.usbc_get_local_source_pdo_all_info()

    def usbc_get_remote_source_pdo_all_info(self) -> PdoInfo:
        """

        Return the object of PdoInfo class. It contains information about source remote PDO.

        Available info:
            role - info of current device role: False - Sink, True - Source (type: bool)
            pdo_selected - info of PDO index (type: int)
            pdo_type - info of PDO type (type: int)
            voltage - info of PDO voltage (type: int)
            max_voltage - info of PDO max voltage (type: int)
            min_voltage - info of PDO min voltage (type: int)
            max_current - info of PDO max current (type: int)
            peak_current - info of PDO peak current (type: int)
            max_power - info of PDO max power (type: int)
            fixed_bits - info of PDO fixed buts (type: int)
            usb_suspend_supported - flag of USB suspend supported (type: bool)
            externally_powered - flag of externally powered (type: bool)
            usb_communications_capable - flag of usb communications capable (type: bool)
            dual_role_data - flag of device dual role (type: bool)
            unchunked_extended_messages_supported - flag of unchunked extended messages supported (type: bool)
            higher_capability - flag of higher capability (type: bool)

        Returns
        -------
        result : PdoInfo
           Remote PDO info
        """
        return self._pdc.power_source.usbc_get_remote_source_pdo_all_info()

    def usbc_set_source_pdos(self, pwr_source: PdoInfo, set_pdos: list):
        """

        Set list of PDOs. PowerSinkIndo description:
            Available info:
            unigrafExternalPowerSupply - flag of external power supply (type: bool)
            powerContractSelectedByIndex - flag of selected power contract by index (type: bool)
            powerContractSelect - index of selected power contract (type: int)
            priority - state of PDO priority (type: int)
            szPDOsSupported - count of available PDO on device (type: int)
            external - state of External resistor (type: int)
            internal - state of Internal resistor (type: int)
            pdos - list with available PDOs (type: PDO) (In this case - PDOs with default values)

        Parameters
        ----------
        pwr_source : PdoInfo
            Power sink info
        set_pdos : list
            Value (list) with PDO
        """
        self._pdc.power_source.usbc_set_source_pdos(pwr_source, set_pdos)

    def usbc_set_source_pdo(self, pdo: PDO):
        """

        Set one sink PDO. PDO class description:
            role - info of current device role: False - Sink, True - Source (type: bool)
            pdo_selected - info of PDO index (type: int)
            pdo_type - info of PDO type (type: int)
            voltage - info of PDO voltage (type: int)
            max_voltage - info of PDO max voltage (type: int)
            min_voltage - info of PDO min voltage (type: int)
            max_current - info of PDO max current (type: int)
            peak_current - info of PDO peak current (type: int)
            max_power - info of PDO max power (type: int)
            fixed_bits - info of PDO fixed buts (type: int)
            usb_suspend_supported - flag of USB suspend supported (type: bool)
            externally_powered - flag of externally powered (type: bool)
            usb_communications_capable - flag of usb communications capable (type: bool)
            dual_role_data - flag of device dual role (type: bool)
            unchunked_extended_messages_supported - flag of unchunked extended messages supported (type: bool)
            higher_capability - flag of higher capability (type: bool)

        Parameters
        ----------
        pdo : PDO
            Type of resistor: False - Internal, True - External
        """
        self._pdc.power_source.usbc_set_source_pdo(pdo)

    # DP Alt Mode Block
    def usbc_set_dp_alt_mode(self, te_role: bool, mode_type: str, autoenter=1):
        """

        Set DP Alt mode.

        Parameters
        ----------
        te_role : bool
            True - Sink
            False - Source
        mode_type : str
            'c' - 1
            'd' - 2
            'e' - 4
        autoenter : int
            Auto aplay flag (default = 1)
        """
        self._pdc.alt_mode.usbc_set_dp_alt_mode(te_role, mode_type, autoenter)

    def usbc_get_dp_alt_mode(self) -> int:
        """

        Return current DP Alt mode.

        Returns
        -------
        result : int
            DP Alt mode

        """
        return self._pdc.alt_mode.usbc_get_dp_alt_mode()

    def usbc_alt_mode_sink_enter_2_lanes_mode_d(self):
        """

        Set DP Alt enter 2 lanes mode 'D' on Sink side.

        """
        self._pdc.alt_mode.usbc_alt_mode_sink_enter_2_lanes_mode_d()

    def usbc_alt_mode_sink_enter_4_lanes_mode_c(self):
        """

        Set DP Alt enter 4 lanes mode 'C' on Sink side.

        """
        self._pdc.alt_mode.usbc_alt_mode_sink_enter_4_lanes_mode_c()

    def usbc_alt_mode_sink_enter_4_lanes_mode_e(self):
        """

        Set DP Alt enter 4 lanes mode 'C' on Sink side.

        """
        self._pdc.alt_mode.usbc_alt_mode_sink_enter_4_lanes_mode_e()

    def usbc_alt_mode_source_enter_2_lanes_mode_d(self):
        """

        Set DP Alt enter 2 lanes mode 'D' on Source side.

        """
        self._pdc.alt_mode.usbc_alt_mode_source_enter_2_lanes_mode_d()

    def usbc_alt_mode_source_enter_4_lanes_mode_c(self):
        """

        Set DP Alt enter 4 lanes mode 'C' on Source side.

        """
        self._pdc.alt_mode.usbc_alt_mode_source_enter_4_lanes_mode_c()

    def usbc_alt_mode_source_enter_4_lanes_mode_e(self):
        """

        Set DP Alt enter 4 lanes mode 'C' on Source side.

        """
        self._pdc.alt_mode.usbc_alt_mode_source_enter_4_lanes_mode_e()

    def usbc_alt_mode_exit(self):
        """

        Disable DP Alternate mode auto enter on cable plug.

        """
        self._pdc.alt_mode.usbc_alt_mode_exit()

    def usbc_alt_mode_command(self, value: int):
        self._pdc.alt_mode.usbc_alt_mode_command(value)

    def usbc_alt_mode_disable(self):
        """

        Disable DP Alt mode.

        """
        self._pdc.alt_mode.usbc_alt_mode_disable()

    def usbc_set_auto_enter(self, value: bool):
        """

        Set value for Auto enter flag.

        Parameters
        ----------
        value : bool
            Auto enter flag
        """
        self._pdc.alt_mode.usbc_set_auto_enter(value)

    def usbc_get_auto_enter(self) -> int:
        """

        Return current value for Auto enter flag.

        Returns
        -------
        result : int
            Auto enter flag
        """
        return self._pdc.alt_mode.usbc_get_auto_enter()

    def usbc_alt_mode_multi_function(self, value: bool):
        """

        Set Multi-function preference setting.

        Parameters
        ----------
        value : bool
            Multi-function flag

        """
        self._pdc.alt_mode.usbc_alt_mode_multi_function(value)

    def usbc_get_multi_function(self) -> int:
        """

        Return current value for Multi-function preference flag.

        Returns
        -------
        result : int
            Multi-function flag

        """
        return self._pdc.alt_mode.usbc_get_multi_function()

    def usbc_get_alt_mode_sink_enter_2_lanes_mode_d(self) -> bool:
        """

        Return current state of DP Alt enter 2 lanes mode 'D' on Sink side.

        Returns
        -------
        result : bool
            State

        """
        return self._pdc.alt_mode.usbc_get_alt_mode_sink_enter_2_lanes_mode_d()

    def usbc_get_alt_mode_sink_enter_4_lanes_mode_c(self) -> bool:
        """

        Return current state of DP Alt enter 4 lanes mode 'C' on Sink side.

        Returns
        -------
        result : bool
            State

        """
        return self._pdc.alt_mode.usbc_get_alt_mode_sink_enter_4_lanes_mode_c()

    def usbc_get_alt_mode_sink_enter_4_lanes_mode_e(self) -> bool:
        """

        Return current state of DP Alt enter 4 lanes mode 'E' on Sink side.

        Returns
        -------
        result : bool
            State

        """
        return self._pdc.alt_mode.usbc_get_alt_mode_sink_enter_4_lanes_mode_e()

    def usbc_get_alt_mode_source_enter_2_lanes_mode_d(self) -> bool:
        """

        Return current state of DP Alt enter 2 lanes mode 'D' on Source side.

        Returns
        -------
        result : bool
            State

        """
        return self._pdc.alt_mode.usbc_get_alt_mode_source_enter_2_lanes_mode_d()

    def usbc_get_alt_mode_source_enter_4_lanes_mode_c(self) -> bool:
        """

        Return current state of DP Alt enter 4 lanes mode 'C' on Source side.

        Returns
        -------
        result : bool
            State

        """
        return self._pdc.alt_mode.usbc_get_alt_mode_source_enter_4_lanes_mode_c()

    def usbc_get_alt_mode_source_enter_4_lanes_mode_e(self):
        """

        Return current state of DP Alt enter 4 lanes mode 'E' on Source side.

        Returns
        -------
        result : bool
            State

        """
        return self._pdc.alt_mode.usbc_get_alt_mode_source_enter_4_lanes_mode_e()

    # Status Block
    def usbc_get_pdc_type(self) -> int:
        """

        Return current PDC type.

        Returns
        -------
        result : bool
            PDC type

        """
        return self._pdc.status.usbc_get_pdc_type()

    def usbc_set_cable_control(self, command: int):
        """

        Set cable control.

        Parameters
        ----------
        command : int
            Cable control command

        """
        self._pdc.status.usbc_set_cable_control(command)

    def usbc_send_source_pdo(self):
        """

        Send source PDO command.

        """
        self._pdc.status.usbc_set_pdc_control(0x41)

    def usbc_set_pdc_control(self, command: int):
        """

        Set PDC control.

        Parameters
        ----------
        command : int
            PDC control command

        """
        self._pdc.status.usbc_set_pdc_control(command)

    def usbc_set_pdc_hw_control(self, command: int):
        """

        Set PDC hardware control.

        Parameters
        ----------
        command : int
            PDC hardware control command

        """
        self._pdc.status.usbc_set_pdc_hw_control(command)

    def usbc_reconnect(self):
        """

        Run reconnect.

        """
        self._pdc.status.usbc_reconnect()

    def usbc_detach(self):
        """

        Disconnect CC lines. The DUT will see this as cable unplugged

        """
        self._pdc.status.usbc_detach()

    def usbc_get_pd_status(self) -> int:
        """

        Return current status of the PD controller in USB-C enabled devices

        Returns
        -------
        result : int
            PD status

        """
        return self._pdc.status.usbc_get_pd_status()

    def usbc_get_cable_status(self) -> int:
        """

        Return current cable status.

        Returns
        -------
        result : int
            Cable status

        """
        return self._pdc.status.usbc_get_cable_status()

    def usbc_get_role_status(self) -> int:
        """

        Return current role status.

        Returns
        -------
        result : int
            Role status

        """
        return self._pdc.status.usbc_get_role_status()

    def usbc_get_pdo_source_data(self) -> int:
        """

        Return raw PDO source data.

        Returns
        -------
        result : int
            PDO source data

        """
        return self._pdc.status.usbc_get_pdo_source_data()

    def usbc_get_rdo_sink_data(self) -> int:
        """

        Return raw RDO sink data.

        Returns
        -------
        result : int
            RDO sink data

        """
        return self._pdc.status.usbc_get_rdo_sink_data()

    def usbc_get_bus_electrical_status(self) -> tuple:
        """

        Return bus electrical status.

        Returns
        -------
        result : tuple
            Bus electrical status

        """
        return self._pdc.status.usbc_get_bus_electrical_status()

    def usbc_get_current_bus_electrical_status(self) -> int:
        """

        Return current bus electrical status.

        Returns
        -------
        result : int
            Role status

        """
        return self._pdc.status.usbc_get_current_bus_electrical_status()

    def usbc_get_voltage_on_cc1(self) -> int:
        """

        Return current voltage on CC1 lane.

        Returns
        -------
        result : int
            Voltage

        """
        return self._pdc.status.usbc_get_voltage_on_cc1()

    def usbc_get_voltage_on_cc2(self) -> int:
        """

        Return current voltage on CC2 lane.

        Returns
        -------
        result : int
            Voltage

        """
        return self._pdc.status.usbc_get_voltage_on_cc2()

    def usbc_get_vconn_voltage(self) -> int:
        """

        Return current VCONN voltage.

        Returns
        -------
        result : int
            Voltage

        """
        return self._pdc.status.usbc_get_vconn_voltage()

    def usbc_get_vconn_current(self):
        """

        Return VCONN current.

        Returns
        -------
        result : int
            Current

        """
        return self._pdc.status.usbc_get_vconn_current()

    def usbc_get_id_vdo(self) -> tuple:
        """

        Return current ID VDO data.

        Returns
        -------
        result : int
            tuple

        """
        return self._pdc.status.usbc_get_id_vdo()

    def usbc_get_svid(self) -> tuple:
        """

        Return current SVID info.

        Returns
        -------
        result : int
            tuple

        """
        return self._pdc.status.usbc_get_svid()

    def usbc_get_dp_alt_mode_support(self) -> int:
        """

        Return DP Alt mode dpam disc modes support.

        Returns
        -------
        result : int
            State

        """
        return self._pdc.status.usbc_get_dp_alt_mode_support()

    def usbc_get_dp_alt_mode_status(self) -> int:
        """

        Return current status of PD Alt mode.

        Returns
        -------
        result : int
            Status

        """
        return self._pdc.status.usbc_get_dp_alt_mode_status()

    def usbc_get_dut_alt_mode_status(self) -> int:
        """

        Return current DUT status of PD Alt mode.

        Returns
        -------
        result : int
            Status

        """
        return self._pdc.status.usbc_get_dut_alt_mode_status()

    def usbc_get_status_all_info(self) -> USBCStatus:
        """

        Return full info of current USBC status.

        Available info:
            plugged - info of state cable: plugged or nor. (type: bool)
            orientation - info of cable orientation (type: bool)
            unigrafCable - state if unigraf cable (type: bool)
            status - object of Status class:
                statusDataRole - info of device data role (type: int)
                statusPowerRole - info of device power role (type: int)
                statusVconn - info of device vconn (type: int)
            dutStatus - object of DUTStatus:
                dutDataRole - info of DUT device data role (type: int)
                dutPowerRole - info of DUT device power role (type: int)
                dutVconn - info of DUT device vconn (type: int)
            pdContract - object of PDContract:
                PDOType - info of PDO type (type: int)
                PDOVoltage - info of PDO voltage (type: int)
                PDOMaxCurr - info of PDO Max current (type: int)
                RDOMaxCurr - info of RDO Max current (type: int)
                RDOOperCurr - info of RDO Oper current (type: int)
                usbSuspend - flag of USB suspend (type: bool)
                capMismatch - flag of capability mismatch (type: bool)
                usbCommCapable - flag of USB comm capable (type: bool)
                giveBack - flag of give back (type: bool)
            busElectricalStatus - object of BusElectricalStatus:
                vbusVoltage - info of vBus Voltage (type: int)
                vbusCurrent - info of vBus Current (type: int)
                cc1Voltage - info of Voltage on CC1 (type: int)
                cc2Voltage - info of Voltage on CC2 (type: int)
                vconnVoltage - info of VCONN Coltage (type: int)
                vconnCurrent - info of VCONN Current (type: int)
                sbu1Voltage - info of sbus1 Voltage (type: int)
                sbu2Voltage - info of sbus2 Voltage (type: int)
            dutDiscovery - object of DUTDiscovery:
                hostCapable - info of host capable (type: int)
                deviceCapable - info of device capable (type: int)
                prodTypeDFP - info of production type DFP (type: int)
                prodTypeUFP - info of production type UFP (type: int)
                usbVendorID - info of USB Vendor ID (type: int)
                usbProdID - info of USB Production ID (type: int)
                BCDDevice - info of DCD Device (type: int)
                SVID0 - info of SVID0 (type: int)
                SVID1 - info of SVID1 (type: int)
                vdo - list with VDO (type: list)
            dpAltModeSupport - object of DPAltModeSupport:
                supportDP1_3 - flag of support DP 1.3 (type: bool)
                supportUSBgen2 - flag of support USB generation 2 (type: bool)
                DFP_D - state of DFP role (type: bool)
                UFP_D - state of UFP role (type: bool)
            teDpAltModeStatus - object of TEDPAltModeStatus:
                teStatus - info of device DP Alt mode status (type: int)
                teHPDState - info of HDP state (type: bool)
                selectDP1_3 - flag of selected DP 1.3 (type: bool)
                selectUSBgen2 - flag of selected USB gen2
                pins Count of pins (type: int)
            dutDpAltModeStatus - object of DUTDpAltModeStatus:
                status - info of DUT DP Alt mode status (type: int)
                multifuncPrefered - flag of multi function prefered (type: bool)
                HPDState - info of HDP state (type: bool)
                powerLow - info of power low (type: bool)

        Returns
        -------
        result : USBCStatus
            USBC Status

        """
        return self._pdc.status.usbc_get_status_all_info()

    def usbc_set_reject_dr_swap(self, value: bool):
        """

        Enable or Disable DR_Swap message processing.

        Parameters
        ----------
        value : bool
            True - Enable
            False - Disable

        """
        self._pdc.status.usbc_set_reject_dr_swap(value)

    def usbc_set_reject_pr_swap(self, value: bool):
        """

        Enable or Disable PR_Swap message processing.

        Parameters
        ----------
        value : bool
            True - Enable
            False - Disable

        """
        self._pdc.status.usbc_set_reject_pr_swap(value)

    def usbc_set_reject_vconn_swap(self, value: bool):
        """

        Enable or Disable VCONN_Swap message processing.

        Parameters
        ----------
        value : bool
            True - Enable
            False - Disable

        """
        self._pdc.status.usbc_set_reject_vconn_swap(value)

    def usbc_set_toggle_audio_accessory(self, value: bool):
        """

        Enable or Disable Audio Accessory support.

        Parameters
        ----------
        value : bool
            True - Enable
            False - Disable

        """
        self._pdc.status.usbc_set_toggle_audio_accessory(value)

    def usbc_set_toggle_debug_accessory(self, value: bool):
        """

        Enable or Disable Debug Accessory support.

        Parameters
        ----------
        value : bool
            True - Enable
            False - Disable

        """
        self._pdc.status.usbc_set_toggle_debug_accessory(value)

    # PDC Block
    def usbc_set_role_control(self, command: int):
        """

        Set command to control port roles after cable is plugged into TE and roles are established.

        Parameters
        ----------
        command : int
            Command to control
        """
        self._pdc.usbc_set_role_control(command)

    def usbc_set_dr_swap(self):
        """

        Request swapping data role.

        """
        self._pdc.usbc_set_dr_swap()

    def usbc_set_pr_swap(self):
        """

        Request swapping power role.

        """
        self._pdc.usbc_set_pr_swap()

    def usbc_set_vconn_swap(self):
        """

        Request swapping Vconn.

        """
        self._pdc.usbc_set_vconn_swap()

    def usbc_set_fr_swap(self):
        """

        Clear “USB Communications capable” flag for PD Sink.

        """
        self._pdc.usbc_set_fr_swap()

    def usbc_send_orientation(self, value: bool):
        """

        Change device orientation.

        Parameters
        ----------
        value : bool
            True - Set initial port role to DFP.
            False - Set initial port role to UFP.

        """
        self._pdc.usbc_send_orientation(value)

    def usbc_enable_adc_data_scanner(self):
        """

        Enable ADC data scanner

        """
        self._pdc.usbc_enable_adc_data_scanner()

    def usbc_disable_adc_data_scanner(self):
        """

        Enable ADC data scanner

        """
        self._pdc.usbc_enable_adc_data_scanner()

    def usbc_set_pd_command(self, command: int):
        """

        Used to issue commands to the PD Controller in USB-C enabled devices

        Parameters
        ----------
        command : int
            0 - No operation.
            1 - Reset PD Controller.
        """
        self._pdc.usbc_set_pd_command(command)

    def usbc_reset(self):
        """

        Reset PD Controller.

        """
        self.usbc_set_pd_command(1)

    def usbc_set_cc_pull_up(self, value):
        """

        Set CC pull up.

        Parameters
        ----------
        value : int
            3 - Indicate 0.9A power source capability.
            4 - Indicate 1.5A power source capability.
            5 - Indicate 3.0A power source capability.

        """
        self._pdc.usbc_set_cc_pull_up(value)

    # USBC capture
    def usbc_start_event_capture(self, event_types=('PD',)):
        """

        Starts capturing events.

        Parameters
        ----------
        event_types : tuple
            list of one or more of the following values:
                'PDC': pdc events
                All DP available events
                'USB-C Voltage' and 'USB-C Event' for UCD-500
        """

        self._capture.usbc_start_event_capture(event_types)

    def usbc_download_captured_events(self, save_to_bin_file: bool = False, save_to_txt_file: bool = False,
                                      path_to_save=""):
        """

        Download all captured events to current moment.

        Parameters
        ----------
        save_to_bin_file : bool
            Flag for saving captured events to bin files
        save_to_txt_file : bool
            Flag for saving captured events to txt files
        path_to_save : str
            Path to save all events

        Returns
        -------
        result : list
            Value (list) with captured events.

        """

        return self._capture.download_captured_events(save_to_bin_file, save_to_txt_file, path_to_save)

    def usbc_stop_event_capture(self):
        """

        Stop event capture.

        """

        self._capture.usbc_stop_event_capture()
