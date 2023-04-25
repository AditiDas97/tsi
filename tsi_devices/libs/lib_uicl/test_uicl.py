import copy
from typing import Any

from . import uicl
from PIL import Image
from ctypes import *


class ImageU:

    def __init__(self, data=None, version=1, width=0, height=0, bpc=0, colorspace=0, sampling=0, packing=0,
                 component_order=0, _alignment=0, endianness=0, monochrome=False, crop=False, colorimetry=0,
                 hdcp_protected=False, hdcp_decrypted=False):
        """

        Parameters
        ----------
        data: bytearray
            Data from file
        version: type c_uint16
        width: type c_uint32
        height: type c_uint32
        bpc: type c_uint8
            Bits per color
        colorspace: type c_int
            Unknown = 0, RGB = 1, YCbCr = 2, Raw = 3, MaxValue = 4
        sampling: type c_int
            Unknown = 0, 444 = 1, 422 = 2, 420 = 3, MaxValue = 4
        packing: type c_int
            Unknown = 0, Planar = 1, SemiPlanar = 2, Packed = 3, MaxValue = 4
        component_order: type c_int
            Unknown = 0, UCDTX_HI = 1, UCDTX_LO = 2, UCDRX = 3, RGB = 4, RGBA = 5, BGR = 6, BGRA = 7, YCbCr = 8,
            CbYCr = 9, CbY0CrY1 = 10, PlainRaw = 11, MaxValue = 12
        _alignment: type c_int
            Unknown = 0, MSB = 1, LSB = 2, MaxValue = 3
        colorimetry: type c_int
            Colorimetry_Unknown = 0, Colorimetry_RGB = 1, Colorimetry_ITU_R_BT601 = 2, Colorimetry_ITU_R_BT709 = 3,
            Colorimetry_ITU_R_BT2020 = 4, Colorimetry_MaxValue = 5
        endianness: type c_int
            Unknown = 0, Big = 1, Little = 2
        monochrome: type c_bool
            True or False
        crop: type c_bool
            True or False
        hdcp_decrypted: type c_bool
            True or False
        hdcp_protected: type c_bool
            True or False
        """
        self.start_timestamp_us = 0
        self.end_timestamp_us = 0
        self.msa = bytearray()
        self.sdp_list = []
        self.type = None
        self.version = version
        self.hdcp_protected = hdcp_protected
        self.hdcp_decrypted = hdcp_decrypted
        self.src_image = uicl.UICL_Image()
        if colorspace in [0, 1, 2, 3, 4]:
            self.colorimetry = colorimetry
        else:
            self.colorimetry = 0
        if width >= 0:
            self.width = width
        else:
            self.width = 0
        if height >= 0:
            self.height = height
        else:
            self.height = 0
        if bpc >= 0:
            self.bpc = bpc
        else:
            self.bpc = 0
        if colorspace in [0, 1, 2, 3, 4]:
            self.colorspace = colorspace
        else:
            self.colorspace = 0
        if sampling in [0, 1, 2, 3, 4]:
            self.sampling = sampling
        else:
            self.sampling = 0
        if packing in [0, 1, 2, 3, 4]:
            self.packing = packing
        else:
            self.packing = 0
        if component_order in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]:
            self.component_order = component_order
        else:
            self.component_order = 0
        if endianness in [0, 1, 2]:
            self.endianness = endianness
        else:
            self.endianness = c_int(0)
        if _alignment in [0, 1, 2, 3]:
            self.alignment = _alignment
        else:
            self.alignment = 0
        self.monochrome = c_bool(monochrome)
        self.crop = c_bool(crop)
        if data is not None:
            self.data_size = len(data)
            self.data_ptr = data
        else:
            self.data_size = None
            self.data_ptr = None

    def __eq__(self, other):
        count = 0
        dict_eq = dict()
        for key in self.__dict__.keys():
            if key == 'data_ptr':
                count_error_pixels = []
                if len(self.__dict__[key]) == len(other.__dict__[key]):
                    for i in range(len(self.__dict__[key])):
                        if self.__dict__[key][i] != other.__dict__[key][i]:
                            print("Bit number {}: {} is not equal to bit {}".format(i, self.__dict__[key][i],
                                                                                    other.__dict__[key][i]))
                            count = 1
                            count_error_pixels.append(i)
                    dict_eq.update({"data_ptr": count_error_pixels})
                else:
                    dict_eq.update({"data_ptr": "Error, different length for arrays!"})
            elif key not in ["start_timestamp_us", "end_timestamp_us", "src_image"]:
                if self.__dict__[key] != other.__dict__[key]:
                    count = 1
                    print(key + ": " + str(self.__dict__[key]) + " != " + str(other.__dict__[key]))
                    dict_eq.update({key: [self.__dict__[key], other.__dict__[key]]})
        if count > 0:
            return False, dict_eq
        else:
            return True, {}

    def add_data(self, data):
        if data is not None:
            self.data_size = len(data)
            self.data_ptr = data

    def setting_src_object(self):
        if self.data_size > 0 and self.data_ptr is not None:
            _src_image_parameters = uicl.UICL_ImageParameters()
            _src_image_parameters.Version = self.version
            _src_image_parameters.Width = self.width
            _src_image_parameters.Height = self.height
            _src_image_parameters.BitsPerColor = self.bpc
            _src_image_parameters.Colorspace = self.colorspace
            _src_image_parameters.ComponentOrder = self.component_order
            _src_image_parameters.Sampling = self.sampling
            _src_image_parameters.Packing = self.packing
            _src_image_parameters.Alignment = self.alignment
            _src_image_parameters.Endianness = self.endianness
            _src_image_parameters.Crop = self.crop
            _src_image_parameters.Colorimetry = self.colorimetry
            _src_image_parameters.IsMonochrome = self.monochrome
            self.src_image.Parameters = _src_image_parameters
            self.src_image.DataSize = self.data_size
            self.src_image.DataPtr = (uicl.c_uint8 * self.src_image.DataSize)(*self.data_ptr)

    def convert(self, width=0, height=0, colorspace=0, sampling=0, bpc=0, component_order=0, packing=0, _alignment=0,
                endianness=0, monochrome=False, crop=False, upscaling_flag=False, colorimetry=1):

        _src_image = uicl.UICL_Image()
        if self.data_size > 0 and self.data_ptr is not None:
            _src_image_parameters = uicl.UICL_ImageParameters()
            _src_image_parameters.Version = self.version
            _src_image_parameters.Width = self.width
            _src_image_parameters.Height = self.height
            _src_image_parameters.BitsPerColor = self.bpc
            _src_image_parameters.Colorspace = self.colorspace
            _src_image_parameters.ComponentOrder = self.component_order
            _src_image_parameters.Sampling = self.sampling
            _src_image_parameters.Packing = self.packing
            _src_image_parameters.Alignment = self.alignment
            _src_image_parameters.Endianness = self.endianness
            _src_image_parameters.Crop = self.crop
            _src_image_parameters.Colorimetry = self.colorimetry
            _src_image_parameters.IsMonochrome = self.monochrome
            _src_image.Parameters = _src_image_parameters
            _src_image.DataSize = self.data_size
            _src_image.DataPtr = (uicl.c_uint8 * _src_image.DataSize)(*self.data_ptr)

        if width < 0:
            width = 0
        if height < 0:
            height = 0
        if bpc < 0:
            bpc = 0
        if colorspace in [0, 1, 2, 3, 4] is False:
            colorspace = 0
        if sampling in [0, 1, 2, 3, 4] is False:
            sampling = 0
        if packing in [0, 1, 2, 3, 4] is False:
            packing = 0
        if component_order in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12] is False:
            component_order = 0
        if endianness in [0, 1, 2] is False:
            endianness = 0
        if _alignment in [0, 1, 2, 3] is False:
            _alignment = 0
        _dest_image = uicl.UICL_Image()
        _dest_image_parameters = uicl.UICL_ImageParameters()
        _dest_image_parameters.Version = 1
        _dest_image_parameters.Width = width
        _dest_image_parameters.Height = height
        _dest_image_parameters.BitsPerColor = bpc
        _dest_image_parameters.Colorspace = colorspace
        _dest_image_parameters.ComponentOrder = component_order
        _dest_image_parameters.Sampling = sampling
        _dest_image_parameters.Packing = packing
        _dest_image_parameters.Alignment = _alignment
        _dest_image_parameters.Endianness = endianness
        _dest_image_parameters.Crop = crop
        _dest_image_parameters.Colorimetry = colorimetry
        _dest_image_parameters.IsMonochrome = monochrome
        _dest_image.Parameters = _dest_image_parameters
        _dest_image.DataSize = uicl.UICL_GetRequiredBufferSize(_dest_image)[0]

        if not _dest_image.DataSize:
            return uicl.UICL_ERROR_CONVERSION_NOT_SUPPORTED, None

        _dest_image.DataPtr = (uicl.c_uint8 * _dest_image.DataSize)()

        result = uicl.UICL_Convert(_src_image, _dest_image)
        if result[0] < uicl.UICL_SUCCESS:
            return result[0], 0

        data = result[1].DataPtr
        size = result[1].DataSize

        out_data = None

        out_data = b''.join([data[i].to_bytes(1, byteorder='big', signed=False) for i in range(size)])

        return result[0], out_data

    def upscaling(self, width=0, height=0, colorspace=0, sampling=0, bpc=0, packing=0, _alignment=0, endianness=0,
                  monochrome=False, crop=False, colorimetry=1):
        return self.convert(width, height, colorspace, sampling, bpc, uicl.UICL_ComponentOrder.Order_BGRA, packing,
                            _alignment, endianness, monochrome, crop, True, colorimetry)

    def save_to_bmp(self, path):
        file_type = 0  # 0 - BMP, 1 - BIN, 2 - PPM
        res = uicl.UICL_SaveToFile(self.src_image, path + ".bmp", file_type)
        print("BMP file saved successfully" if res == 0 else "Error saving BMP file. {}".
              format(uicl.uicl_errors.get(res)))

    def save_to_ppm(self, path):
        file_type = 2
        res = uicl.UICL_SaveToFile(self.src_image, path + ".ppm", file_type)
        print("PPM file saved successfully" if res == 0 else "Error saving PPM file. {}".
              format(uicl.uicl_errors.get(res)))
