from .tsi_types import *
from .tsi_private_types import *
import os.path
import sys

_assert_tsi_success = True

TSI_CURRENT_VERSION = 12
TSI = None
WIN_TSI_PATH = __file__[:-7] + '\\TSI.dll'
WIN_PROPERTY_JSON_PATH = __file__[:-7] + '\\PropertyDescription.json'

if not os.path.isfile(WIN_TSI_PATH):
    WIN_TSI_PATH = 'C:\\Program Files\\Unigraf\\Unigraf UCD Tools\\TSI.dll'

if not os.path.isfile(WIN_PROPERTY_JSON_PATH):
    WIN_PROPERTY_JSON_PATH = 'C:\\Program Files\\Unigraf\\Unigraf UCD Tools\\data\\dut_test\\PropertyDescription.json'

dll_path = WIN_TSI_PATH
try:
    TSI = windll.LoadLibrary(dll_path)
except OSError:
    print('ERROR({}): {}'.format(GetLastError(), dll_path))
    if GetLastError() == 193:
        print(
            'Perhaps you are using a 64-bit python interpreter along with a 32-bit library, or vice versa.'
            ' Need the same.')


def from_cstr(src_str):
    return src_str.value.decode('cp1252')


def to_cstr(src_str):
    return c_char_p(src_str.encode('utf-8'))


def show_error(error_code):
    if error_code >= TSI_SUCCESS:
        return False
    result = TSI_MISC_GetErrorDescription(error_code)
    val = None
    if result[0] < TSI_SUCCESS:
        val = ' Error %d: (No description available)' + str(error_code) + '\n'
    else:
        val = ' Error ' + str(error_code) + ': ' + str(result[1]) + "\n"
    return val


def create_c_array(data, _type, _size):
    buftype = _type * _size
    buf = buftype()
    buf.value = data
    return buf


def TSI_Init(version):
    _TSI_Init = TSI.TSI_Init
    _TSI_Init.argtypes = [TSI_VERSION_ID]
    _TSI_Init.restype = TSI_RESULT
    _version = c_uint(version)
    return _TSI_Init(_version)


def TSI_Clean():
    _TSI_Clean = TSI.TSI_Clean
    _TSI_Clean.argtypes = []
    _TSI_Clean.restype = TSI_RESULT
    return _TSI_Clean()


def TSI_DEV_GetDeviceCount():
    _TSI_DEV_GetDeviceCount = TSI.TSI_DEV_GetDeviceCount
    _TSI_DEV_GetDeviceCount.argtypes = []
    _TSI_DEV_GetDeviceCount.restype = TSI_RESULT

    result = _TSI_DEV_GetDeviceCount()
    assert result >= TSI_SUCCESS, 'TSI_DEV_GetDeviceCount() return {}'.format(result)

    return result


def TSI_DEV_GetDeviceName(device_id: int):
    _TSI_DEV_GetDeviceName = TSI.TSI_DEV_GetDeviceName
    _TSI_DEV_GetDeviceName.argtypes = (TSI_DEVICE_ID, c_char_p, c_uint)
    _TSI_DEV_GetDeviceName.restype = TSI_RESULT

    _device_name = create_string_buffer(TSI_NAME_SIZE)
    result = _TSI_DEV_GetDeviceName(device_id, _device_name, TSI_NAME_SIZE)

    return result, from_cstr(_device_name)


def TSIX_DEV_OpenDevice(device_id: int):
    _TSIX_DEV_OpenDevice = TSI.TSIX_DEV_OpenDevice
    _TSIX_DEV_OpenDevice.argtypes = (TSI_DEVICE_ID, POINTER(TSI_RESULT))
    _TSIX_DEV_OpenDevice.restype = TSI_HANDLE

    result = c_int(TSI_SUCCESS)
    _device_id = c_uint(device_id)
    device = _TSIX_DEV_OpenDevice(_device_id, byref(result))

    return result.value, device


def TSIX_DEV_CloseDevice(device):
    _TSIX_DEV_CloseDevice = TSI.TSIX_DEV_CloseDevice
    _TSIX_DEV_CloseDevice.argtypes = (TSI_HANDLE,)
    _TSIX_DEV_CloseDevice.restype = TSI_RESULT
    return _TSIX_DEV_CloseDevice(device)


def TSIX_PORT_Enable(device, port_index):
    _TSIX_PORT_Enable = TSI.TSIX_PORT_Enable
    _TSIX_PORT_Enable.argtypes = (TSI_HANDLE, TSI_LOGICAL_PORT)
    _TSIX_PORT_Enable.restype = TSI_RESULT

    _port_index = c_uint32(port_index)

    return _TSIX_PORT_Enable(device, port_index)


def TSIX_PORT_Disable(device, port_index):
    _TSIX_PORT_Disable = TSI.TSIX_PORT_Disable
    _TSIX_PORT_Disable.argtypes = (TSI_HANDLE, TSI_LOGICAL_PORT)
    _TSIX_PORT_Disable.restype = TSI_RESULT

    _port_index = c_uint32(port_index)

    return _TSIX_PORT_Disable(device, _port_index)


def TSIX_TS_SetConfigItem(device, config_id, data, data_type=c_uint32, data_count=1, data_size=0, print_error=True):
    _TSIX_TS_SetConfigItem = TSI.TSIX_TS_SetConfigItem
    _TSIX_TS_SetConfigItem.argtypes = (TSI_HANDLE, TSI_CONFIG_ID, c_void_p, c_uint)
    _TSIX_TS_SetConfigItem.restype = TSI_RESULT
    if data_size > 0:
        if type(data) == int or type(data) == bool:
            _data = data_type(data)
            result = _TSIX_TS_SetConfigItem(device, config_id, byref(_data), data_size)
    else:
        if type(data) == int or type(data) == bool:
            _data = data_type(data)
            result = _TSIX_TS_SetConfigItem(device, config_id, byref(_data), sizeof(_data))
        elif type(data) == list or type(data) == bytearray:
            _data = (data_type * data_count)(*data)
            result = _TSIX_TS_SetConfigItem(device, config_id, byref(_data), sizeof(_data))
        elif type(data) == str:
            _data = create_string_buffer(data_count)
            _data.value = str.encode(data)
            result = _TSIX_TS_SetConfigItem(device, config_id, byref(_data), sizeof(_data))
        elif str(type(data)).find('WINFUNCTYPE') != -1 or str(type(data)).find('CFUNCTYPE') != -1:
            result = _TSIX_TS_SetConfigItem(device, config_id, data, sizeof(data))
        else:
            result = TSI_ERROR_NOT_IMPLEMENTED

    if print_error:
        assert (not _assert_tsi_success or result >= TSI_SUCCESS), \
            'TSIX_TS_SetConfigItem({device:#x}, {config_id:#x}, {data}, {data_type}, {data_count}) returned {result}. '\
            '\nDescription:{descript}'.format(**locals(), descript=show_error(result))

    return result


def TSIX_TS_GetConfigItem(device, config_id, data_type, data_count=1):
    _TSIX_TS_GetConfigItem = TSI.TSIX_TS_GetConfigItem
    _TSIX_TS_GetConfigItem.argtypes = (TSI_HANDLE, TSI_CONFIG_ID, c_void_p, c_uint)
    _TSIX_TS_GetConfigItem.restype = TSI_RESULT

    if data_type is None:
        rv = _TSIX_TS_GetConfigItem(device, config_id, data_type, data_count)
        result = rv,
    elif data_count > 1:
        _data = (data_type * data_count)()
        rv = _TSIX_TS_GetConfigItem(device, config_id, _data, sizeof(data_type) * data_count)
        result = rv, _data, data_count
    else:
        _data = data_type(0)
        rv = _TSIX_TS_GetConfigItem(device, config_id, byref(_data), sizeof(_data))
        result = rv, _data.value

    assert (not _assert_tsi_success or rv >= TSI_SUCCESS), \
        'TSIX_TS_GetConfigItem({device:#x}, {config_id:#x}, {data_type}, {data_count}) returned {rv}'.format(**locals())

    return result


def TSI_MISC_GetErrorDescription(error):
    _TSI_MISC_GetErrorDescription = TSI.TSI_MISC_GetErrorDescription
    _TSI_MISC_GetErrorDescription.argtypes = (TSI_RESULT, c_char_p, c_uint)
    _TSI_MISC_GetErrorDescription.restype = TSI_RESULT

    err_msg_size = 256
    err_msg = create_string_buffer(err_msg_size)
    result = _TSI_MISC_GetErrorDescription(error, err_msg, err_msg_size)

    return result, from_cstr(err_msg)


def TSIX_PORT_Select(device: TSI_HANDLE, port):
    _TSIX_PORT_Select = TSI.TSIX_PORT_Select
    _TSIX_PORT_Select.argtypes = (TSI_HANDLE, TSI_LOGICAL_PORT)
    _TSIX_PORT_Select.restype = TSI_RESULT

    return _TSIX_PORT_Select(device, port)


def TSIX_PORT_Deselect(device, port):
    _TSIX_PORT_Deselect = TSI.TSIX_PORT_Deselect
    _TSIX_PORT_Deselect.argtypes = (TSI_HANDLE, TSI_LOGICAL_PORT)
    _TSIX_PORT_Deselect.restype = TSI_RESULT

    return _TSIX_PORT_Deselect(device, port)


def TSIX_TS_RunTest(device: TSI_HANDLE, test_id: int):
    _TSIX_TS_RunTest = TSI.TSIX_TS_RunTest
    _TSIX_TS_RunTest.argtypes = (TSI_HANDLE, TSI_TEST_ID)
    _TSIX_TS_RunTest.restype = TSI_RESULT

    result = _TSIX_TS_RunTest(device, c_uint(test_id))

    assert (not _assert_tsi_success or result >= TSI_SUCCESS), \
        'TSIX_TS_SetConfigItem({device:#x}, {config_id:#x}, {data}, {data_type}, {data_count}) returned {result}. ' \
        '\nDescription:{descript}'.format(**locals(), descript=show_error(result))

    return result


def TSIX_PORT_GetTestCount(device: TSI_HANDLE, port: TSI_LOGICAL_PORT):
    _TSIX_PORT_GetTestCount = TSI.TSIX_PORT_GetTestCount
    _TSIX_PORT_GetTestCount.argtypes = (TSI_HANDLE, TSI_LOGICAL_PORT)
    _TSIX_PORT_GetTestCount.restype = TSI_RESULT

    return _TSIX_PORT_GetTestCount(device, port)


def TSIX_PORT_GetTestInfo(device: TSI_HANDLE, port: TSI_LOGICAL_PORT, test_index: int):
    _TSIX_PORT_GetTestInfo = TSI.TSIX_PORT_GetTestInfo
    _TSIX_PORT_GetTestInfo.argtypes = (TSI_HANDLE, TSI_LOGICAL_PORT, c_int, POINTER(TSI_TEST_ID), POINTER(c_int),
                                       c_char_p, c_uint)
    _TSIX_PORT_GetTestInfo.restype = TSI_RESULT

    msg_size = c_uint(1024)
    test_id = c_uint(0)
    msg_buffer = create_string_buffer(msg_size.value)
    test_flags = c_int(0)

    result = _TSIX_PORT_GetTestInfo(device, port, test_index, byref(test_id), byref(test_flags), msg_buffer, msg_size)
    assert (not _assert_tsi_success or result >= TSI_SUCCESS)

    return test_id.value, test_flags.value, from_cstr(msg_buffer)


def TSIX_STLOG_WaitMessage(device: TSI_HANDLE, max_wait: int):
    _TSIX_STLOG_WaitMessage = TSI.TSIX_STLOG_WaitMessage
    _TSIX_STLOG_WaitMessage.argtypes = (TSI_HANDLE, c_int)
    _TSIX_STLOG_WaitMessage.restype = TSI_RESULT

    return _TSIX_STLOG_WaitMessage(device, c_int(max_wait))


def TSIX_STLOG_GetMessageData(device: TSI_HANDLE):
    _TSIX_STLOG_GetMessageData = TSI.TSIX_STLOG_GetMessageData
    _TSIX_STLOG_GetMessageData.argtypes = (TSI_HANDLE, c_char_p, c_uint, POINTER(c_uint))
    _TSIX_STLOG_GetMessageData.restype = TSI_RESULT

    msg_size = c_uint(512)
    out_size = c_uint(0)
    msg_buffer = create_string_buffer(msg_size.value)

    result = _TSIX_STLOG_GetMessageData(device, msg_buffer, msg_size, byref(out_size))

    return result, from_cstr(msg_buffer), out_size.value


def TSI_ParseEvent(data, to_dict=False):
    _TSI_ParseEvent = TSI.TSI_ParseEvent
    _TSI_ParseEvent.argtypes = (POINTER(c_byte), c_int, POINTER(c_ulonglong), c_char_p, c_int, c_char_p, c_int, c_char_p, c_int, c_char_p, c_int)
    _TSI_ParseEvent.restype = TSI_RESULT

    event_data = (c_byte * (len(data) - 12))(*data[12:])
    type_str_max_size = 128
    brief_str_max_size = 256
    content_str_max_size = 4096
    event_source_str_max_size = 64

    typeStr = create_string_buffer(type_str_max_size)
    briefStr = create_string_buffer(brief_str_max_size)
    contentStr = create_string_buffer(content_str_max_size)
    eventSourceStr = create_string_buffer(event_source_str_max_size)
    timestamp = c_ulonglong(0)

    result = _TSI_ParseEvent(event_data, c_int(len(data) - 12), byref(timestamp), typeStr, type_str_max_size, briefStr, brief_str_max_size,
                   contentStr, content_str_max_size, eventSourceStr, event_source_str_max_size)

    if to_dict:
        return result, \
               {
                   'timestamp': timestamp.value,
                   'type': from_cstr(typeStr),
                   'brief': from_cstr(briefStr),
                   'content': from_cstr(contentStr),
                   'source': from_cstr(eventSourceStr),
                   'data': data[12:]
               }
    else:
        return result, timestamp.value, from_cstr(typeStr), from_cstr(briefStr), from_cstr(contentStr), from_cstr(eventSourceStr), data[12:]


def TSI_TST_RunTest(device, config_script, test_id):
    _TSI_TST_RunTest = TSI.TSI_TST_RunTest
    _TSI_TST_RunTest.argtypes = (c_char_p, c_char_p, c_int, POINTER(c_bool), POINTER(c_bool), c_char_p, c_int, c_char_p, c_int)
    _TSI_TST_RunTest.restype = None

    # cfg_script = create_string_buffer(config_script.encode('ascii'))
    passed = c_bool()
    error = c_bool()

    error_msg = create_string_buffer(1024)
    report_text = create_string_buffer(64000)

    _TSI_TST_RunTest(device, config_script, c_int(test_id), byref(passed), byref(error), error_msg, 1024, report_text, 64000)
    return TSI_SUCCESS, passed.value, error.value, error_msg.value, report_text.value


def TSI_TST_Init(setup_script):
    _TSI_TST_Init = TSI.TSI_TST_Init
    _TSI_TST_Init.argtypes = (c_char_p, POINTER(c_bool), POINTER(c_long), c_char_p, c_int)
    _TSI_TST_Init.restype = None

    set_script = create_string_buffer(bytes(setup_script), len(bytes(setup_script)))
    error = c_bool()
    error_code = c_long()
    error_msg = create_string_buffer(1024)

    _TSI_TST_Init(set_script, byref(error), byref(error_code), error_msg, 1024)
    return TSI_SUCCESS, error.value, error_code.value, error_msg.value


def TSI_DPCD_RegNames(reg_addr, just_name=True):
    _TSI_DPCD_RegNames = TSI.TSI_DPCD_RegNames
    _TSI_DPCD_RegNames.argtypes = (c_int, c_bool, c_char_p, c_int)
    _TSI_DPCD_RegNames.restype = TSI_RESULT

    output_str = create_string_buffer(64000)
    raddr = c_int(reg_addr)
    jname = c_bool(just_name)

    result = _TSI_DPCD_RegNames(raddr, jname, output_str, 64000)

    return result, str(output_str.value.decode('utf-8'))


def TSI_DPCD_RegInfoData(reg_addr, reg_data: int, just_name=False):
    _TSI_DPCD_RegInfoData = TSI.TSI_DPCD_RegInfoData
    _TSI_DPCD_RegInfoData.argtypes = (c_int, c_byte, c_bool, c_char_p, c_int)
    _TSI_DPCD_RegInfoData.restype = TSI_RESULT

    output_str = create_string_buffer(64000)
    raddr = c_int(reg_addr)
    rdata = c_byte(reg_data)
    jname = c_bool(just_name)

    result = _TSI_DPCD_RegInfoData(raddr, rdata, jname, output_str, 64000)

    return result, str(output_str.value.decode('utf-8'))

def TSI_CreateEventParser(timestam_res: int = 100):
    _TSI_CreateEventParser = TSI.TSI_CreateEventParser
    _TSI_CreateEventParser.argtypes = (POINTER(TSI_RESULT), c_uint32)
    _TSI_CreateEventParser.restype = TSI_PARSER

    result = c_int(TSI_SUCCESS)
    parser = _TSI_CreateEventParser(byref(result), c_uint32(timestam_res))

    return parser


def TSI_RemoveEventParser(parser):
    _TSI_RemoveEventParser = TSI.TSI_RemoveEventParser
    _TSI_RemoveEventParser.argtypes = (TSI_PARSER,)
    _TSI_RemoveEventParser.restype = TSI_RESULT

    return _TSI_RemoveEventParser(parser)


def TSI_GetParsedEventData(parser, data, to_dict=False):
    _TSI_GetParsedEventData = TSI.TSI_GetParsedEventData
    _TSI_GetParsedEventData.argtypes = (TSI_PARSER, POINTER(c_byte), c_int, POINTER(c_ulonglong), c_char_p, c_int, c_char_p, c_int, c_char_p, c_int, c_char_p, c_int)
    _TSI_GetParsedEventData.restype = TSI_RESULT

    event_data = (c_byte * (len(data) - 12))(*data[12:])
    type_str_max_size = 128
    brief_str_max_size = 256
    content_str_max_size = 4096
    event_source_str_max_size = 64

    typeStr = create_string_buffer(type_str_max_size)
    briefStr = create_string_buffer(brief_str_max_size)
    contentStr = create_string_buffer(content_str_max_size)
    eventSourceStr = create_string_buffer(event_source_str_max_size)
    timestamp = c_ulonglong(0)

    result = _TSI_GetParsedEventData(parser, event_data, c_int(len(data) - 12), byref(timestamp), typeStr, type_str_max_size, briefStr,
                             brief_str_max_size,
                             contentStr, content_str_max_size, eventSourceStr, event_source_str_max_size)

    if to_dict:
        return result, \
               {
                   'timestamp': timestamp.value,
                   'type': from_cstr(typeStr),
                   'brief': from_cstr(briefStr),
                   'content': from_cstr(contentStr),
                   'source': from_cstr(eventSourceStr),
                   'data': data[12:]
               }
    else:
        return result, timestamp.value, from_cstr(typeStr), from_cstr(briefStr), from_cstr(contentStr), from_cstr(
            eventSourceStr), data[12:]


def TSI_DEV_GetParameterCount(device_id):
    _TSI_DEV_GetParameterCount = TSI.TSI_DEV_GetParameterCount
    _TSI_DEV_GetParameterCount.argtypes = (TSI_DEVICE_ID,)
    _TSI_DEV_GetParameterCount.restype = TSI_RESULT

    return _TSI_DEV_GetParameterCount(device_id)


def TSI_DEV_GetParameterID(device_id, parameter_index):
    _TSI_DEV_GetParameterID = TSI.TSI_DEV_GetParameterID
    _TSI_DEV_GetParameterID.argtypes = (TSI_DEVICE_ID, c_int, POINTER(TSI_CONFIG_ID), POINTER(c_uint))
    _TSI_DEV_GetParameterID.restype = TSI_RESULT

    param_id = TSI_CONFIG_ID()
    param_flags = c_uint()

    result = _TSI_DEV_GetParameterID(device_id, parameter_index, byref(param_id), byref(param_flags))

    return result, param_id.value, param_flags.value


def TSI_DEV_SetSearchMask(required_caps, unallowed_caps):
    _TSI_DEV_SetSearchMask = TSI.TSI_DEV_SetSearchMask
    _TSI_DEV_SetSearchMask.argtypes = (TSI_DEVICE_CAPS, TSI_DEVICE_CAPS)
    _TSI_DEV_SetSearchMask.restype = TSI_RESULT

    return _TSI_DEV_SetSearchMask(required_caps, unallowed_caps)


def TSI_DEV_GetDeviceInfo(device_id):
    _TSI_DEV_GetDeviceInfo = TSI.TSI_DEV_GetDeviceInfo
    _TSI_DEV_GetDeviceInfo.argtypes = (TSI_DEVICE_ID, POINTER(TSI_DEVICE_CAPS))
    _TSI_DEV_GetDeviceInfo.restype = TSI_RESULT

    device_caps = TSI_DEVICE_CAPS()
    result = _TSI_DEV_GetDeviceInfo(device_id, byref(device_caps))

    return result, device_caps.value


def TSIX_VIN_GetParameterCount(device, input_id):
    _TSIX_VIN_GetParameterCount = TSI.TSIX_VIN_GetParameterCount
    _TSIX_VIN_GetParameterCount.argtypes = (TSI_HANDLE, TSI_INPUT_ID)
    _TSIX_VIN_GetParameterCount.restype = TSI_RESULT

    return _TSIX_VIN_GetParameterCount(device, input_id)


def TSIX_VIN_GetParameterID(device, input_id, param_id, param_flags):
    _TSIX_VIN_GetParameterID = TSI.TSIX_VIN_GetParameterID
    _TSIX_VIN_GetParameterID.argtypes = (TSI_HANDLE, TSI_INPUT_ID, c_int, TSI_CONFIG_ID, POINTER(c_uint))
    _TSIX_VIN_GetParameterID.restype = TSI_RESULT

    return _TSIX_VIN_GetParameterID(device, input_id, param_id, param_flags)


def TSIX_VIN_GetInputCount(device):
    _TSIX_VIN_GetInputCount = TSI.TSIX_VIN_GetInputCount
    _TSIX_VIN_GetInputCount.argtypes = (TSI_HANDLE,)
    _TSIX_VIN_GetInputCount.restype = TSI_RESULT

    return _TSIX_VIN_GetInputCount(device)


def TSIX_VIN_GetInputName(device, input_id):
    _TSIX_VIN_GetInputName = TSI.TSIX_VIN_GetInputName
    _TSIX_VIN_GetInputName.argtypes = (TSI_HANDLE, TSI_INPUT_ID, c_char_p, c_uint)
    _TSIX_VIN_GetInputName.restype = TSI_RESULT

    name_string_max_len = 256
    input_name_string = create_string_buffer(name_string_max_len)

    result = _TSIX_VIN_GetInputName(device, input_id, input_name_string, name_string_max_len)

    return result, from_cstr(input_name_string)


def TSIX_VIN_Disable(device):
    _TSIX_VIN_Disable = TSI.TSIX_VIN_Disable
    _TSIX_VIN_Disable.argtypes = (TSI_HANDLE,)
    _TSIX_VIN_Disable.restype = TSI_RESULT

    return _TSIX_VIN_Disable(device)


def TSIX_VIN_Enable(device, flags):
    _TSIX_VIN_Enable = TSI.TSIX_VIN_Enable
    _TSIX_VIN_Enable.argtypes = (TSI_HANDLE, TSI_FLAGS)
    _TSIX_VIN_Enable.restype = TSI_RESULT

    return _TSIX_VIN_Enable(device, flags)


def TSIX_VIN_Select(device, output_id):
    _TSIX_VIN_Select = TSI.TSIX_VIN_Select
    _TSIX_VIN_Select.argtypes = (TSI_HANDLE, TSI_OUTPUT_ID)
    _TSIX_VIN_Select.restype = TSI_RESULT

    return _TSIX_VIN_Select(device, output_id)


def TSIX_VOUT_Disable(device):
    _TSIX_VOUT_Disable = TSI.TSIX_VOUT_Disable
    _TSIX_VOUT_Disable.argtypes = (TSI_HANDLE,)
    _TSIX_VOUT_Disable.restype = TSI_RESULT

    return _TSIX_VOUT_Disable(device)


def TSIX_VOUT_Enable(device, flag):
    _TSIX_VOUT_Enable = TSI.TSIX_VOUT_Enable
    _TSIX_VOUT_Enable.argtypes = (TSI_HANDLE, TSI_FLAGS)
    _TSIX_VOUT_Enable.restype = TSI_RESULT

    return _TSIX_VOUT_Enable(device, flag)


def TSIX_VOUT_GetOutputCount(device):
    _TSIX_VOUT_GetOutputCount = TSI.TSIX_VOUT_GetOutputCount
    _TSIX_VOUT_GetOutputCount.argtypes = (TSI_HANDLE,)
    _TSIX_VOUT_GetOutputCount.restype = TSI_RESULT

    return _TSIX_VOUT_GetOutputCount(device)


def TSIX_VOUT_GetOutputName(device, output_id):
    _TSIX_VOUT_GetOutputName = TSI.TSIX_VOUT_GetOutputName
    _TSIX_VOUT_GetOutputName.argtypes = (TSI_HANDLE, TSI_OUTPUT_ID, c_char_p, c_uint)
    _TSIX_VOUT_GetOutputName.restype = TSI_RESULT

    name_string_max_len = 256
    output_name_string = create_string_buffer(name_string_max_len)

    result = _TSIX_VOUT_GetOutputName(device, output_id, output_name_string, name_string_max_len)

    return result, from_cstr(output_name_string)


def TSIX_VOUT_GetParameterCount(device, output_id):
    _TSIX_VOUT_GetParameterCount = TSI.TSIX_VOUT_GetParameterCount
    _TSIX_VOUT_GetParameterCount.argtypes = (TSI_HANDLE, TSI_OUTPUT_ID)
    _TSIX_VOUT_GetParameterCount.restype = TSI_RESULT

    return _TSIX_VOUT_GetParameterCount(device, output_id)


def TSIX_VOUT_GetParameterID(device, output_id, parameter_index):
    _TSIX_VOUT_GetParameterID = TSI.TSIX_VOUT_GetParameterID
    _TSIX_VOUT_GetParameterID.argtypes = (TSI_HANDLE, TSI_OUTPUT_ID, c_int, POINTER(TSI_CONFIG_ID), POINTER(c_uint))
    _TSIX_VOUT_GetParameterID.restype = TSI_RESULT

    config_id = c_uint()
    param_flags = c_uint()

    return _TSIX_VOUT_GetParameterID(device, output_id, parameter_index, byref(config_id), byref(param_flags))


def TSIX_VOUT_Select(device, output_id):
    _TSIX_VOUT_Select = TSI.TSIX_VOUT_Select
    _TSIX_VOUT_Select.argtypes = (TSI_HANDLE, TSI_OUTPUT_ID, c_int)
    _TSIX_VOUT_Select.restype = TSI_RESULT

    return _TSIX_VOUT_Select(device, output_id)


def TSIX_VPREV_SetWindowHandle(device, container):
    _TSIX_VPREV_SetWindowHandle = TSI.TSIX_VPREV_SetWindowHandle
    _TSIX_VPREV_SetWindowHandle.argtypes = (TSI_HANDLE, OS_WINDOW_ID)
    _TSIX_VPREV_SetWindowHandle.restype = TSI_RESULT

    return _TSIX_VPREV_SetWindowHandle(device, container)


def TSIX_APREV_SetWindowHandle(device, container):
    _TSIX_APREV_SetWindowHandle = TSI.TSIX_APREV_SetWindowHandle
    _TSIX_APREV_SetWindowHandle.argtypes = (TSI_HANDLE, OS_WINDOW_ID)
    _TSIX_APREV_SetWindowHandle.restype = TSI_RESULT

    return _TSIX_APREV_SetWindowHandle(device, container)


def TSIX_APREV_SelectDevice(device, audio_device_id):
    _TSIX_APREV_SelectDevice = TSI.TSIX_APREV_SelectDevice
    _TSIX_APREV_SelectDevice.argtypes = (TSI_HANDLE, TSI_AUDIO_DEVICE_ID)
    _TSIX_APREV_SelectDevice.restype = TSI_RESULT

    return _TSIX_APREV_SelectDevice(device, audio_device_id)


def TSIX_TS_GetTestCount(device):
    _TSIX_TS_GetTestCount = TSI.TSIX_TS_GetTestCount
    _TSIX_TS_GetTestCount.argtypes = (TSI_HANDLE,)
    _TSIX_TS_GetTestCount.restype = TSI_RESULT

    return _TSIX_TS_GetTestCount(device)


def TSIX_TS_GetTestInfo(device, test_index):
    _TSIX_TS_GetTestInfo = TSI.TSIX_TS_GetTestInfo
    _TSIX_TS_GetTestInfo.argtypes = (TSI_HANDLE, c_int, POINTER(TSI_TEST_ID), c_char_p, c_int)
    _TSIX_TS_GetTestInfo.restype = TSI_RESULT

    test_name_max_length = 256
    test_id = TSI_TEST_ID()
    test_name = create_string_buffer(test_name_max_length)

    result = _TSIX_TS_GetTestInfo(device, c_int(test_index), byref(test_id), test_name, test_name_max_length)

    return result, from_cstr(test_name)


def TSIX_TS_GetTestParameterCount(device, test_id):
    _TSIX_TS_GetTestParameterCount = TSI.TSIX_TS_GetTestParameterCount
    _TSIX_TS_GetTestParameterCount.argtypes = (TSI_HANDLE, TSI_TEST_ID)
    _TSIX_TS_GetTestParameterCount.restype = TSI_RESULT

    return _TSIX_TS_GetTestParameterCount(device, test_id)


def TSIX_TS_GetTestParameterID(device, test_id, param_index):
    _TSIX_TS_GetTestParameterID = TSI.TSIX_TS_GetTestParameterID
    _TSIX_TS_GetTestParameterID.argtypes = (TSI_HANDLE, TSI_TEST_ID, c_int, POINTER(TSI_CONFIG_ID), POINTER(c_uint))
    _TSIX_TS_GetTestParameterID.restype = TSI_RESULT

    config_id = TSI_CONFIG_ID()
    param_flags = c_uint()

    result = _TSIX_TS_GetTestParameterID(device, test_id, c_int(param_index), byref(config_id), byref(param_flags))

    return result, config_id.value, param_flags.value


def TSIX_TS_Clear(device):
    _TSIX_TS_Clear = TSI.TSIX_TS_Clear
    _TSIX_TS_Clear.argtypes = (TSI_HANDLE,)
    _TSIX_TS_Clear.restype = TSI_RESULT

    return _TSIX_TS_Clear(device)


def TSIX_TS_SaveConfig(device, filename):
    _TSIX_TS_SaveConfig = TSI.TSIX_TS_SaveConfig
    _TSIX_TS_SaveConfig.argtypes = (TSI_HANDLE, c_char_p)
    _TSIX_TS_SaveConfig.restype = TSI_RESULT

    name = create_string_buffer(filename.encode())

    return _TSIX_TS_SaveConfig(device, name)


def TSIX_TS_LoadConfig(device, filename: str):
    _TSIX_TS_LoadConfig = TSI.TSIX_TS_LoadConfig
    _TSIX_TS_LoadConfig.argtypes = (TSI_HANDLE, c_char_p)
    _TSIX_TS_LoadConfig.restype = TSI_RESULT

    name = create_string_buffer(filename.encode())

    return _TSIX_TS_LoadConfig(device, name)


def TSIX_TS_CaptureReference(device, required_matches, ref_index):
    _TSIX_TS_CaptureReference = TSI.TSIX_TS_CaptureReference
    _TSIX_TS_CaptureReference.argtypes = (TSI_HANDLE, c_int, c_int)
    _TSIX_TS_CaptureReference.restype = TSI_RESULT

    return _TSIX_TS_CaptureReference(device, c_int(required_matches), c_int(ref_index))


def TSIX_TS_WaitInputSignal(device, max_wait):
    _TSIX_TS_WaitInputSignal = TSI.TSIX_TS_WaitInputSignal
    _TSIX_TS_WaitInputSignal.argtypes = (TSI_HANDLE, c_int)
    _TSIX_TS_WaitInputSignal.restype = TSI_RESULT

    return _TSIX_TS_WaitInputSignal(device, c_int(max_wait))


def TSIX_MISC_SaveReference(device, filename, ref_index, format_id):
    _TSIX_MISC_SaveReference = TSI.TSIX_MISC_SaveReference
    _TSIX_MISC_SaveReference.argtypes = (TSI_HANDLE, c_char_p, c_uint, TSI_FRAME_FORMAT_ID)
    _TSIX_MISC_SaveReference.restype = TSI_RESULT

    return _TSIX_MISC_SaveReference(device, create_string_buffer(filename.encode()), c_uint(ref_index), format_id)


def TSIX_MISC_LoadReference(device, filename, ref_index):
    _TSIX_MISC_LoadReference = TSI.TSIX_MISC_LoadReference
    _TSIX_MISC_LoadReference.argtypes = (TSI_HANDLE, c_char_p, c_uint)
    _TSIX_MISC_LoadReference.restype = TSI_RESULT

    return _TSIX_MISC_LoadReference(device, create_string_buffer(filename.encode()), c_uint(ref_index))


def TSIX_MISC_SetOption(device, option_id, option_value):
    _TSIX_MISC_SetOption = TSI.TSIX_MISC_SetOption
    _TSIX_MISC_SetOption.argtypes = (TSI_HANDLE, TSI_OPTION_ID, c_int)
    _TSIX_MISC_SetOption.restype = TSI_RESULT

    return _TSIX_MISC_SetOption(device, option_id, c_int(option_value))


def TSIX_STLOG_GetMessageCount(device):
    _TSIX_STLOG_GetMessageCount = TSI.TSIX_STLOG_GetMessageCount
    _TSIX_STLOG_GetMessageCount.argtypes = (TSI_HANDLE,)
    _TSIX_STLOG_GetMessageCount.restype = TSI_RESULT

    return _TSIX_STLOG_GetMessageCount(device)


def TSIX_STLOG_Clear(device):
    _TSIX_STLOG_Clear = TSI.TSIX_STLOG_Clear
    _TSIX_STLOG_Clear.argtypes = (TSI_HANDLE,)
    _TSIX_STLOG_Clear.restype = TSI_RESULT

    return _TSIX_STLOG_Clear(device)


def TSIX_REP_BeginLogRecord(device, target_file, dut_info):
    _TSIX_REP_BeginLogRecord = TSI.TSIX_REP_BeginLogRecord
    _TSIX_REP_BeginLogRecord.argtypes = (TSI_HANDLE, c_char_p, c_char_p)
    _TSIX_REP_BeginLogRecord.restype = TSI_RESULT

    return _TSIX_REP_BeginLogRecord(device, create_string_buffer(target_file.encode()),
                                    create_string_buffer(dut_info.encode()))


def TSIX_REP_EndLogRecord(device):
    _TSIX_REP_EndLogRecord = TSI.TSIX_REP_EndLogRecord
    _TSIX_REP_EndLogRecord.argtypes = (TSI_HANDLE,)
    _TSIX_REP_EndLogRecord.restype = TSI_RESULT

    return _TSIX_REP_EndLogRecord(device)
