from .capture_usbc import *
import datetime


class BulkCapturer(CapturerDpRx):

    def __init__(self, device):
        super().__init__(device)

    def start_bulk_capture(self, requested_capture_size, bulk_10bit=True) -> int:
        # Stop buffered capture if running
        cap_status = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_CAP_STATUS, c_uint32)[1]
        if cap_status:
            TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_W_CAP_COMMAND, 2)
            slept_ms = 0
            max_sleep_ms = 5 * 1000
            while slept_ms < max_sleep_ms and cap_status & 0x1:
                cap_status = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_CAP_STATUS, c_uint32)[1]
                slept_ms += 100
                time.sleep(0.1)

            if cap_status & 0x1:
                return 0

        # Stop bulk capture if running
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_BULK_CAPTURE_CONTROL_W, TSI_BULK_CAPTURE_STOP)
        value = -1
        slept_ms = 0
        max_sleep_ms = 5000
        while slept_ms < max_sleep_ms and value != TSI_BULK_STATUS_IDLE:
            TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_BULK_CAPTURE_CLEAR_W, 0)
            value = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_BULK_CAPTURE_STATUS_R, c_uint32)[1]
            slept_ms += 100
            time.sleep(0.1)

        if value != TSI_BULK_STATUS_IDLE:
            return 0

        total_device_memory_bytes = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_MEMORY_SIZE, c_ulonglong)[1]
        print('Read total device memory {}'.format(total_device_memory_bytes))
        if total_device_memory_bytes == 0:
            return 0

        reserved_memory_bytes = 0x10000000
        max_capture_size = total_device_memory_bytes - reserved_memory_bytes

        if requested_capture_size > max_capture_size:
            actual_capture_size = max_capture_size
        else:
            actual_capture_size = requested_capture_size

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_MEMORY_LAYOUT, actual_capture_size, c_ulonglong)
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_BULK_CAPTURE_BLOCK, 0)

        bulk_type = TSI_BULK_CAPTURE_TYPE_10BIT if bulk_10bit else TSI_BULK_CAPTURE_TYPE_8BIT
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_BULK_CAPTURE_TYPE_W, bulk_type)

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_BULK_CAPTURE_CONTROL_W, TSI_BULK_CAPTURE_START)

        print('Started bulk capture, size={} bytes'.format(actual_capture_size))

        return actual_capture_size

    def bulk_capture_is_ready(self):
        status = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_BULK_CAPTURE_STATUS_R, c_uint32)[1]
        return status == TSI_BULK_STATUS_TRANSFERRING

    def download_bulk_capture(self, capture_size, filename=''):
        if not self.bulk_capture_is_ready():
            return []

        # Read out data and save to file.
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))

        file = open(filename, 'wb')
        download_size = 0
        buffer_size_bytes = 1 * 1024 * 1024
        data = []

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_EVCAP_CTRL, 0)
        time.sleep(1)

        while download_size < capture_size:
            result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_BULK_CAPTURE_DATA_R, c_byte, buffer_size_bytes)
            received_data_bytes = result[0]
            buffer = bytearray(result[1])
            if (capture_size - download_size) < received_data_bytes:
                received_data_bytes = capture_size - download_size
                file.write(buffer[:received_data_bytes])
                data.append(buffer[:received_data_bytes])
            else:
                file.write(buffer)
                data.append(buffer)
            download_size += received_data_bytes
            print("Capturing: {:<2%}".format(download_size / capture_size), end='\r')

        print('Stop bulk capture')

        file.close()
        return data

    def stop_bulk_capture(self):
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_BULK_CAPTURE_CONTROL_W, TSI_BULK_CAPTURE_STOP)
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_W_MEMORY_RESET, 0)

        return TSI_SUCCESS

    def bulk_capture(self, capture_size, path='', bulk_10bit=True, params=None):
        if self.device.get_tsi_name().find("DPRX") != -1 or self.device.get_tsi_name().find("USBC") != -1:
            self.dprx_start_event_capture(('AUX_BW'))

        actual_capture_size = self.start_bulk_capture(capture_size, bulk_10bit)
        if self.device.get_tsi_name().find("DPRX") != -1 or self.device.get_tsi_name().find("USBC") != -1:
            self.dprx_stop_event_capture()

        now = datetime.datetime.now()
        name_str = 'capture_%4d%02d%02d_%02d%02d%02d' % (now.year, now.month, now.day, now.hour, now.minute, now.second)

        if params is not None and len(params) == 4:
            folder_name = name_str[: 8] + "{}x{}_{}_{}bpc".format(params[0], params[1], params[2], params[3]) + \
                          name_str[7:]
        else:
            folder_name = name_str
        if path == '':
            path = os.getcwd()
        path += '\\' + folder_name + '\\'
        if not os.path.exists(path):
            os.makedirs(path)
        else:
            shutil.rmtree(path)
            os.makedirs(path)

        bulk_path = path + name_str + '.mainlink.bin'
        events_path = path + name_str + '.events.bin'

        events = self.download_captured_events()
        while not self.bulk_capture_is_ready():
            time.sleep(0.05)
            more_events = self.download_captured_events()
            events += more_events

        self.download_bulk_capture(actual_capture_size, bulk_path)

        if len(events):
            f = open(events_path, 'wb')
            for i in range(len(events)):
                f.write(events[i])
            f.close()

        return bulk_path
