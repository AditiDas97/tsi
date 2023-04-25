import os
import shutil
import subprocess
from PIL import Image


WIN_DSC_EXE_PATH = __file__[:-16] + 'DSC.exe'
WIN_DP_CRC_EXE_PATH = __file__[:-16] + 'DP_CRC.exe'
WIN_PB_EXE_PATH = __file__[:-16] + 'PB.exe'
WIN_DSC_SOURCE_PATH = 'C:\\Program Files\\Unigraf\\Unigraf UCD Tools\\data\\dsc'

color_format = {0: "RGB444", 1: "YCbCr 4:2:2", 2: "YCbCr 4:4:4", 3: "YCbCr 4:2:0", 4: "Simple 4:2:2"}

if not os.path.isfile(WIN_DSC_EXE_PATH):
    WIN_DSC_EXE_PATH = 'C:\\Program Files\\Unigraf\\Unigraf UCD Tools\\DSC.exe'

if not os.path.isfile(WIN_DP_CRC_EXE_PATH):
    WIN_DP_CRC_EXE_PATH = 'C:\\Program Files\\Unigraf\\Unigraf UCD Tools\\DP_CRC.exe'

if not os.path.isfile(WIN_PB_EXE_PATH):
    WIN_PB_EXE_PATH = 'C:\\Program Files\\Unigraf\\Unigraf UCD Tools\\PB.exe'

MISSING = 1  # File is missing
INVALID_SIZE = 2  # Invalid image size


class DscParameters:

    def __init__(self, width: int, height: int, colorformat: int, bpc: int, bpp: int, is_block_prediction_enabled: bool,
                 horizontal_slice_number: int, buffer_bit_depth: int, vertical_slice_number: int):
        self.Width = width
        self.Height = height
        self.ColorFormat = color_format.get(colorformat)
        self.ColorFormatID = colorformat
        self.BitsPerComponent = bpc
        self.BitsPerPixel = bpp
        self.IsBlockPredictionEnabled = is_block_prediction_enabled
        self.HorizontalSliceNumber = horizontal_slice_number
        self.BufferBitDepth = buffer_bit_depth
        self.VerticalSliceNumber = vertical_slice_number


class DscConverter:

    def __init__(self):
        self.dsc_params = None
        self.path = None
        self.path_to_save = None
        self.dsc_source_path = None

    def set_params(self, path_custom_image, path_to_save, params: DscParameters):
        self.dsc_params = params
        self.path = path_custom_image
        self.path_to_save = path_to_save
        self.dsc_source_path = self.open_external_image(path_custom_image, path_to_save)

    @staticmethod
    def get_ext_compression_config_name(params: DscParameters):

        color_format = ""
        bits_per_pixel = str(int(params.BitsPerPixel / 16))

        if params.ColorFormat.find("YUV420") != -1:
            color_format += "_420"

        if params.ColorFormat.find("YUV422") != -1:
            color_format += "_422"

        return "rc_" + str(params.BitsPerComponent) + "bpc_" + bits_per_pixel + "bpp" + color_format + ".cfg"

    @staticmethod
    def process_execution(cmd):
        popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        log_str = ""
        for stdout_line in iter(popen.stdout.readline, ""):
            log_str += stdout_line + "\n"
        popen.stdout.close()
        return_code = popen.wait()
        if return_code:
            raise subprocess.CalledProcessError(return_code, cmd)
        return log_str, return_code

    @staticmethod
    def get_dsc_source_name(params: DscParameters):
        is_yuv = False
        edited_color_format = params.ColorFormat
        position = edited_color_format.find("YUV")
        if position != -1:
            is_yuv = True

        position = edited_color_format.find("SIMPL")
        if position != -1:
            is_yuv = True

        if edited_color_format == "RGB":
            edited_color_format += "444"

        dsc_source_filename = "{}x{}_{}_bpc{}.{}".format(params.Width, params.Height, edited_color_format,
                                                         params.BitsPerComponent, "yuv" if is_yuv else "ppm")

        return dsc_source_filename

    @staticmethod
    def make_dsc_filename(params: DscParameters):

        dsc_filename = "{}x{}_{}_{}_bpc{}_bpp{}_{}slicew_{}slicew_{}lb.dsc".\
            format(params.Width, params.Height, params.ColorFormat, "BPY" if params.IsBlockPredictionEnabled else "NBP",
                   params.BitsPerComponent, params.BitsPerPixel, params.HorizontalSliceNumber,
                   params.VerticalSliceNumber, params.BufferBitDepth)

        return dsc_filename

    @staticmethod
    def rename_dsc_file(path: str):

        dsc_filename = path.replace(".umf", ".dsc")

        return dsc_filename

    def open_external_image(self, path: str, path_to_save: str):

        if not os.path.exists(path):
            print("Image: {} is missing!".format(path))
            return MISSING

        image = Image.open(path)
        size = image.size

        if size == [0, 0]:
            print("Error. Invalid image size.")
            return INVALID_SIZE

        dsc_source_image = Image.new(image.mode, size)
        dsc_source_image.putdata(image.getdata())
        #  path_to_save - where will be located ppm or yuv image
        dsc_source_image_path = os.path.join(path_to_save, self.get_dsc_source_name(self.dsc_params))
        dsc_source_image.save(dsc_source_image_path)
        dsc_source_image.close()
        image.close()

        return dsc_source_image_path

    def compress_dsc(self, is_simple422_selected: bool):
        dsc_exe_path = WIN_DSC_EXE_PATH
        dp_crc_exe_path = WIN_DP_CRC_EXE_PATH
        pb_exe_path = WIN_PB_EXE_PATH
        multiplier = 1.0
        dsc_cfg_files_folder = WIN_DSC_SOURCE_PATH
        image_txt_path = os.path.join(self.path_to_save, "images.txt")
        tmp_cfg_path = os.path.join(self.path_to_save, "tmp.cfg")

        if not os.path.exists(dsc_exe_path):
            print("DSC.EXE is missing!")
            return MISSING

        if not os.path.exists(dp_crc_exe_path):
            print("DP_CRC.EXE is missing!")
            return MISSING

        if not os.path.exists(pb_exe_path):
            print("PB.EXE is missing!")
            return MISSING

        if not os.path.exists(dsc_cfg_files_folder):
            print("Directory is missing!")
            return MISSING

        ext_config_name = self.get_ext_compression_config_name(self.dsc_params)
        if not os.path.exists(os.path.join(dsc_cfg_files_folder, ext_config_name)):
            print("Required DSC configuration file is missing!")
            return MISSING

        is_yuv = (self.dsc_params.ColorFormat.find("YUV") != -1)
        is422 = (self.dsc_params.ColorFormat.find("422") != -1)
        is_simple422 = (self.dsc_params.ColorFormat == "SIMPL422")
        is420 = (self.dsc_params.ColorFormat.find("420") != -1)

        tmp_cfg_file = open(tmp_cfg_path, "w")
        tmp_cfg_file.write("DSC_VERSION_MINOR 2\n")
        tmp_cfg_file.write("FUNCTION 1\n")
        tmp_cfg_file.write("SRC_LIST {}\n".format(image_txt_path))
        tmp_cfg_file.write("OUT_DIR {}\n".format(self.path_to_save + "\\"))

        tmp_cfg_file.write("DPXR_PAD_ENDS 1\n")
        tmp_cfg_file.write("DPXR_DATUM_ORDER 1\n")
        tmp_cfg_file.write("DPXR_FORCE_BE 0\n")
        tmp_cfg_file.write("SWAP_R_AND_B 1\n")

        tmp_cfg_file.write("DPXW_PAD_ENDS 1\n")
        tmp_cfg_file.write("DPXW_DATUM_ORDER 1\n")
        tmp_cfg_file.write("DPXW_FORCE_PACKING 1\n")
        tmp_cfg_file.write("SWAP_R_AND_B_OUT 1\n")
        tmp_cfg_file.write("PPM_FILE_OUTPUT 0\n")
        tmp_cfg_file.write("DPX_FILE_OUTPUT 0\n")
        tmp_cfg_file.write("BLOCK_PRED_ENABLE {}\n".format(self.dsc_params.IsBlockPredictionEnabled & 1))

        tmp_cfg_file.write("VBR_ENABLE 0\n")
        tmp_cfg_file.write("LINE_BUFFER_BPC {}\n".format(0 if self.dsc_params.BufferBitDepth == 16
                                                         else int(self.dsc_params.BufferBitDepth)))

        if is422 or is420:
            multiplier = 2.0

        tmp_cfg_file.write("USE_YUV_INPUT {}\n".format(1 if is_yuv else 0))

        if is_yuv:
            tmp_cfg_file.write("YUV_FILE_FORMAT 0\n")
            tmp_cfg_file.write("PIC_WIDTH {}\n".format(self.dsc_params.Width))
            tmp_cfg_file.write("PIC_HEIGHT {}\n".format(self.dsc_params.Height))

        tmp_cfg_file.write("SIMPLE_422 {}\n".format(1 if (is_yuv and is_simple422) else 0))
        tmp_cfg_file.write("NATIVE_422 {}\n".format(1 if (is_yuv and is422) else 0))
        tmp_cfg_file.write("NATIVE_420 {}\n".format(1 if (is_yuv and is420) else 0))
        tmp_cfg_file.write("FULL_ICH_ERR_PRECISION 0\n")

        slice_width = (self.dsc_params.Width / self.dsc_params.HorizontalSliceNumber) \
            if (self.dsc_params.HorizontalSliceNumber != 0) \
            else self.dsc_params.Width

        slice_height = (self.dsc_params.Height / self.dsc_params.VerticalSliceNumber) \
            if (self.dsc_params.VerticalSliceNumber != 0) \
            else self.dsc_params.Height

        tmp_cfg_file.write("SLICE_WIDTH {}\n".format(int(slice_width)))
        tmp_cfg_file.write("SLICE_HEIGHT {}\n".format(int(slice_height)))

        shutil.copy(os.path.join(dsc_cfg_files_folder, ext_config_name),
                    os.path.join(self.path_to_save, ext_config_name))

        tmp_cfg_file.write("INCLUDE {}\n".format(os.path.join(self.path_to_save, ext_config_name)))
        tmp_cfg_file.write("BITS_PER_PIXEL {}\n".format(multiplier * (1.0 / 16.0) * self.dsc_params.BitsPerPixel))

        tmp_cfg_file.close()

        dsc_source_image_name = self.dsc_source_path
        result_file = os.path.join(self.path_to_save, self.make_dsc_filename(self.dsc_params))

        patch_header = False
        if is_yuv & is_simple422:
            patch_header = not is_simple422_selected
            umf_file = result_file.replace(".dsc", ("_444.umf" if patch_header else "_422.umf"))
        else:
            umf_file = result_file.replace(".dsc", ".umf")

        dsc_file = dsc_source_image_name.replace(("yuv" if dsc_source_image_name.find("yuv") != -1 else "ppm"), "dsc")

        file = open(image_txt_path, "w")
        file.write("{}\r\n".format(dsc_source_image_name))
        file.close()

        compression_command = "{} -F {}".format(dsc_exe_path, tmp_cfg_path)
        print(self.process_execution(compression_command)[0])

        if patch_header:
            compression_command = "{} {} -p 8 -a 0xf7".format(pb_exe_path, dsc_file)
            print(self.process_execution(compression_command)[0])

        compression_command = "{} -u{}{}{} -r {} {} {}"\
            .format(dp_crc_exe_path, (" -y auto " if is_yuv else ""),
                    (("-c {} ".format(self.dsc_params.ColorFormatID)) if is_yuv else ""),
                    (("-d {} {}".format(self.dsc_params.Width, self.dsc_params.Height)) if is_yuv else ""),
                    dsc_file, self.dsc_source_path, umf_file)

        print(self.process_execution(compression_command)[0])

        if os.path.exists(self.rename_dsc_file(umf_file)):
            os.remove(self.rename_dsc_file(umf_file))
            os.rename(dsc_file, self.rename_dsc_file(umf_file))
        os.remove(image_txt_path)
        os.remove(tmp_cfg_path)
        os.remove(os.path.join(self.path_to_save, ext_config_name))
        os.remove(self.dsc_source_path)
