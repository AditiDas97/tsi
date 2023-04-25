from tsi.tsi_devices.Dut_tests.opf_dialog import *
from .Reports import *
import threading

# int = 0,Double = 1,String = 2,Bool = 3,Uint32 = 4,ArrayU8 = 5,ArrayU16 = 6,ArrayU32 = 7,PHYAddress = 8,BitFlag = 9,
# ArrayFromFilePath = 10, FolderPath = 11

_device = None
_file = None
_result = []
_test = OPF()


def search_bit(mask):
    count = 0

    if mask:
        while not (mask & 1):
            mask >>= 1
            count += 1

    return count


@WINFUNCTYPE(c_int, POINTER(TSI_OPF_CALLBACK_STRUCT), c_void_p)
def ofp_impl(_struct, _void_p):
    global _file
    global _test
    if _file is not None:
        _file.write("*Operator Feedback Dialog*\n")
    param = []
    if _struct[0].ParameterCount >= 2:
        for i in range(_struct[0].ParameterCount):
            param.append(_struct[0].Parameters[i])
    else:
        param.append(_struct[0].Parameters)
    return _test.input_message(_struct[0].ID, _struct[0].Title.decode("utf-8"),
                               _struct[0].Request.decode("utf-8"), _struct[0].Request2.decode("utf-8"), param)


class DUTDevice:

    def __init__(self, device, data, device_2):
        self.data = data
        global _device
        _device = device_2
        global _file
        self.device = device

    def clear_data(self):
        self.data.clear()

    def set_operator_feedback(self):
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_TS_OF_MODE, TSI_OFMODE_RUN_CALL_STRUCT_PROCEDURE)
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_TS_OF_REQ_ID, -1)
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_TS_OF_CALLBACK, ofp_impl)

    def status_thread(self, current_test):
        global _result
        t = threading.current_thread()
        while getattr(t, "stop_thread", True):
            result = TSIX_STLOG_WaitMessage(self.device.get_handle(), 250)
            if result > 0:
                msg_count = result
                for i in range(0, msg_count):
                    result = TSIX_STLOG_GetMessageData(self.device.get_handle())
                    if result[0] >= TSI_SUCCESS:
                        print(result[1])
                        if str(result[1]).find("Error:") != -1:
                            _result.append(int(result[1][str(result[1]).find("Error:") + 6: str(result[1]).rfind(":")]))
                            _result.append(result[1][str(result[1]).rfind(":") + 1:])
                        current_test.logMessages += result[1] + "\n"
                        if str(result[1]).lower().find("test failed") != -1:
                            current_test.result = 'FAILED'
                        elif str(result[1]).lower().find("test passed") != -1:
                            current_test.result = 'PASSED'
                        elif str(result[1]).lower().find("test skipped") != -1:
                            current_test.result = 'SKIPPED'
        return 0

    def configure_test(self, current_test: TestReport):
        current_test.startTime = datetime.now()

        for parameter in self.data:
            _len = 1
            _type = c_uint32

            value = None

            if str(parameter.variable_dict.get('defaultValue')).find('0x') != -1:
                value = dict_types.get(parameter.variable_dict.get('type'))(parameter.variable_dict.get('defaultValue'),
                                                                            16)
                _type = c_uint32
            else:
                if dict_types.get(parameter.variable_dict.get('type')) == str:
                    value = parameter.variable_dict.get('defaultValue')
                    _type = c_char_p
                    _len = len(value)
                elif dict_types.get(parameter.variable_dict.get('type')) == bool:
                    value = int(parameter.variable_dict.get('defaultValue'))
                    _type = c_bool
                elif parameter.variable_dict.get('defaultValue') == '' or \
                        parameter.variable_dict.get('defaultValue') == []:
                    if dict_types.get(parameter.variable_dict.get('type')) == list:
                        value = []
                        _len = 6
                    else:
                        value = 0
                    _type = c_uint32
                elif dict_types.get(parameter.variable_dict.get('type')) == list:
                    param = parameter.variable_dict.get('defaultValue')
                    value = []
                    if type(param) != list and type(param) == str:
                        param = param.split(" ")
                        param.pop()
                        for p in param:
                            value.append(int(p))
                    else:
                        value = param
                    _len = len(value)
                    _type = c_uint16
                elif dict_types.get(parameter.variable_dict.get('type')) == "bitList":
                    bit_list = parameter.variable_dict.get('bitList')
                    value = 0
                    for elem in bit_list:
                        mask = elem.get("mask")
                        offSet = search_bit(mask)
                        value |= (int(elem.get("defaultValue")) << offSet) & mask if int(elem.get("defaultValue")) != 0\
                            else 0
                    _type = c_uint32
                else:
                    value = dict_types.get(parameter.variable_dict.get('type')) \
                        (parameter.variable_dict.get('defaultValue'))
                    _type = dict_c_types.get(dict_types.get(parameter.variable_dict.get('type')))

            result = TSIX_TS_SetConfigItem(self.device.get_handle(), int(parameter.variable_dict.get('configId'), 16),
                                           value, data_type=_type, data_count=_len)

            assert result >= TSI_SUCCESS, 'TSIX_TS_SetConfigItem() Test configuration error.'
            current_test.configuration += "{} = {}<br>".format(str(parameter.variable_dict.get('name')), str(value))

        return TSI_SUCCESS

    def run_test(self, test_id: int, reports_list: list, test_report: TestReport, opf_dialog=None) -> list:
        global _device
        global _result
        global _test
        _result.clear()

        if opf_dialog is None:
            opf_dialog = TsiOpfDevice(_device)

        _test.set_opf_dialog(opf_dialog)
        result = self.configure_test(test_report)

        if result < TSI_SUCCESS:
            print('Test configuration failed!')
            return result
        print('Test configuration success!')

        thread = threading.Thread(target=self.status_thread, args=(test_report, ))

        thread.start()
        self.set_operator_feedback()
        if self.device.get_type().replace("UCD-", "") in ["400", "424", "500"] \
                and str(self.device.__module__).find('rx') != -1:
            self.device.dprx_set_dsc(True)
            self.device.dprx_capable_fec(True, False)
            self.device.dprx_set_link_flags(True, True, True, True, False, False)
            self.device.dprx_set_hpd_pulse(1000 * 1000)
        result = TSIX_TS_RunTest(self.device.get_handle(), test_id)
        test_report.endTime = datetime.now()
        reports_list.append(test_report)
        thread.stop_thread = False
        thread.join()
        _result.insert(0, result)
        # if _device is not None and _device.get_role() == "TX":
        #     _device.stop_generate_audio()

        return _result
