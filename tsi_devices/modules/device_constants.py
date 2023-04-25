import time
import warnings

case_values_pg = [[800, 525, 640, 480, 144, 35, 96, 2, 60000, 0, 1, False, False, 0, "Color Bars"],
                  [858, 525, 720, 480, 122, 36, 62, 6, 60000, 0, 1, False, False, 0, "Color Bars"],
                  [858, 525, 720, 480, 122, 36, 62, 6, 120000, 0, 1, False, False, 0, "Color Bars"],
                  [1056, 628, 800, 600, 216, 27, 128, 4, 60000, 0, 1, True, True, 0, "Color Bars"],
                  [1088, 517, 848, 480, 224, 31, 112, 8, 60000, 0, 1, True, True, 0, "Color Bars"],
                  [1344, 806, 1024, 768, 296, 35, 136, 6, 60000, 0, 1, False, False, 0, "Color Bars"],
                  [1650, 750, 1280, 720, 260, 25, 40, 5, 60000, 0, 1, True, True, 0, "Color Bars"],
                  [1650, 750, 1280, 720, 260, 25, 40, 5, 120000, 0, 1, True, True, 0, "Color Bars"],
                  [1440, 790, 1280, 768, 112, 19, 32, 7, 60000, 0, 1, True, False, 0, "Color Bars"],
                  [1664, 798, 1280, 768, 320, 27, 128, 7, 60000, 0, 1, False, True, 0, "Color Bars"],
                  [1440, 823, 1280, 800, 112, 20, 32, 6, 60000, 0, 1, True, False, 1, "Color Bars"],
                  [1680, 831, 1280, 800, 328, 28, 128, 6, 60000, 0, 1, False, True, 0, "Color Bars"],
                  [1800, 1000, 1280, 960, 424, 39, 112, 3, 60000, 0, 1, True, True, 0, "Color Bars"],
                  [1688, 1066, 1280, 1024, 360, 41, 112, 3, 60000, 0, 1, True, True, 0, "Color Bars"],
                  [1792, 795, 1360, 768, 368, 24, 112, 6, 60000, 0, 1, True, True, 0, "Color Bars"],
                  [1560, 1080, 1400, 1050, 112, 27, 32, 4, 60000, 0, 1, False, False, 1, "Color Bars"],
                  [1864, 1089, 1400, 1050, 376, 36, 144, 4, 60000, 0, 1, False, False, 1, "Color Bars"],
                  # [1716, 525, 1440, 480, 244, 36, 124, 6, 59940, 0, 1, False, False, 0, "Color Bars"],
                  [1728, 625, 1440, 576, 264, 44, 128, 5, 50000, 0, 1, False, False, 0, "Color Bars"],
                  [1760, 1235, 1600, 1200, 112, 32, 32, 4, 60000, 0, 1, False, False, 1, "Color Bars"],
                  [2160, 1250, 1600, 1200, 496, 49, 192, 3, 60000, 0, 1, True, True, 0, "Color Bars"],
                  [2200, 750, 1680, 720, 260, 25, 40, 5, 60000, 0, 1, True, True, 0, "Color Bars"],
                  [2000, 825, 1680, 720, 260, 100, 40, 5, 120000, 0, 1, True, True, 0, "Color Bars"],
                  [1840, 1080, 1680, 1050, 112, 27, 32, 6, 60000, 0, 1, True, False, 1, "Color Bars"],
                  [2240, 1089, 1680, 1050, 456, 36, 176, 6, 60000, 0, 1, False, True, 0, "Color Bars"],
                  [2448, 1394, 1792, 1344, 528, 49, 200, 3, 60000, 0, 1, False, True, 0, "Color Bars"],
                  [2528, 1439, 1856, 1392, 576, 46, 224, 3, 60000, 0, 1, False, True, 0, "Color Bars"],
                  [2080, 1096, 1920, 1080, 112, 13, 32, 5, 30000, 0, 1, True, False, 1, "Color Bars"],
                  [2000, 1096, 1920, 1080, 72, 14, 32, 8, 30000, 0, 1, True, False, 2, "Color Bars"],
                  [2200, 1125, 1920, 1080, 192, 41, 44, 5, 30000, 0, 1, True, True, 0, "Color Bars"],
                  # [2080, 1157, 1920, 1080, 152, 14, 32, 8, 144050, 0, 1, False, False, 3, "Color Bars"],
                  # [2080, 1190, 1920, 1080, 152, 14, 32, 8, 200070, 0, 1, False, False, 3, "Color Bars"],
                  [2080, 1111, 1920, 1080, 112, 28, 32, 5, 60000, 0, 1, False, False, 1, "Color Bars"],
                  [2080, 1111, 1920, 1080, 72, 14, 32, 8, 60000, 0, 1, True, True, 2, "Color Bars"],
                  [2200, 1125, 1920, 1080, 192, 41, 44, 5, 60000, 0, 1, True, True, 0, "Color Bars"],
                  [2080, 1144, 1920, 1080, 112, 61, 32, 5, 120000, 0, 1, True, False, 1, "Color Bars"],
                  [2000, 1144, 1920, 1080, 72, 14, 32, 8, 120000, 0, 1, True, False, 2, "Color Bars"],
                  [2200, 1125, 1920, 1080, 192, 41, 44, 5, 120000, 0, 1, True, True, 0, "Color Bars"],
                  [2592, 1245, 1920, 1200, 536, 42, 200, 6, 60000, 0, 1, False, True, 0, "Color Bars"],
                  [2600, 1500, 1920, 1440, 552, 59, 208, 3, 60000, 0, 1, False, True, 0, "Color Bars"],
                  [2208, 1580, 2048, 1536, 112, 41, 32, 4, 60000, 0, 1, True, False, 1, "Color Bars"],
                  [2640, 1481, 2560, 1440, 72, 14, 32, 8, 60000, 0, 1, True, False, 2, "Color Bars"],
                  [2720, 1481, 2560, 1440, 112, 38, 32, 5, 60000, 0, 1, True, False, 1, "Color Bars"],
                  # [2720, 1543, 2560, 1440, 152, 14, 32, 8, 144050, 0, 1, True, False, 3, "Color Bars"],
                  # [2720, 1586, 2560, 1440, 152, 14, 32, 8, 200070, 0, 1, True, False, 3, "Color Bars"],
                  [3424, 1120, 2560, 1080, 704, 37, 272, 10, 60000, 0, 1, False, True, 0, "Color Bars"],
                  [2720, 1111, 2560, 1080, 112, 28, 32, 10, 60000, 0, 1, True, False, 1, "Color Bars"],
                  # [2720, 1157, 2560, 1080, 152, 14, 32, 8, 144051, 0, 1, True, False, 3, "Color Bars"],
                  # [2720, 1190, 2560, 1080, 152, 14, 32, 8, 200070, 0, 1, True, False, 3, "Color Bars"],
                  [3000, 1100, 2560, 1080, 192, 16, 44, 5, 60000, 0, 1, True, True, 0, "Color Bars"],
                  [3300, 1250, 2560, 1080, 192, 16, 44, 5, 120000, 0, 1, True, True, 0, "Color Bars"],
                  [3504, 1658, 2560, 1600, 752, 55, 280, 6, 60000, 0, 1, False, True, 0, "Color Bars"],
                  [2720, 1646, 2560, 1600, 112, 43, 32, 6, 60000, 0, 1, True, False, 1, "Color Bars"],
                  [2976, 1456, 2880, 1440, 48, 8, 8, 1, 60000, 0, 1, True, True, 0, "Color Bars"],
                  [4176, 2222, 4096, 2160, 72, 14, 32, 8, 60000, 0, 1, True, False, 2, "Color Bars"],
                  [4000, 2191, 3840, 2160, 112, 28, 32, 5, 30000, 0, 1, True, False, 1, "Color Bars"],
                  [3920, 2191, 3840, 2160, 72, 14, 32, 8, 30000, 0, 1, True, False, 2, "Color Bars"],
                  # [4000, 2314, 3840, 2160, 152, 14, 32, 8, 144050, 0, 1, True, False, 3, "Color Bars"],
                  [4400, 2250, 3840, 2160, 384, 82, 88, 10, 30000, 0, 1, True, True, 0, "Color Bars"],
                  [5280, 2250, 3840, 2160, 384, 82, 88, 10, 50000, 0, 1, True, True, 0, "Color Bars"],
                  [5280, 2250, 4096, 2160, 216, 82, 88, 10, 50000, 0, 1, True, True, 0, "Color Bars"],
                  [3840, 2160, 4000, 2222, 112, 59, 32, 5, 60000, 0, 1, True, False, 1, "Color Bars"],
                  [3920, 2222, 3840, 2160, 72, 14, 32, 8, 60000, 0, 1, True, False, 2, "Color Bars"],
                  # [4000, 2222, 3840, 2160, 152, 14, 32, 8, 60021, 0, 1, True, False, 3, "Color Bars"],
                  [4400, 2250, 3840, 2160, 384, 82, 88, 10, 60000, 0, 1, True, True, 0, "Color Bars"],
                  [4256, 2222, 4096, 2160, 112, 59, 32, 10, 60000, 0, 1, True, False, 1, "Color Bars"],
                  # [4256, 2222, 4096, 2160, 152, 14, 32, 8, 60021, 0, 1, True, False, 3, "Color Bars"],
                  # [4256, 2314, 4096, 2160, 152, 14, 32, 8, 144050, 0, 1, True, False, 3, "Color Bars"],
                  [4400, 2250, 4096, 2160, 216, 82, 88, 10, 60000, 0, 1, True, True, 0, "Color Bars"],
                  [4000, 2287, 3840, 2160, 112, 124, 32, 5, 120000, 0, 1, True, False, 1, "Color Bars"],
                  [3920, 2287, 3840, 2160, 72, 14, 32, 8, 120000, 0, 1, True, False, 2, "Color Bars"],
                  [4400, 2250, 3840, 2160, 384, 82, 88, 10, 120000, 0, 1, True, True, 0, "Color Bars"],
                  [5280, 2191, 5120, 2160, 112, 28, 32, 10, 30000, 0, 1, True, False, 1, "Color Bars"],
                  [5200, 2191, 5120, 2160, 72, 14, 32, 8, 30000, 0, 1, True, False, 2, "Color Bars"],
                  [6000, 2200, 5120, 2160, 216, 32, 88, 10, 30000, 0, 1, True, True, 0, "Color Bars"],
                  [5280, 2222, 5120, 2160, 112, 59, 32, 10, 60000, 0, 1, True, False, 1, "Color Bars"],
                  [5200, 2222, 5120, 2160, 72, 14, 32, 6, 60000, 0, 1, True, False, 2, "Color Bars"],
                  [5500, 2250, 5120, 2160, 216, 82, 88, 10, 60000, 0, 1, True, True, 0, "Color Bars"],
                  [5280, 2287, 5120, 2160, 112, 124, 32, 10, 120000, 0, 1, True, False, 1, "Color Bars"],
                  # [5280, 2287, 5120, 2160, 152, 14, 32, 8, 120042, 0, 1, True, False, 3, "Color Bars"],
                  [5200, 2287, 5120, 2160, 72, 14, 32, 8, 120000, 0, 1, True, False, 2, "Color Bars"],
                  [5500, 2250, 5120, 2160, 216, 82, 88, 10, 120000, 0, 1, True, True, 0, "Color Bars"],
                  [5280, 2962, 5120, 2880, 112, 79, 32, 5, 60000, 0, 1, True, False, 1, "Color Bars"],
                  [5200, 2962, 5120, 2880, 72, 14, 32, 8, 60000, 0, 1, True, False, 2, "Color Bars"],
                  # [5280, 2962, 5120, 2880, 152, 14, 32, 8, 60021, 0, 1, True, False, 3, "Color Bars"],
                  [11000, 4500, 7680, 4320, 768, 164, 176, 20, 24000, 0, 1, True, True, 0, "Color Bars"],
                  [7840, 4381, 7680, 4320, 112, 58, 32, 5, 30000, 0, 1, True, False, 1, "Color Bars"],
                  [7760, 4381, 7680, 4320, 72, 14, 32, 8, 30000, 0, 1, True, False, 2, "Color Bars"],
                  [9000, 4400, 7680, 4320, 768, 64, 176, 20, 30000, 0, 1, True, True, 0, "Color Bars"],
                  [7840, 4443, 7680, 4320, 112, 120, 32, 5, 60000, 0, 1, True, True, 1, "Color Bars"],
                  [7760, 4443, 7680, 4320, 72, 14, 32, 8, 60000, 0, 1, True, False, 2, "Color Bars"],
                  [9000, 4400, 7680, 4320, 768, 64, 176, 20, 60000, 0, 1, True, True, 0, "Color Bars"],
                  # [7840, 4529, 7680, 4320, 112, 206, 32, 5, 100000, 0, 1, True, False, 1, "Color Bars"],
                  # [7760, 4529, 7680, 4320, 72, 14, 32, 8, 100000, 0, 1, True, False, 2, "Color Bars"],
                  # [10560, 4500, 7680, 4320, 768, 164, 176, 20, 100000, 0, 1, True, True, 0, "Color Bars"],
                  [11000, 4500, 10240, 4320, 112, 58, 32, 5, 30000, 0, 1, True, False, 1, "Color Bars"],
                  [11000, 4500, 10240, 4320, 72, 14, 32, 8, 30000, 0, 1, True, False, 2, "Color Bars"],
                  [12500, 4950, 10240, 4320, 768, 614, 176, 20, 24000, 0, 1, True, True, 0, "Color Bars"],
                  [13500, 4400, 10240, 4320, 768, 64, 176, 20, 25000, 0, 1, True, True, 0, "Color Bars"],
                  [11000, 4500, 10240, 4320, 472, 164, 176, 20, 30000, 0, 1, True, True, 0, "Color Bars"]
                  # [12500, 4950, 10240, 4320, 768, 614, 176, 20, 48000, 0, 1, True, True, 0, "Color Bars"],
                  # [13500, 4400, 10240, 4320, 768, 64, 176, 20, 50000, 0, 1, True, True, 0, "Color Bars"],
                  # [11000, 4500, 10240, 4320, 472, 164, 176, 20, 60000, 0, 1, True, True, 0, "Color Bars"],
                  # [13200, 4500, 10240, 4320, 768, 164, 176, 20, 100000, 0, 1, True, True, 0, "Color Bars"],
                  # [11000, 4500, 10240, 4320, 472, 164, 176, 20, 120000, 0, 1, True, True, 0, "Color Bars"]
                  ]

dict_rate = {1.62: 6, 2.70: 10, 5.40: 20, 6.75: 25, 8.10: 30}

dict_color_formate = {"RGB": 0, "YCbCr 4:4:4 ITU-601": 1, "YCbCr 4:2:2 ITU-601": 2, "YCbCr 4:2:0 ITU-601": 3,
                      "YCbCr 4:4:4 ITU-709": 4, "YCbCr 4:2:2 ITU-709": 5, "YCbCr 4:2:0 ITU-709": 6}

dict_color_formate_rev = {0: "RGB", 1: "YCbCr 4:4:4 ITU-601", 2: "YCbCr 4:2:2 ITU-601", 3: "YCbCr 4:2:0 ITU-601",
                          4: "YCbCr 4:4:4 ITU-709", 5: "YCbCr 4:2:2 ITU-709", 6: "YCbCr 4:2:0 ITU-709"}

dict_color_mode_dp = {0: "No Data", 1: "Unknown", 2: "RGB", 3: "YCbCr 4:2:2", 4: "YCbCr 4:4:4", 5: "YCbCr 4:2:0",
                      6: "IDO", 7: "Y only", 8: "Raw", 9: "DSC"}

dict_colorimetry_dp = {0: "No Data", 1: "Unknown", 2: "RGB", 3: "SMPTE 170M", 4: "ITU-601", 5: "ITU-709",
                       6: "xvYCC.601", 7: "xvYCC.709", 8: "sYCC.601", 9: "Adobe YCC.601", 10: "Adobe RGB",
                       11: "ITU-R BT2020 (YcCbcCrc)", 12: "ITU-R BT2020 (YCbCr)", 13: "ITU-R BT2020 (RGB)",
                       14: "Wide gamut RGB fixed point", 15: "Wide gamut RGB floating point",
                       16: "DCI-3 (SMPTE RP 431-1)", 17: "DICOM 1.4 gray scale", 18: "Custom color profile"}

dict_build_color_format = {"PGImageFormatRGB_080808": 0x000,
                           "PGImageFormatRGB_161616": 0x001,
                           "PGImageFormatRGBA_080808A": 0x002,
                           "PGImageFormatRGBA_161616A": 0x003,
                           "PGImageFormatRGB_121212": 0x004,
                           "PGImageFormatYCbCr_080808": 0x100,
                           "PGImageFormatYCbCr_161616": 0x101,
                           "PGImageFormatYCbYCr_08": 0x200,
                           "PGImageFormatYCbYCr_16": 0x201,
                           "PGImageFormatYYCbYYCr_08": 0x300,
                           "PGImageFormatYYCbYYCr_16": 0x301,
                           "PGImageFormatI420_08": 0x310,
                           "PGImageFormatI420_10": 0x311,
                           "PGImageFormatI420_12": 0x312,
                           "PGImageFormatI420_16": 0x313,
                           "PGImageFormatUnknown": 2147483647}

dict_bpc = {6: 0, 8: 1, 10: 2, 12: 3, 16: 4, 18: 0, 24: 1, 32: 2}

dict_bpc_rev = {0: 6, 1: 8, 2: 10, 3: 12, 4: 16}

dict_usbc_bit_rate_values = {10: 1, 20: 2, 13: 4}
dict_usbc_bit_rate_rev_values = {1: 10, 2: 20, 4: 13}

dict_pattern = {"Disabled": 0,
                "Color Bars": 1,
                "Chessboard": 2,
                "Solid color": 3,
                "Solid white": 4,
                "Solid red": 5,
                "Solid green": 6,
                "Solid blue": 7,
                "White V-Strips": 8,
                "RGB 16 Wide strips": 9,
                "Color Ramp": 10,
                "Color Square": 11,
                "Motion pattern": 12,
                "Custom image": 13,
                "Playback": 14,
                "Square Window": 15,
                "DSC": 16}

dict_color_mode_hdmi = {
    0: "No Data", 1: "Unknown", 2: "RGB", 3: "YCbCr4:2:2", 4: "YCbCr4:4:4", 5: "YCbCr4:2:0", 6: "IDO", 7: "Y-Only",
    8: "Raw"
}

dict_colorimetry_hdmi = {
    0: "No Data", 1: "Unknown", 2: "RGB", 3: "SMPTE 170M", 4: "ITU-R BT.601", 5: "ITU-R BT.709", 6: "xvYCC.601",
    7: "xvYCC.709", 8: "sYCC.601", 9: "Adobe YCC.601", 10: "Adobe RGB", 11: "ITU-R BT2020 (YcCbcCrc)",
    12: "ITU-R BT2020 (YCbCr)", 13: "ITU-R BT2020 (RGB)", 14: "Wide gamut RGB fixed point",
    15: "Wide gamut RGB floating point", 16: "DCI-3 (SMPTE RP 431-1)", 17: "DICOM 1.4 gray scale",
    18: "Custom color profile"
}

dict_link_mode_frl = {
    0: "FRL_Disable",
    1: "FRL_3L_03G",
    2: "FRL_3L_06G",
    3: "FRL_4L_06G",
    4: "FRL_4L_08G",
    5: "FRL_4L_10G",
    6: "FRL_4L_12G"
}

dict_hdmi_behavior = {0: "HDMI 1.4", 1: "HDMI 2.0", 2: "HDMI 2.1"}

device_roles = {"sink": "RX", "source": "TX"}


def info_hex(idx: int, data: str, sz: int, gap: int) -> str:
    list_r_dp_sdp = ["ACR", "ASP", "AIF"]
    tmp = list_r_dp_sdp[idx]
    for i in range(sz):
        tmp += " " + hex(int(data[i])) + (" " if i == gap else "")
    tmp += "\n"
    return tmp


def info_header(num: int, hbsz: int) -> str:
    s = "       "
    n = 0
    for i in range(num):
        if i != hbsz:
            s += "   " + str(n)
            n += 1
        else:
            n = 0
            s += " "
    return s


PDC_STATE_PULLUP_POS = 0
PDC_STATE_PULLUP_09A = 0 << PDC_STATE_PULLUP_POS
PDC_STATE_PULLUP_15A = 1 << PDC_STATE_PULLUP_POS
PDC_STATE_PULLUP_30A = 2 << PDC_STATE_PULLUP_POS
PDC_STATE_PULLUP_UNKNOWN = 3 << PDC_STATE_PULLUP_POS

PDC_STATE_DEV_ROLE_POS = 2
PDC_STATE_DEV_ROLE_UFP = 0 << PDC_STATE_DEV_ROLE_POS
PDC_STATE_DEV_ROLE_DFP = 1 << PDC_STATE_DEV_ROLE_POS
PDC_STATE_DEV_ROLE_DRP = 2 << PDC_STATE_DEV_ROLE_POS
PDC_STATE_DEV_ROLE_UNKNOWN = 3 << PDC_STATE_DEV_ROLE_POS

PDC_STATE_PD_MODE_POS = 4
PDC_STATE_PD_MODE_NORMAL = 0 << PDC_STATE_PD_MODE_POS
PDC_STATE_PD_MODE_LSOURCE = 1 << PDC_STATE_PD_MODE_POS
PDC_STATE_PD_MODE_LSINK = 2 << PDC_STATE_PD_MODE_POS
PDC_STATE_PD_MODE_UNKNOWN = 3 << PDC_STATE_PD_MODE_POS

PDC_STATE_USB3_MODE_POS = 6
PDC_STATE_USB3_MODE_DISABLED = 0 << PDC_STATE_USB3_MODE_POS
PDC_STATE_USB3_MODE_GEN_1 = 1 << PDC_STATE_USB3_MODE_POS
PDC_STATE_USB3_MODE_GEN_2 = 2 << PDC_STATE_USB3_MODE_POS
PDC_STATE_USB3_MODE_UNKNOWN = 3 << PDC_STATE_USB3_MODE_POS

PDC_STATE_USB2_ENABLED = 1 << 8
PDC_STATE_VCONN_SWAP_EN = 1 << 9
PDC_STATE_PR_SWAP_EN = 1 << 10
PDC_STATE_DR_SWAP_EN = 1 << 11
PDC_STATE_DEBUG_ACCESSORY = 1 << 12
PDC_STATE_AUDIO_ACCESSORY = 1 << 13
PDC_STATE_FR_SWAP_EN = 1 << 14

PDC_STATE_DRP_TRY_MODE_POS = 16
PDC_STATE_DRP_TRY_MODE_PURE_DRP = 0 << PDC_STATE_DRP_TRY_MODE_POS
PDC_STATE_DRP_TRY_MODE_DRP_TRYSNK = 1 << PDC_STATE_DRP_TRY_MODE_POS
PDC_STATE_DRP_TRY_MODE_DRP_TRYSRC = 2 << PDC_STATE_DRP_TRY_MODE_POS
PDC_STATE_DRP_TRY_MODE_DRP_UNKNOWN = 3 << PDC_STATE_DRP_TRY_MODE_POS

PG_TIMF_META_REDUCED_BLANK = (1 << 24)
PG_TIMF_META_REDUCED_BLANK_2 = (2 << 24)
PG_TIMF_META_REDUCED_BLANK_3 = (3 << 24)

CAP_OPTION_AUDIO = 1
CAP_OPTION_VIDEO = 1 << 1
CAP_OPTION_EVENTS = 1 << 2
CAP_OPTION_MODE_LIVE = 1 << 3
CRC_MAX_READ_COUNT = 125

PG_TIMF_COLOR_RGB = (0 << 11)
PG_TIMF_COLOR_YUV = (1 << 11)
PG_TIMF_COLOR_YUV422 = (2 << 11)
PG_TIMF_COLOR_YUV420 = (3 << 11)
PG_TIMF_COLOR_Y = (4 << 11)
PG_TIMF_COLOR_RAW = (5 << 11)

dict_color_formate_tx_rev = {PG_TIMF_COLOR_RGB: "RGB", PG_TIMF_COLOR_YUV: "YCbCr 4:4:4",
                             PG_TIMF_COLOR_YUV422: "YCbCr 4:2:2", PG_TIMF_COLOR_YUV420: "YCbCr 4:2:0"}

PG_TIMF_COLORIMETRY_MASK = (0x01 << 16)
PG_TIMF_ITU_601 = (0 << 16)
PG_TIMF_ITU_709 = (1 << 16)

dict_colorimetry_tx = {PG_TIMF_ITU_601: "ITU-601", PG_TIMF_ITU_709: "ITU-709"}


class DeviceOpenError(Exception):

    def __init__(self, message: str):
        self.__message = message
        super().__init__(self.__message)


def check_frame_size(h_active, v_active, input_color_mode, count, memory):
    color_mode = 4 if input_color_mode in [2, 3, 4, "RGB", "YCbCr4:2:2", "YCbCr4:4:4"] else 3
    frame_size = h_active * v_active * color_mode

    max_device_memory = memory
    count_frames_available = int(max_device_memory // frame_size)

    if count > count_frames_available:
        warnings.warn("Exceeded the maximum number of frames available to capture {}. Will be captured {} frames"
                      .format(count_frames_available, count_frames_available))
        count = count_frames_available

    return count
