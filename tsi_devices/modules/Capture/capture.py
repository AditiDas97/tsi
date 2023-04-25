from tsi.tsi_devices.libs.lib_tsi.tsi import *
from tsi.tsi_devices.libs.lib_uicl.test_uicl import *
import shutil
from dataclasses import dataclass
import time
import warnings


@dataclass
class EventData:
    timestamp: int
    event_data: bytearray
    type: str


class Capturer:

    def __init__(self, device):
        self.device = device

    def download_captured_events(self, save_to_bin_file: bool = False, save_to_txt_file: bool = False,
                                 path_to_save="") -> list:
        event_count = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_EVCAP_COUNT, c_uint32)[1]
        if event_count <= 0:
            return []

        events = []

        while event_count > 0:
            event_size = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_EVCAP_DATA, None, 0)[0]
            if event_size > 0:
                data = bytearray(TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_EVCAP_DATA, c_byte,
                                                       event_size)[1])
                events.append(data)
            event_count -= 1

        if path_to_save == "":
            path = os.getcwd() + '\\Events\\'
            if not os.path.exists(path):
                os.makedirs(path)
            else:
                shutil.rmtree(path)
                os.makedirs(path)
        else:
            path = path_to_save
            if not os.path.exists(path):
                os.makedirs(path)

        result = []
        e_file = 0
        for data in events:
            if save_to_bin_file:
                f = open(path + 'Event{:0>3}.bin'.format(e_file), 'wb')
                f.write(data)
                f.close()

            if save_to_txt_file:
                result = self.device.parse_event(data)
                if result[0] < TSI_SUCCESS:
                    return []
                info = open(path + 'Event_all.txt'.format(e_file), 'a+')
                info.write(result[3] + '\n')
                info.write(result[2] + '\n')
                info.write(result[5] + '\n')
                info.write(result[4] + '\n')

                for i in range(len(data)):
                    if not (i % 16):
                        info.write('\n')
                    info.write('0x{:02x} '.format(data[i]))

                info.close()
            e_file += 1

        return events

    def frame_capture_is_ready(self):
        status = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_CAP_STATUS, c_int)[1]

        if status & (1 << 2):
            return True
        else:
            return False

    @staticmethod
    def parse_attributes(attributes):
        frame = ImageU()

        color_component_format = attributes >> 16 & 0x7
        frame.colorspace = uicl.parse_attributes_colorspace[color_component_format]
        frame.sampling = uicl.parse_attributes_sampling[color_component_format]
        frame.component_order = uicl.UICL_ComponentOrder.Order_UCDRX
        frame.packing = uicl.parse_attributes_packing[attributes >> 14 & 0x3]
        frame.bpc = uicl.parse_attributes_bpc[attributes >> 5 & 0xF]
        frame.alignment = uicl.UICL_Alignment.Alignment_MSB
        frame.endianness = uicl.UICL_Endianness.Endianness_Little
        frame.colorimetry = uicl.parse_attributes_colorimetry[attributes >> 20 & 0x3] if (attributes >> 20 & 0x3) != 0x3 \
            else uicl.parse_attributes_ecolorimetry[attributes >> 22 & 0x7]

        if color_component_format == 6:
            frame.colorspace = uicl.UICL_Colorspace.Colorspace_Unknown
            frame.sampling = uicl.UICL_Sampling.Sampling_Unknown
            frame.packing = uicl.UICL_Packing.Packing_Unknown
            frame.alignment = uicl.UICL_Alignment.Alignment_Unknown
            frame.component_order = uicl.UICL_ComponentOrder.Order_Unknown

        frame.monochrome = False
        frame.crop = False

        return frame

    def start_capture(self, config: int):
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_CAP_CONFIG, config)
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_W_CAP_COMMAND, 1)
        time.sleep(1)

    def stop_capture(self):
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_W_CAP_COMMAND, 2)
