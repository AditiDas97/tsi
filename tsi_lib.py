from .tsi_devices.tsi_dp_rx500 import *
from .tsi_devices.tsi_hd_rx400 import *
from .tsi_devices.tsi_usbc_rx500 import *
from .tsi_devices.tsi_usbc_rx400 import *
from .tsi_devices.tsi_dp_tx500 import *
from .tsi_devices.tsi_hd_tx400 import *
from .tsi_devices.tsi_usbc_tx500 import *
from .tsi_devices.tsi_usbc_tx400 import *
from .tsi_devices.tsi_usbc_tx import *
from .tsi_devices.tsi_usbc_rx import *
import sys


class TsiLib:

    def __init__(self):
        """

        General class of initialization TSI library.
        Private variables:
            tsi - object of TSI lib
            device_count - count of available devices
            list_device_name - list of available device names

        """
        self.__list_device_name = list()
        self.__list_numbers = list()
        self.__device_count = TSI_RESULT
        try:
            self.__tsi = TSI_Init(TSI_CURRENT_VERSION)
            assert self.__tsi >= TSI_SUCCESS
        except AssertionError:
            sys.exit(1)

    def __del__(self):
        """

        Run TSI_Clean (Closes device).
        Delete variables: list_device_name, device_count, list_numbers.

        """
        self.__tsi = TSI_Clean()
        del self.__list_device_name, self.__device_count, self.__list_numbers

    def print_device_list(self, print_out=True):
        """

        Print list with available devices.

        Parameters
        ----------
        print_out : bool
            Flag used for printing info

        """

        self.__list_device_name.clear()
        self.__device_count = TSI_DEV_GetDeviceCount()
        if self.__device_count == 0:
            raise DeviceOpenError("No available devices.")

        if print_out:
            print('Devices available: ')
        for index in range(self.__device_count):
            name = str(TSI_DEV_GetDeviceName(index)[1])
            self.__list_device_name.append(name)
            self.__list_numbers.append(name[name.find("[") + 1: name.find("]")])
            if print_out:
                print('Device {}: \'{}\''.format(index, self.__list_device_name[-1]))

    def find_device_role_index(self, serial_number: str, port_name_and_role: list) -> int:
        """
        
        Find a device role index.
        Example:
            find_device_role_index("1234C789", (("DP", "RX")))

        Parameters
        ----------
        serial_number : str
            The serial number of the device.
        port_name_and_role : list
            Port name of the device (DP, HD, USBC)
            Port role of the device (RX, TX)

        Returns
        -------
        device_index : int
            Device role index

        """

        assert (type(serial_number) == str and len(serial_number) == 8), \
            "Device ID should be provide type int or string with length 8 symbols"

        self.print_device_list(False)
        start_index_ser_number = self.__list_numbers.index(serial_number.upper())
        amount_devices = self.__list_numbers.count(serial_number.upper())
        device_index = -1

        for i in range(start_index_ser_number, start_index_ser_number + amount_devices):
            info = self.__get_tuple(self.__list_device_name[i])
            device_index = 0

            for item in info[1]:
                for inp in port_name_and_role:
                    if inp[0] == item[0] and inp[1] == item[1]:
                        device_index += 1
            if (len(info[1]) == len(port_name_and_role) and device_index == len(port_name_and_role)) \
                    or (len(info[1]) > len(port_name_and_role) and device_index > 0):
                device_index = i - start_index_ser_number
                break
            else:
                device_index = -1

        return device_index

    def open_device(self, device_id, print_out=True, role=None, device_role_index=None) -> TSIDevice:
        """

        Open the indicated device and return an object of TSIDevice.

        Parameters
        ----------
        device_id : int or str
            Indicates the device. Also perform as the serial number of the device.
        print_out : bool
            Print info about available device
        role : str (Do not using this parameter. Will be removed.)
            Role of device (RX - Sink, TX - Source)
        device_role_index : int
            Device index in the list of serial numbers

        Returns
        -------
        result : TSIDevice
            Object of class TSIDevice
        """

        self.print_device_list(print_out)
        if print_out:
            print('\nSelecting device {}...'.format(device_id))

        assert type(device_id) == int or (type(device_id) == str and len(device_id) == 8), \
            "Device ID should be provide type int or string with length 8 symbols"

        if type(device_id) == str:
            if not (device_role_index is not None and device_role_index >= 0):
                raise DeviceOpenError(f"Incorrect device role index: {device_role_index}.")
            if device_id.upper() not in self.__list_numbers:
                raise DeviceOpenError(f"Device with {device_id.upper()} serial number is not found.")
            start_index_ser_number = self.__list_numbers.index(device_id.upper())
            amount_devices = self.__list_numbers.count(device_id.upper())
            if device_role_index >= amount_devices:
                raise DeviceOpenError(f"Device role index {device_role_index} is out of range {amount_devices}.")
            device_id = device_role_index + start_index_ser_number

        if self.__list_device_name[device_id].find("in use") != -1:
            raise DeviceOpenError(f"Device {self.__list_device_name[device_id]} {self.__list_numbers[device_id]} "
                                  f"is not available. Please, select another free device.")
        if device_id < 0:
            raise DeviceOpenError(f"Can not find device.")

        temp = self.__get_tuple(self.__list_device_name[device_id])
        if print_out:
            _info = ""
            for item in temp[1]:
                _info += "\nPort - {}{}".format(item[0], item[1])
            print("For device {} available following ports and roles: {}".format(temp[0], _info))
        return TSIDevice(TSIX_DEV_OpenDevice(device_id)[1], temp[0], temp[1])

    @staticmethod
    def __get_tuple(info: str):
        device_type = None
        device_type_prev = None
        device_role = None
        device_ports = []

        device_info = info[info.find(":"):]
        if device_info.find("and") != -1:
            device_info = device_info.split("and")
        else:
            device_info = [device_info]

        for i in range(len(device_info)):
            if device_info[i].find("HDMI") != -1:
                device_type = "HD"
            elif device_info[i].find("DisplayPort") != -1:
                device_type = "DP"
            elif device_info[i].find("USB-C") != -1:
                device_type = "USBC"

            if device_info[i].find("Sink") != -1:
                device_role = "RX"
            elif device_info[i].find("Source") != -1:
                device_role = "TX"

            device_ports.append([device_type if device_type != device_type_prev else device_ports[-1][0],
                                 device_role, i if device_type != device_type_prev else i - 1])
            if i > 0 and device_ports[i][2] == device_ports[i - 1][2]:
                device_ports[i - 1][2] = i

            device_type_prev = device_type

        return info[:7], device_ports

    @staticmethod
    def close_device(device: TSIDevice) -> TSI_RESULT:
        """

        Close the device indicated by the handle value.

        Parameters
        ----------
        device : TSIDevice
            Indicates the device on which the operation is to be carried out

        Returns
        -------
        result : TSI_RESULT
            Result of closing device (successfully or not)
        """

        result = TSIX_DEV_CloseDevice(device.get_handle())
        if result < TSI_SUCCESS:
            return result
        return TSI_SUCCESS
