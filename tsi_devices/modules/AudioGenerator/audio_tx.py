from tsi.tsi_devices.libs.lib_tsi.tsi import *
import pickle
import wave


class AudioGeneratorTx:

    def __init__(self, device):
        self.device = device

    def start_generate_audio(self, waveform=0, signal_frequency=1000, sample_rate=44100, bits=16, amplitude=60,
                             channels=2, read=False, path=""):

        if read is False:
            list_sample_rate = [22050, 44100, 88200, 176400, 24000, 48000, 96000, 192000, 32000, 768000]
            list_bits = [16, 20, 24]

            if self.device.get_tsi_name().find('USBC') == -1:
                if self.device.get_tsi_name().find('RXTX') == -1:
                    assert self.device.get_tsi_name().find('RX') == -1, "The device does not generate audio"
            assert 0 <= waveform <= 2, "Invalid type"
            assert sample_rate in list_sample_rate, "Invalid value. The value is not in the list"
            assert bits in list_bits, "Invalid value. The value is not in the list"
            memory_block_no = 2

            arr = []
            frame_offset = 8192 * 4096 * 4 * 2
            arr.append(frame_offset)
            arr.append(frame_offset)
            channels_mem = 2 if (channels <= 2) else 8
            audio_size = 4 * channels_mem * sample_rate
            aligned_size = (audio_size + 15) & (-16)
            arr.append(aligned_size)
            arr.append(8192 * 1024)

            TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_MEMORY_LAYOUT, arr, c_uint64, len(arr))

            TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_AUDGEN_SIGNAL_BLOCK, memory_block_no)
            TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_AUDGEN_SIGNAL_TYPE, waveform)
            TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_AUDGEN_CHANNEL_COUNT, channels)
            TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_AUDGEN_SAMPLE_RATE, sample_rate)
            TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_AUDGEN_SAMPLE_SIZE, bits)
            TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_AUDGEN_SIGNAL_FREQ, signal_frequency)
            TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_AUDGEN_SIGNAL_VOLUME, amplitude)
            TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_W_AUDGEN_CONTROL, 1)
        else:
            data_dict = self.read_audio(path)
            if data_dict is not None:
                TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_MEMORY_BLOCK_INDEX, data_dict.get("memory_block_no"))
                TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_AUDGEN_SIGNAL_BLOCK, data_dict.get("memory_block_no"))
                TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_W_MEMORY_WRITE, data_dict.get('data'))
                TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_AUDGEN_AUDIO_SIZE, data_dict.get('size'))

                res = self.set_config_bit(2, False)
                res = self.set_config_bit(3, True)

                audio_sts = self.create_audio_sts(data_dict)
                # TSIX_TS_SetConfigItem(device.get_handle(), TSI_VR_AG_CHANNELS_STS, audio_sts)
                if self.device.get_port_type() == "HD":
                    rate = data_dict.get("sample_rate")
                    frameRateNotMatch = (data_dict.get("channels") > 2) and data_dict.get("compressed")
                    if frameRateNotMatch:
                        rate *= 4
                    tp = 0
                    if data_dict.get("channels") == 8 and rate >= 64000:
                        tp = 3
                    res = self.set_config_bit(8, True)
                    res = self.set_config_bit(12, True)
                    # TSIX_TS_SetConfigItem(device.get_handle(), TSI_VR_AG_PACKET_TYPE, tp)

                TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_AUDGEN_SIGNAL_TYPE, 3)
                TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_AUDGEN_CHANNEL_COUNT, data_dict.get("channels"))
                TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_AUDGEN_SAMPLE_RATE, data_dict.get("sample_rate"))
                TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_AUDGEN_SAMPLE_SIZE, data_dict.get("bits"))
                TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_W_AUDGEN_CONTROL, 1)
            else:
                print("Invalid file")

    def stop_generate_audio(self):

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_W_AUDGEN_CONTROL, 0)

    @staticmethod
    def get_size_of_file(file):

        file.seek(0, os.SEEK_END)
        size = file.tell()
        file.seek(0, os.SEEK_SET)
        return size

    def read_audio(self, path="", audio_swap=False, sample_rate=44100, channels=2, bits=16):

        file = open(path, "rb")
        file_extension = path[path.rfind(".") + 1:]
        memory_block_no = 2
        file.close()
        if file_extension == 'bin':
            size = self.get_size_of_file(file)
            if size == 0:
                return None
            data = pickle.load(file)
            if audio_swap:
                for i in range(int(size / 2)):
                    x = data[i]
                    data[i + 1] = ((x & 0xff) << 8) | ((x & 0xff00) >> 8)
            corrected_buffer_size = len(data) * 2
            if bits == 32:
                pass
            return {"sample_rate": sample_rate, "channels": channels, "bits": bits, "memory_block_no": memory_block_no,
                    "size": size, "data": data, "compressed": False}

        elif file_extension == 'wav' or file_extension == 'wave':
            data = wave.open(path, 'rb')
            temp_channels = 2 if data.getnchannels() <= 2 else 8
            size = data.getnframes() * temp_channels * sizeof(c_uint32) + sizeof(c_uint32)
            channels = data.getnchannels()
            sample_rate = data.getframerate()
            bits = data.getsampwidth() * 8
            bytes_block = data.readframes(size)
            data.close()

            return {"sample_rate": sample_rate, "channels": channels, "bits": bits, "memory_block_no": memory_block_no,
                    "size": size, "data": bytes_block, "compressed": False}
        else:
            return None

    def set_config_bit(self, _bit: int, _set: bool):

        value = 0
        # Result = TSIX_TS_SetConfigItem(device.get_handle(), TSI_VR_AG_CONFIG, value)
        # if Result < TSI_SUCCESS:
        #     return Result

        if _set:
            value |= (1 << _bit)
        else:
            value &= ~(1 << _bit)

        # return TSIX_TS_SetConfigItem(device.get_handle(), TSI_VR_AG_CONFIG, value)
        return None

    @staticmethod
    def create_audio_sts(data):

        stsB = [None for i in range(4)]

        stsB[0] = 2 if data.get("compressed") else 0
        stsB[0] |= 4
        rate = data.get("sample_rate")
        bits = data.get("bits")

        frameRateNotMatch = (data.get("channels") > 2) and data.get("compressed")
        if frameRateNotMatch:
            rate *= 4

        dict_sample_rate = {22050: 4, 44100: 0, 88200: 8, 176400: 12, 24000: 6, 48000: 2, 96000: 10, 192000: 14,
                            32000: 3,
                            768000: 9}
        dict_bits = {16: 2, 20: 10, 24: 11}
        smpl = dict_sample_rate.get(rate)
        if frameRateNotMatch:
            smpl |= 0x30
        stsB[3] = smpl

        smlen = dict_bits.get(bits)
        stsB[4] = smlen

        return stsB
