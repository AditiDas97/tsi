from tsi.tsi_devices.libs.lib_tsi.tsi import *
from tsi.tsi_devices.libs.lib_uicl.test_uicl import *
from tsi.tsi_devices.Dut_tests.DUT_tests import *
from tsi.tsi_devices.modules.EDID.edid import *
from tsi.tsi_devices.modules.device_constants import *
from tsi.tsi_devices.modules.DSC.dsc_converter import *
import time
import shutil


class TSIDevice:

    def __init__(self, device_handle: TSI_HANDLE, device_type: str, ports_and_roles: list):
        """

        General class for device.

        The class contains the following fields:
        handle - Indicates the device on which the operation is to be carried out;
        port_type - Device port type: DP, HDMI, USBC;
        type - Type of UCD device;
        role - Device role: RX(sink) or TX(source)
        port_number - Number of device port;
        serial_number - Serial number of device (for example, '1903C495');
        fw_info - Device firmware information (for example, '*Image 0 (Code 9): MF: 1.0.33 MN: 1.10.65')
        detailed_version_data - Detailed firmware version data (for example, PD: 0.0.19 [01.12.11])
        parser - Object of PacketParser class. Needed for capturing and parsing events from device.
        test - Object of GeneralDutTest class. Needed for configuration, running DUT tests.
        edid - Object of Edid class. Needed for reading, writing, saving and loading edid information.
        dsc_converter - Object of DscConverter class. Needed to convert a user image to a DSC image.
        memory_size - Total available device memory in bytes

        Parameters
        ----------
        device_handle : TSI_HANDLE
            Indicates the device on which the operation is to be carried out
        device_type : str
            Type of UCD device (for example, "UCD-340")
        ports_and_roles : list
            Contain info about Device port type (DP, HDMI, USB-C) and Device role (RX(sink) or TX(source))

        """

        self.__handle = device_handle
        self.__ports_and_roles = ports_and_roles
        self.__port_type = None
        self.__type = device_type
        self.__role = None
        self.__port_number = 0
        self.__serial_number = ""
        self.__fw_info = ""
        self.__detailed_version_data = ""
        self.__parser = TSI_CreateEventParser()
        self.__test = GeneralDutTest()
        self.__edid = Edid(self)
        self.__dsc_converter = DscConverter()
        self._memory_size = self.get_device_memory() * 0.8

        data = self.get_fw_version()
        data = data.split("\r\n")
        for item in enumerate(data):
            if item[0] == 0:
                self.__serial_number = item[1][item[1].find("/") + 2:]
            elif item[1].find("*Image") != -1 and item[1].find("[in use]") != -1:
                self.__fw_info = item[1].replace("[in use]", "").replace(",", "")
            elif item[1].find("MC") != -1 or item[1].find("PD") != -1 or item[1].find("PX") != -1:
                self.__detailed_version_data += item[1] + " "

    def __del__(self):
        """

        Deleted object of event parser.

        """

        TSI_RemoveEventParser(self.__parser)

    # Device info block
    def get_detailed_version_data(self) -> str:
        """

        Get a detailed version data.

        Returns
        -------
        result : str
            Version info.
        """

        return self.__detailed_version_data

    def get_device_fw_package(self) -> str:
        """

        Get a device firmware package.

        Returns
        -------
        result : str
            Firmware package info.

        """

        return self.__fw_info

    def set_role(self, role: str):
        """

        Set a role for device.

        Parameters
        ----------
        role : str
            Device role.

        """

        self.__role = role

    def get_role(self) -> str:
        """

        Get a current device role.

        Returns
        -------
        result : str
            String with info.

        """
        return self.__role

    def get_type(self) -> str:
        """

        Get a device type.

        Returns
        -------
        result : str
            String with info.

        """

        return self.__type

    def get_handle(self) -> TSI_HANDLE:
        """

        Get a device handle.

        Returns
        -------
        result : TSI_HANDLE
            Device handle.

        """

        return self.__handle

    def get_ports_and_roles(self) -> list:
        """

        """

        return self.__ports_and_roles

    def set_port_type(self, port_type: str):
        """

        Set a port type for device.

        Parameters
        ----------
        port_type : str
            Device role.
        """

        self.__port_type = port_type

    def get_port_type(self) -> str:
        """

        Get a current device port type.

        Returns
        -------
        result : str
            String with info.
        """
        return self.__port_type

    def get_tsi_name(self) -> str:
        """

        Get a tsi device name.

        Returns
        -------
        result : str
            String with info.

        """

        return self.get_port_type() + self.get_role()

    def get_full_name(self) -> str:
        """

        Get a full device name.

        Returns
        -------
        result : str
            String with info.

        """

        return self.__type + " [" + self.__serial_number + "]: " + self.__port_type + " " + self.__role

    def get_port_number(self) -> int:
        """

        Get a port device number.

        Returns
        -------
        result : int
            Number of current port.

        """

        return self.__port_number

    def get_device_memory(self) -> int:
        """

        Get a device memory size.

        Returns
        -------
        result : int
            Device memory size.

        """

        result = TSIX_TS_GetConfigItem(self.get_handle(), TSI_R_MEMORY_SIZE, c_uint64)[1]

        return result

    def open_port(self, port_id: int, role, dev_type):
        """

        Open port. If open port was not successfully, will be raised an exception.

        Parameters
        ----------
        port_id : int
            Number of port.

        """
        assert self.__handle is not None, "Device handle is None. Check device open function result!"
        result = TSIX_PORT_Select(self.__handle, port_id)
        self.__port_number = port_id
        self.__role = role
        self.__port_type = dev_type
        assert result >= TSI_SUCCESS, "Port is not available. Please, select another port!"

    def get_fw_version(self) -> str:
        """

        Getting firmware information from device.

        Returns
        -------
        result : str
            String with info.

        """

        result = TSIX_TS_GetConfigItem(self.get_handle(), TSI_FW_VERSION_TEXT, c_char, 16384)

        return result[1].value.decode('cp1252')

    # Public methods block
    def parse_event(self, data) -> list:
        """

        Getting a parse data.

        Parameters
        ----------
        data : list
            Input unparsed events

        """

        return TSI_GetParsedEventData(self.__parser, data)

    def capture_crc(self, count=1) -> list:
        """

        Capture and return CRC data from device.

        Parameters
        ----------
        count : int
            Count of CRC data.

        Returns
        -------
        result : list
            CRC data

        """

        real_count, crc, _ = TSIX_TS_GetConfigItem(self.get_handle(), TSI_CRC_MEASUREMENT_DATA_R, c_uint16,
                                                   count * 3 if count < CRC_MAX_READ_COUNT else CRC_MAX_READ_COUNT * 3)

        crc_list = []

        for i in range(0, real_count * 3, 3):
            crc_r = crc[i]
            crc_g = crc[i + 1]
            crc_b = crc[i + 2]
            crc_list.append(dict({"r": hex(crc_r), "g": hex(crc_g), "b": hex(crc_b)}))

        return crc_list

    @staticmethod
    def convert_frame(frame: ImageU, width=0, height=0, colorspace=0, sampling=0, bpc=0, component_order=0,
                      packing=0, _alignment=0, endianness=0, monochrome=False, crop=False, upscaling=False,
                      colorimetry=1) -> bytearray:
        """

        Сonverting one frame to another with the given settings.

        Parameters
        ----------
        frame : ImageU
            Reference (current) frame.
        width : int
            Width of destination frame.
        height : int
            Height of destination frame.
        colorspace : int
            Colorspace of destination frame.
        sampling : int
            Sampling of destination frame.
        bpc : int
            BPC of destination frame.
        component_order : int
            Component order of destination frame.
        packing : int
            Packing of destination frame.
        _alignment : int
            Alignment of destination frame.
        endianness : int
            Endianness of destination frame.
        monochrome : int
            Monochrome of destination frame.
        crop : int
            Crop of destination frame.
        upscaling : int
            Flag to upscaling
        colorimetry : int
            Colorimetry of destination frame.

        Returns
        -------
        result : bytearray
            Converted data of destination frame.

        """

        if upscaling:
            result = frame.upscaling(width, height, colorspace, sampling, bpc, packing, _alignment, endianness,
                                     monochrome, crop, colorimetry=colorimetry)
        else:
            result = frame.convert(width, height, colorspace, sampling, bpc, component_order, packing, _alignment,
                                   endianness, monochrome, crop, colorimetry=colorimetry)
        if result[0] < uicl.UICL_SUCCESS or result[1] is None:
            print('Error while conversion!')
            return bytearray()
        return bytearray(result[1])

    # DUT testing block
    def get_info_of_available_tests(self) -> str:
        """

        Getting information from the device about available tests.

        Returns
        -------
        result : str
            Return a string with available tests.

        """
        return self.__test.get_info_of_available_groups(self, self.get_port_number())

    def get_tests_in_group(self, test_group_id: TestGroupId) -> list:
        """

        Getting information from the device about amount of tests available in test group.

        Returns
        -------
        result : list
            Return a list with test ids of specified test group.

        """
        return self.__test.get_tests_in_group(self, self.get_port_number(), test_group_id)

    def get_default_data_for_test_group(self, id_group: int) -> dict:
        """

        Getting default values for a test group. Will be returned a dict with parameters:
        "Key (Name of CI)" : "Value (int, str or list)".

        Returns
        -------
        result : dict
            Default data(dict) with test settings.

        """
        return self.__test.choose_group_of_test(id_group)

    def get_test_name_from_group(self, id_group: TestGroupId, id_test: int) -> str:
        """

        Getting test name for specified test group id and test id. Will be returned a str with test name:

        Returns
        -------
        result : str
            Test name.

        """
        return self.__test.get_test_name_from_group(self, self.get_port_number(), id_group, id_test)

    def configure_test(self, data_for_test: dict, list_new_values: list):
        """

        Configure test settings.

        Parameters
        ----------
        data_for_test : dict
            Data(dict) with settings to test ("Key (Name of CI)" : "Value (int, str or list)").
        list_new_values : list
            Data(list) with new values for test settings.

        """

        self.__test.config_test(data_for_test, list_new_values)

    def read_info_from_device(self, device, port_id):
        """

        Read info about all available tests.

        Parameters
        ----------
        device : TSIDevice
            Indicates the device on which the operation is to be carried out
        port_id : int
            Indicates the port of device
        """
        self.__test.read_info_from_device(device, port_id)

    def run_test(self, id_group: int, id_test: int, data: dict, device_2=None, opf_device=None) -> list:
        """

        Run selected test by id test and id group.

        Parameters
        ----------
        id_group : int
            ID group of test
        id_test : int
            ID test
        data : dict
            Data to test
        device_2
            Additional parameter for test (It will be necessary, if present operator feedback dialog)
        opf_device
            Additional parameter for test (It will be necessary, if present operator feedback dialog).
            Can be used a default opf device object.

        Returns
        -------
        result : list
            Result list

        """

        return self.__test.run_test(self, id_group, id_test, data, device_2=device_2, opf_device=opf_device)

    def make_test_report(self, path: str, test_additional_info: TestAdditionalInfo) -> int:
        """

        Making html report after testing.

        Parameters
        ----------
        path : str
            Path to save report
        test_additional_info : TestAdditionalInfo
            Additional info about test (Dut Model Name, Dut Revision, Dut Serial Number, Dut Firmware Version,
            Dut Driver Version, Tested By, Remarks)

        Returns
        -------
        result : int
            Result list

        """

        return self.__test.make_report(path, test_additional_info, self)

    def run_test_from_file(self, path, device_2=None, opf_device=None):
        """

        Run test from special json file.

        Parameters
        ----------
        path : str
            Path to input file.
        device_2
            Additional parameter for test (It will be necessary, if present operator feedback dialog)
        opf_device
            Additional parameter for test (It will be necessary, if present operator feedback dialog).
            Can be used a default opf device object.

        """

        return self.__test.run_test_from_file(self, path, device_2=device_2, opf_device=opf_device)

    # EDID Block
    def read_edid(self) -> bytearray:
        """

        Allows access to read device EDID block(s).

        Returns
        -------
        result : bytearray
            Return a byte array with EDID data.

        """

        return self.__edid.read_edid()

    def write_edid(self, data: bytearray) -> TSI_RESULT:
        """

        Write EDID block(s) to device.

        Parameters
        ----------
        data : bytearray
            EDID block(s) data.

        Returns
        -------
        result : TSI_RESULT
            Return a result of operation.

        """

        return self.__edid.write_edid(data)

    def save_edid(self, path: str, data: bytearray, save_bin: bool = True, save_hex: bool = False):
        """

        Saving EDID block(s) from device.

        Parameters
        ----------
        path : str
            Path to save files.
        data : bytearray
            EDID block(s) data.
        save_bin : bool
            Flag for saving data to a file with .bin extension.
        save_hex : bool
            Flag for saving data to a file with .hex extension.

        """

        self.__edid.save_edid(path, data, save_bin, save_hex)

    def load_edid(self, path: str) -> bytearray:
        """

        Loading, parse and return EDID data from file.
        Valid file extensions: .bin, .hex.

        Returns
        -------
        result : bytearray
            Return EDID data from file.

        """

        return self.__edid.load_edid(path)

    # DSC Converter
    def set_dsc_converter_params(self, path_custom_image: str, path_to_save: str, params: DscParameters):
        """

        Set dsc converter params for future dsc image compression process.

        Parameters
        ----------
        path_custom_image : str
            Full path to custom image
        path_to_save : str
            Full path to saving image
        params : DscParameters
            Object of DscParameters class.
            Need to fill following fields:
            width: int, height: int, colorformat: int, bpc: int, bpp: int, is_block_prediction_enabled: bool,
            horizontal_slice_number: int, buffer_bit_depth: int, vertical_slice_number: int

        """

        self.__dsc_converter.set_params(path_custom_image, path_to_save, params)

    def compress_dsc_image(self, is_simple422_selected: bool):
        """

        Start the dsc image compression process.

        Parameters
        ----------
        is_simple422_selected : bool
            Flag simple 422 mode.

        """

        self.__dsc_converter.compress_dsc(is_simple422_selected)
