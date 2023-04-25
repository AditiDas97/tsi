import json
import re
from sys import platform
from .DUT_device import *
from enum import IntEnum


class TestGroupId(IntEnum):
    DP_RX_ELECTRICAL = 0x01
    HDMI_RX_ELECTRICAL = 0x02
    CEC_FUNCTIONAL = 0x05
    DP_RX_CRC = 0x06
    DP_RX_SIMPLE_LT = 0x07
    DP_HDCP_CTS_AUTHENTICATION = 0x0A
    HDMI_RX_CRC = 0x0B
    USB_TYPE_C_ELECTRICAL = 0x0C
    DP_RX_LL_CTS = 0x0E
    DP_TX_LL_CTS = 0x0F
    DP_TX_LL_CTS_DSC = 0x10
    DP_RX_LL_CTS_DSC = 0x11
    DP_2_0_RX_LL_CTS = 0x12
    DP_2_0_TX_LL_CTS = 0x13
    DP_HDCP_CTS_1A = 0x26
    DP_HDCP_CTS_1B = 0x27
    DP_HDCP_CTS_2C = 0x28
    DP_HDCP_CTS_3A = 0x29
    DP_HDCP_CTS_3B = 0x2A
    DP_HDCP_CTS_3C = 0x2B
    DP_TX_DISPLAYID = 0x32
    DP_RX_DISPLAYID = 0x33
    HDMI_RX_VRR = 0x34
    HDMI_TX_VRR = 0x35
    DP_TX_ADAPTIVESYNC = 0x36
    DP_RX_ADAPTIVESYNC = 0x37


def conversion_str_to_hex(value: str):
    result = re.findall(r'[0-9, A-F]\.[0-9, A-F]\.[0-9, A-F]\.[0-9, A-F]', value)
    assert result != []
    return int(result[0].replace(".", ""), 16)


class TypeTest:

    def __init__(self, _dict: dict):
        self.id = []
        self.id_group = 0
        self.variable_dict = dict()
        for key in _dict.keys():
            if key == "enumerationVariants":
                self.variable_dict.update({key: self.parse(_dict.get(key))})
            else:
                self.variable_dict.update({key: _dict.get(key)})

    def change_value(self, new_value):
        if self.variable_dict.get('type') == 8:
            self.variable_dict.update({'defaultValue': conversion_str_to_hex(new_value)})
        else:
            self.variable_dict.update({'defaultValue': new_value})

    @staticmethod
    def parse(_str):
        list_value = []
        if type(_str) == str:
            value = _str.split("\n")
            for _str in value:
                if _str.find("#") != -1:
                    if _str.find("0x") != -1:
                        list_value.append(int(_str[: _str.find("#")], 16))
                    else:
                        list_value.append(int(_str[: _str.find("#")]))
                else:
                    list_value.append(int(_str))
            return list_value
        else:
            return _str


class GeneralDutTest:

    def __init__(self):
        self.all_tests = []
        self.dict_group = dict()
        self.reports_list = []

        if platform == "linux":
            self.read_json(path="")
        elif platform == 'darwin':
            self.read_json(path="")
        elif platform == 'win32':
            self.read_json(path=WIN_PROPERTY_JSON_PATH)

    def read_info_from_device(self, device, port):
        self.dict_group.clear()
        count = TSIX_PORT_GetTestCount(device.get_handle(), port)
        _list = list()
        for i in range(count):
            data = TSIX_PORT_GetTestInfo(device.get_handle(), port, i)
            id_group = data[0] >> 16
            id_test = data[0] & 0xFFFF
            name = data[2]
            if name.find('Electrical Test Set') != -1:
                if device.get_port_type() == 'HD':
                    name = 'HDMI' + ' ' + data[2]
                elif device.get_port_type() == 'USBC':
                    name = 'USBC' + ' ' + data[2]
                else:
                    name = device.get_port_type() + ' ' + data[2]
            if name.find('Compare video frame sequence') != -1:
                id_group = 1000
            _list.append((name, id_group, id_test))
        for i in range(len(self.all_tests)):
            name = self.all_tests[i].get('name')
            for info in _list:
                if info[0].find(name) != -1 or (info[0].find("AdaptiveSync CTS Sink Test Set") != -1
                                                and name == "Link Layer CTS Test Set"):
                    for elem in self.all_tests[0].get('data'):
                        elem.id.append(info[2])
                        elem.id_group = info[1]
                    self.dict_group.update({info[1]: i})

    @staticmethod
    def get_info_of_available_groups(device, port):
        count = TSIX_PORT_GetTestCount(device.get_handle(), port)
        _str = str()
        for i in range(count):
            name = []
            data = TSIX_PORT_GetTestInfo(device.get_handle(), port, i)
            id_group = data[0] >> 16
            id_test = data[0] & 0xFFFF
            if data[2].find('/') != -1:
                name = data[2].split("/")
            else:
                if data[2].find("Validate audio") != -1:
                    name.append("Audio Test")
                else:
                    name.append("Pixel Level Video Test")
                    id_group += 1000
                name.append(str(data[2]))
            if _str.find(name[0]) == -1 or _str.find("Group ID: {}".format(id_group)) == -1:
                _str += "\nGroup ID: {}. Group name: {}\nTest list:\n".format(id_group, name[0])
            _str += "Test ID: {}. Test name:{}.\n".format(id_test, name[1])
        return _str

    @staticmethod
    def get_tests_in_group(device, port, test_group_id):
        count = TSIX_PORT_GetTestCount(device.get_handle(), port)
        test_list = []
        for i in range(count):
            data = TSIX_PORT_GetTestInfo(device.get_handle(), port, i)
            id_group = data[0] >> 16
            id_test = data[0] & 0xFFFF

            if id_group != test_group_id:
                continue

            test_list.append(id_test)

        return test_list

    @staticmethod
    def get_test_name_from_group(device, port, test_group_id, test_id):
        count = TSIX_PORT_GetTestCount(device.get_handle(), port)
        for i in range(count):
            name = []
            data = TSIX_PORT_GetTestInfo(device.get_handle(), port, i)
            id_group = data[0] >> 16
            id_test = data[0] & 0xFFFF

            if id_group != test_group_id or id_test != test_id:
                continue

            if data[2].find('/') != -1:
                name = data[2].split("/")
            else:
                if data[2].find("Validate audio") != -1:
                    name.append("Audio Test")
                else:
                    name.append("Pixel Level Video Test")
                    id_group += 1000
                name.append(str(data[2]))

            return name[1].strip()
        return ""

    def read_json(self, path=""):
        with open(path, "r", encoding='utf-8') as read_file:
            temp_data = json.load(read_file)

        for index_test in temp_data:
            temp_list = []
            if index_test.get('shortName') == "Audio Test":
                test_data = index_test.get('descriptions')
                for i in test_data:
                    if i.get('id') != "RESERVED":
                        temp_list.append(TypeTest(i))
            elif index_test.get('shortName') == "USBC Electrical Tests":
                test_data = index_test.get('descriptions')
                for i in test_data:
                    if i.get('id') != "RESERVED":
                        temp_list.append(TypeTest(i))
            elif index_test.get('name') == "HDMI Electrical Test Set":
                test_data = index_test.get('descriptions')
                for i in test_data:
                    if i.get('id') != "RESERVED":
                        temp_list.append(TypeTest(i))
            elif index_test.get('shortName') == "Link Config Tests":
                test_data = index_test.get('descriptions')
                for i in test_data:
                    if i.get('id') != "RESERVED":
                        temp_list.append(TypeTest(i))
            elif index_test.get('name') == "DP Electrical Test Set":
                test_data = index_test.get('descriptions')
                for i in test_data:
                    if i.get('id') != "RESERVED":
                        temp_list.append(TypeTest(i))
            elif index_test.get('name') == "DP 1.4 Link Layer Source DUT CTS":
                test_data = index_test.get('descriptions')
                for i in test_data:
                    if i.get('id') != "RESERVED":
                        temp_list.append(TypeTest(i))
            elif index_test.get('name') == "DP 1.4 Link Layer Sink DUT CTS":
                test_data = index_test.get('descriptions')
                for i in test_data:
                    if i.get('id') != "RESERVED":
                        temp_list.append(TypeTest(i))
            elif index_test.get('name') == "DP 2.0 Link Layer Source DUT CTS":
                test_data = index_test.get('descriptions')
                for i in test_data:
                    if i.get('id') != "RESERVED":
                        temp_list.append(TypeTest(i))
            elif index_test.get('name') == "DP 2.0 Link Layer Sink DUT CTS":
                test_data = index_test.get('descriptions')
                for i in test_data:
                    if i.get('id') != "RESERVED":
                        temp_list.append(TypeTest(i))
            # elif index_test.get('shortName') == "Pixel Level Video Tests":
            #     test_data = index_test.get('descriptions')
            #     for i in test_data:
            #         if i.get('id') != "RESERVED":
            #             temp_list.append(TypeTest(i))
            if index_test.get('shortName') == "CRC Video Tests":
                test_data = index_test.get('descriptions')
                for i in test_data:
                    if i.get('id') != "RESERVED":
                        temp_list.append(TypeTest(i))
            elif index_test.get('shortName') == "CEC functional Test Set":
                test_data = index_test.get('descriptions')
                for i in test_data:
                    if i.get('id') != "RESERVED":
                        temp_list.append(TypeTest(i))
            elif index_test.get('shortName').find("HDCP 2.3 CTS") >= 0:
                test_data = index_test.get('descriptions')
                for i in test_data:
                    if i.get('id') != "RESERVED":
                        temp_list.append(TypeTest(i))
            elif index_test.get("shortName") == 'VRR Sink DUT Tests':
                test_data = index_test.get('descriptions')
                for i in test_data:
                    if i.get('id') != "RESERVED":
                        temp_list.append(TypeTest(i))
            elif index_test.get("shortName") == 'VRR Source DUT Tests':
                test_data = index_test.get('descriptions')
                for i in test_data:
                    if i.get('id') != "RESERVED":
                        temp_list.append(TypeTest(i))

            self.all_tests.append({'name': index_test.get('name'), 'data': temp_list})

    def choose_group_of_test(self, choice: int):
        temp_list = self.all_tests[self.dict_group.get(choice)].get('data')
        new_dict = dict()
        for element in temp_list:
            new_dict.update({element.variable_dict.get('id'): element.variable_dict.get('defaultValue')})
        return new_dict

    @staticmethod
    def config_test(chosen_test: dict, list_of_values: list):
        list_of_keys = list(chosen_test.keys())
        assert len(list_of_keys) == len(list_of_values)
        for i in range(len(list_of_keys)):
            chosen_test[list_of_keys[i]] = list_of_values[i]

    def change_values_in_data(self, value: dict, group_number: int, delta: int):
        index = self.dict_group.get(group_number)
        choice_data = self.all_tests[index].get('data')
        i = 0

        for key in value:
            value_type = choice_data[i].variable_dict.get('type')
            old = value.get(key)
            _id = choice_data[i].variable_dict.get('id')
            if _id.find("MAX_LANES") != -1:
                if old == '4':
                    old = "2"
                else:
                    old = '4'
                value.update({key: old})
            if value_type in [0, 4, 8, 9]:
                if _id.find("TIMEOUT") == -1 and _id.find("HPD_PULSE") == -1 and _id.find("MAX_LANES") == -1 and\
                        _id.find("CYCLE_DELAY") == -1:
                    old = str(int(old, 16) + delta)
                    value.update({key: old})
            elif value_type == 1:
                if _id.find("TIMEOUT") == -1 and _id.find("HPD_PULSE") == -1 and _id.find("MAX_LANES") == -1 and \
                        _id.find("CYCLE_DELAY") == -1:
                    old = str(float(old) + delta)
                    value.update({key: old})
            elif value_type in [5, 6, 7, 10]:
                pass
            i += 1

    def run_test(self, device, group_number: int, test_id: int, value: dict, device_2=None, opf_device=None):
        """

        In this function did a selected test for selected device.

        Parameters
        ----------
        device
        group_number: int
            Number of selected group tests.
        test_id: int
            Id test.
        value: dict
            Value for test.
        device_2
        opf_device
        """

        index = self.dict_group.get(group_number)

        choice_data = self.all_tests[index].get('data')

        for i in range(len(value)):
            def_value = choice_data[i].variable_dict.get('defaultValue')
            new_value = value.get(choice_data[i].variable_dict.get('id'))
            value_type = choice_data[i].variable_dict.get('type')
            if new_value != def_value:
                max_v = choice_data[i].variable_dict.get('maxValue')
                min_v = choice_data[i].variable_dict.get('minValue')
                enum_variants = choice_data[i].variable_dict.get('enumerationVariants')
                if max_v is not None and min_v is not None and value_type == 4:
                    try:
                        new_value = int(new_value)
                        assert min_v <= new_value <= max_v
                        if enum_variants is not None:
                            assert new_value in enum_variants
                        choice_data[i].variable_dict.update({'defaultValue': new_value})
                    except BaseException:
                        print("Used invalid value in {} = {}. The default value = {} will be used.".format(
                            choice_data[i].variable_dict.get('id'), new_value, def_value))

                elif value_type in [5, 6, 7, 10]:
                    try:
                        assert type(new_value) == list
                        choice_data[i].variable_dict.update({'defaultValue': new_value})
                    except BaseException:
                        print("Used invalid value in {} = {}. The default value = {} will be used.".format(
                            choice_data[i].variable_dict.get('id'), new_value, def_value))
                elif value_type in [3, 9]:
                    try:
                        assert new_value in [0, 1]
                        choice_data[i].variable_dict.update({'defaultValue': new_value})
                    except BaseException:
                        print("Used invalid value in {} = {}. The default value = {} will be used.".format(
                            choice_data[i].variable_dict.get('id'), new_value, def_value))
                elif value_type == 8:
                    try:
                        new_value = conversion_str_to_hex(new_value)
                        assert 0 <= new_value <= 65535
                        choice_data[i].variable_dict.update({'defaultValue': new_value})
                    except BaseException:
                        print("Used invalid value in {} = {}. The default value = {} will be used.".format(
                            choice_data[i].variable_dict.get('id'), new_value, def_value))
                elif value_type in [2, 11]:
                    try:
                        assert type(new_value) == str
                        choice_data[i].variable_dict.update({'defaultValue': new_value})
                    except BaseException:
                        print("Used invalid value in {} = {}. The default value = {} will be used.".format(
                            choice_data[i].variable_dict.get('id'), new_value, def_value))
                else:
                    choice_data[i].variable_dict.update({'defaultValue': new_value})

        dev = DUTDevice(device, choice_data, device_2)

        test_name, test_group = self.find_test_name(device, group_number, test_id)

        test_report = TestReport(TestInfo(test_name, str(test_id), test_group))
        result = dev.run_test((group_number << 16) | test_id, self.reports_list, test_report, opf_device)

        return result

    def run_test_from_file(self, device, file: str, device_2=None, opf_device=None):
        with open(file, "r", encoding='utf-8') as read_file:
            data = json.load(read_file)

        TestId = data.get("TestId")
        group_number = int(TestId[: 4], 16)
        test_id = int(TestId[4:], 16)
        Data = data.get("Data")

        data_for_test = []
        property_data = self.all_tests[self.dict_group.get(group_number)].get('data')

        for item in property_data:
            data_for_test.append(TypeTest(item.variable_dict.copy()))
            item_for_test = data_for_test[-1]
            value = item.variable_dict.get("defaultValue") if item.variable_dict.get("defaultValue") == \
                                                              Data.get(item.variable_dict.get('id')) else \
                Data.get(item.variable_dict.get('id'))
            item_for_test.variable_dict.update({"defaultValue": value})
            if int(item.variable_dict.get("type")) == 12:
                for i in range(len(item.variable_dict.get("bitList"))):
                    mask = item.variable_dict.get("bitList")[i].get("mask")
                    mask = int(mask, base=(16 if mask.find("0x") != -1 else 10))
                    item_for_test.variable_dict.get("bitList")[i].update({"defaultValue": int(value) & mask})

        test_name, test_group = self.find_test_name(device, group_number, test_id)
        test_report = TestReport(TestInfo(test_name, str(test_id), test_group))

        dev = DUTDevice(device, data_for_test, device_2)
        result = dev.run_test(int(TestId, 16), self.reports_list, test_report, opf_device)

        return result

    def find_test_name(self, device, group_number, test_id):
        _str = self.get_info_of_available_groups(device, device.get_port_number())
        _list = _str.split('\n')
        test_name = ""
        test_group = ""
        for elem in _list:
            if elem.find("Group ID") != -1:
                if int(elem[elem.find(":") + 1: elem.find(".")]) == group_number:
                    test_group = elem[elem.find("Group name:") + 11:]
            if test_group != "":
                if elem.find("Test ID") != -1:
                    if int(elem[elem.find(":") + 1: elem.find(".")]) == test_id:
                        test_name = elem[elem.find("Test name:") + 10:]
                        break

        return test_name, test_group

    def make_report(self, path: str, test_additional_info: TestAdditionalInfo, device):
        if len(self.reports_list) > 0:
            report = Report()
            test_additional_info.deviceName = device.get_full_name()
            test_additional_info.deviceFirmwarePackage = device.get_device_fw_package()
            test_additional_info.deviceDetailedVdata = device.get_detailed_version_data()
            test_additional_info.pythonVersion = str(TSI_CURRENT_VERSION)
            report.generate_html_report(path, test_additional_info, self.reports_list)
            return 0
        else:
            return 1
