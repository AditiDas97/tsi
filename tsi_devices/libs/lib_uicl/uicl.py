from .uicl_types import *
import os
import sys


UICL_CURRENT_VERSION = 1
UICL = None
WIN_UICL_PATH = __file__[:-8] + '\\UICL.dll'

if not os.path.isfile(WIN_UICL_PATH):
    WIN_UICL_PATH = 'C:\\Program Files\\Unigraf\\Unigraf UCD Tools\\UICL.dll'

dll_path = WIN_UICL_PATH
try:
    UICL = windll.LoadLibrary(dll_path)
except OSError:
    print('ERROR({}): {}'.format(GetLastError(), dll_path))
    if GetLastError() == 193:
        print('Perhaps you are using a 64-bit python interpreter along with a 32-bit library, or vice versa.'
              ' Need the same.')


def to_cstr(src_str):
    return c_char_p(src_str.encode('utf-8'))


def UICL_GetRequiredBufferSize(dest_image: UICL_Image):
    _UICL_GetRequiredBufferSize = UICL.UICL_GetRequiredBufferSize
    _UICL_GetRequiredBufferSize.argtypes = [POINTER(UICL_Image)]
    _UICL_GetRequiredBufferSize.restype = UICL_RESULT

    result = _UICL_GetRequiredBufferSize(byref(dest_image))
    return result, dest_image


def UICL_Convert(src_image: UICL_Image, dest_image: UICL_Image):
    _UICL_Convert = UICL.UICL_Convert
    _UICL_Convert.argtypes = [POINTER(UICL_Image), POINTER(UICL_Image)]
    _UICL_Convert.restype = UICL_RESULT

    result = _UICL_Convert(byref(src_image), byref(dest_image))
    return result, dest_image


def UICL_SaveToFile(src_image: UICL_Image, file_name, image_file_format):
    _UICL_SaveToFile = UICL.UICL_SaveToFile
    _UICL_SaveToFile.argtypes = [c_char_p, POINTER(UICL_Image), c_int]
    _UICL_SaveToFile.restype = UICL_RESULT

    return _UICL_SaveToFile(to_cstr(file_name), byref(src_image), image_file_format)
