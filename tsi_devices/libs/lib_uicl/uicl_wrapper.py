from . import uicl


def convert_image(data_1=None, width_1=0, height_1=0, colorspace_1=0, sampling_1=0, bpc_1=0, component_order_1=0,
                  packing_1=0, alignment_1=0, endianness_1=0, monochrome_1=False, crop_1=False, width_2=0, height_2=0,
                  colorspace_2=0, sampling_2=0, bpc_2=0, component_order_2=0, packing_2=0, alignment_2=0,
                  endianness_2=0, monochrome_2=False, crop_2=False):

    _dest_image = uicl.UICL_Image()
    _dest_image_parameters = uicl.UICL_ImageParameters()
    _dest_image_parameters.Version = 1
    _dest_image_parameters.Width = width_2
    _dest_image_parameters.Height = height_2
    _dest_image_parameters.BitsPerColor = bpc_2
    _dest_image_parameters.Colorspace = colorspace_2
    _dest_image_parameters.ComponentOrder = component_order_2
    _dest_image_parameters.Sampling = sampling_2
    _dest_image_parameters.Packing = packing_2
    _dest_image_parameters.Alignment = alignment_2
    _dest_image_parameters.Endianness = endianness_2
    _dest_image_parameters.Crop = crop_2
    _dest_image_parameters.IsMonochrome = monochrome_2
    _dest_image.Parameters = _dest_image_parameters

    _dest_image.DataSize = uicl.UICL_GetRequiredBufferSize(_dest_image)[0]
    if not _dest_image.DataSize:
        return uicl.UICL_ERROR_CONVERSION_NOT_SUPPORTED

    _dest_image.DataPtr = (uicl.c_uint8 * _dest_image.DataSize)()

    _src_image = uicl.UICL_Image()
    if data_1 is not None and len(data_1) > 0:
        _src_image_parameters = uicl.UICL_ImageParameters()
        _src_image_parameters.Version = 1
        _src_image_parameters.Width = width_1
        _src_image_parameters.Height = height_1
        _src_image_parameters.BitsPerColor = bpc_1
        _src_image_parameters.Colorspace = colorspace_1
        _src_image_parameters.ComponentOrder = component_order_1
        _src_image_parameters.Sampling = sampling_1
        _src_image_parameters.Packing = packing_1
        _src_image_parameters.Alignment = alignment_1
        _src_image_parameters.Endianness = endianness_1
        _src_image_parameters.Crop = crop_1
        _src_image_parameters.IsMonochrome = monochrome_1
        _src_image.Parameters = _src_image_parameters
        _src_image.DataSize = len(data_1)
        _src_image.DataPtr = (uicl.c_uint8 * _src_image.DataSize)(*data_1)

    result = uicl.UICL_Convert(_src_image, _dest_image)
    if result[0] < uicl.UICL_SUCCESS:
        return result[0],

    data = result[1].DataPtr
    size = result[1].DataSize
    out_data = b''.join([data[i].to_bytes(1, byteorder='big', signed=False) for i in range(size)])

    return result[0], out_data


def upscaling(data=None, width=0, height=0, colorspace=0, sampling=0, bpc=0, packing=0,
              alignment=0, endianness=0, monochrome=False, crop=False):
    return convert_image(data, width, height, colorspace, sampling, bpc, uicl.UICL_ComponentOrder.Order_UCDRX,
                         packing, alignment, endianness, monochrome, crop, width, height, colorspace, sampling, bpc,
                         uicl.UICL_ComponentOrder.Order_PlainRaw, packing, alignment, endianness)
