from ctypes import *
from enum import IntEnum
from ctypes import wintypes

UICL_RESULT = c_int32

UICL_SUCCESS = 0
UICL_ERROR_UNKNOWN = -1
UICL_ERROR_NULL_IMAGE = -2
UICL_ERROR_INVALID_COLORSPACE = -3
UICL_ERROR_CONVERSION_NOT_SUPPORTED = -4


class CtypesEnum(IntEnum):
    @classmethod
    def from_param(cls, obj):
        return int(obj)


class UICL_Colorspace(CtypesEnum):
    Colorspace_Unknown = 0,
    Colorspace_RGB = 1,
    Colorspace_YCbCr = 2,
    Colorspace_Raw = 3,
    Colorspace_Y = 4,
    Colorspace_MaxValue = 5


class UICL_Sampling(CtypesEnum):
    Sampling_Unknown = 0,
    Sampling_444 = 1,
    Sampling_422 = 2,
    Sampling_420 = 3,
    Sampling_MaxValue = 4


class UICL_Colorimetry(CtypesEnum):
    Colorimetry_Unknown = 0,
    Colorimetry_RGB = 1,
    Colorimetry_ITU_R_BT601 = 2,
    Colorimetry_ITU_R_BT709 = 3,
    Colorimetry_ITU_R_BT2020 = 4,
    Colorimetry_MaxValue = 5


class UICL_Packing(CtypesEnum):
    Packing_Unknown = 0,
    Packing_Planar = 1,
    Packing_SemiPlanar = 2,
    Packing_Packed = 3,
    Packing_32bit = 4,
    Packing_48bit = 5,
    Packing_MaxValue = 6


class UICL_ComponentOrder(CtypesEnum):
    Order_Unknown = 0,
    Order_UCDTX_HI = 1,
    Order_UCDTX_LO = 2,
    Order_UCDRX = 3,
    Order_RGB = 4,
    Order_RGBA = 5,
    Order_BGR = 6,
    Order_BGRA = 7,
    Order_YCbCr = 8,
    Order_CbYCr = 9,
    Order_CrYCb = 10,
    Order_CbY0CrY1 = 11,
    Order_PlainRaw = 12,
    Order_MaxValue = 13


class UICL_Alignment(CtypesEnum):
    Alignment_Unknown = 0,
    Alignment_MSB = 1,
    Alignment_LSB = 2,
    Alignment_MaxValue = 3


class UICL_Endianness(CtypesEnum):
    Endianness_Unknown = 0,
    Endianness_Big = 1,
    Endianness_Little = 2,
    Endianness_MaxValue = 3


class UICL_ImageParameters(Structure):
    _fields_ = [
        ('Width',           c_uint32),
        ('Height',          c_uint32),
        ('BitsPerColor',    c_uint8),
        ('Colorspace',      c_int),
        ('Colorimetry',     c_int),
        ('Sampling',        c_int),
        ('Packing',         c_int),
        ('ComponentOrder',  c_int),
        ('Alignment',       c_int),
        ('Endianness',      c_int),
        ('IsMonochrome',    c_bool),
        ('Crop',            c_bool),
    ]


class ImageFileFormat(CtypesEnum):
    FILE_FORMAT_BMP = 0,
    FILE_FORMAT_BIN = 1


class UICL_Image(Structure):
    _fields_ = [
        ('Parameters',  UICL_ImageParameters),
        ('DataPtr',     POINTER(c_uint8)),
        ('DataSize',    c_uint64)
    ]


parse_attributes_bpc = [6, 8, 10, 12, 16, 7, 14, 0]

parse_attributes_packing = [UICL_Packing.Packing_32bit,
                            UICL_Packing.Packing_48bit,
                            UICL_Packing.Packing_Unknown,
                            UICL_Packing.Packing_Unknown]

parse_attributes_sampling = [UICL_Sampling.Sampling_444,
                             UICL_Sampling.Sampling_422,
                             UICL_Sampling.Sampling_444,
                             UICL_Sampling.Sampling_420,
                             UICL_Sampling.Sampling_444,
                             UICL_Sampling.Sampling_Unknown,
                             UICL_Sampling.Sampling_Unknown,
                             UICL_Sampling.Sampling_Unknown]

parse_attributes_colorspace = [UICL_Colorspace.Colorspace_RGB,
                               UICL_Colorspace.Colorspace_YCbCr,
                               UICL_Colorspace.Colorspace_YCbCr,
                               UICL_Colorspace.Colorspace_YCbCr,
                               UICL_Colorspace.Colorspace_Y,
                               UICL_Colorspace.Colorspace_Raw,
                               UICL_Colorspace.Colorspace_Unknown,
                               UICL_Colorspace.Colorspace_Unknown]

parse_attributes_colorimetry = [UICL_Colorimetry.Colorimetry_Unknown,
                                UICL_Colorimetry.Colorimetry_ITU_R_BT601,
                                UICL_Colorimetry.Colorimetry_ITU_R_BT709,
                                UICL_Colorimetry.Colorimetry_Unknown]

parse_attributes_ecolorimetry = [UICL_Colorimetry.Colorimetry_Unknown,
                                 UICL_Colorimetry.Colorimetry_Unknown,
                                 UICL_Colorimetry.Colorimetry_Unknown,
                                 UICL_Colorimetry.Colorimetry_Unknown,
                                 UICL_Colorimetry.Colorimetry_Unknown,
                                 UICL_Colorimetry.Colorimetry_ITU_R_BT2020,
                                 UICL_Colorimetry.Colorimetry_ITU_R_BT2020,
                                 UICL_Colorimetry.Colorimetry_ITU_R_BT601]

dict_colorspace = {0: "Unknown", 1: "RGB", 2: "YCbCr", 3: "Raw", 4: "MaxValue"}
dict_sampling = {0: "Unknown", 1: "4:4:4", 2: "4:2:2", 3: "4:2:0"}
dict_colorimetry = {0: "Unknown", 1: "RGB", 2: "ITU_R_BT601", 3: "ITU_R_BT709", 4: "ITU_R_BT2020"}
dict_packing = {0: "Unknown", 1: "Planar", 2: "SemiPlanar", 3: "Packed", 4: "32bit", 5: "48bit"}
dict_component_oreder = {0: "Unknown", 1: "UCDTX_HI", 2: "UCDTX_LO", 3: "UCDRX", 4: "RGB", 5: "RGBA", 6: "BGR",
                         7: "BGRA", 8: "YCbCr", 9: "CbYCr", 10: "CrYCb", 11: "CbY0CrY1", 12: "PlainRaw"}
dict_alignment = {0: "Unknown", 1: "MSB", 2: "LSB"}
dict_endianness = {0: "Unknown", 1: "Big", 2: "Little"}

uicl_errors = {-1: "Error unknown", -2: "Error null image", -3: "Invalid colorspace", -4: "Conversion not supported",
               -5: "Error in conversion", -6: "Unsupported format", -7: "Invalid parameters"}
