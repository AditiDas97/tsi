import copy
import time
import wave
import warnings

from tsi.tsi_devices.libs.lib_tsi.tsi import *
import shutil
CAP_OPTION_AUDIO = 1
CAP_OPTION_VIDEO = 1 << 1
CAP_OPTION_EVENTS = 1 << 2
CAP_OPTION_MODE_LIVE = 1 << 3


class AudioFrameData:

    def __init__(self):
        self.data = bytearray()
        self.channels = 0
        self.samples = 0
        self.sampleSize = 0
        self.sampleRate = 0
        self.sampleFormat = 0
        self.frameCounter = 0

    def get_info_about_class(self):
        return self.__dict__


class AudioGeneratorRx:

    def __init__(self, device):
        self.device = device

    def start_capture_audio(self, n_frames: int = 1):

        mask = CAP_OPTION_AUDIO | CAP_OPTION_MODE_LIVE
        config = CAP_OPTION_AUDIO | CAP_OPTION_MODE_LIVE
        capturingConfig = 0

        if mask & CAP_OPTION_AUDIO and config & CAP_OPTION_AUDIO:
            config |= CAP_OPTION_VIDEO
            mask |= CAP_OPTION_VIDEO

        capturingConfig &= ~mask
        config &= mask
        capturingConfig |= config

        tsiConfig = 0

        if capturingConfig & CAP_OPTION_AUDIO:
            tsiConfig |= (1 << 4)
        if capturingConfig & CAP_OPTION_VIDEO:
            tsiConfig |= (1 << 3)
        if capturingConfig & CAP_OPTION_EVENTS:
            tsiConfig |= (1 << 5)
            TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_EVCAP_EVENT_SRC_EN, UCD_ALL_EVENTS)
        if capturingConfig & CAP_OPTION_MODE_LIVE:
            tsiConfig |= (1 << 2)
        else:
            tsiConfig |= (n_frames << 8)

        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_CAP_CONFIG, tsiConfig)

        if config:
            TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_W_CAP_COMMAND, 1)

    def download_captured_audio(self, count=1000):

        frames = []
        time_break = False
        TIME_LIMIT = 10  # 20 seconds waiting
        while count > 0 and not time_break:
            captured = 0
            start_time = time.time()
            while captured < 10 and count > 0:
                status = 0
                try:
                    status = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_AUDCAP_STATUS, c_int)[1]
                except BaseException:
                    status = 0
                current_time = time.time()
                if current_time - start_time > TIME_LIMIT:
                    time_break = True
                    break
                if not status:
                    continue

                audio_frame = AudioFrameData()
                audio_frame.channels = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_AUDCAP_CHANNEL_COUNT, c_int)[1]
                audio_frame.samples = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_AUDCAP_SAMPLE_COUNT, c_int)[1]
                audio_frame.sampleSize = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_AUDCAP_SAMPLE_SIZE, c_int)[1]
                audio_frame.sampleFormat = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_AUDCAP_SAMPLE_FORMAT,
                                                                 c_int)[1]
                audio_frame.sampleRate = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_AUDCAP_SAMPLE_RATE, c_int)[1]
                audio_frame.sampleTimeStamp = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_AUDCAP_TIMESTAMP,
                                                                    c_uint64)[1]
                audio_frame.frameCounter = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_AUDCAP_FRAME_COUNTER,
                                                                 c_int)[1]

                min_buff_size = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_AUDCAP_MIN_BUFFER_SIZE, c_uint32)[1]

                data = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_AUDCAP_SAMPLE_DATA, c_uint8, min_buff_size)[1]
                audio_frame.data = data

                frames.append(audio_frame)
                captured += 1
                count -= 1000 * len(audio_frame.data) / 2 / audio_frame.channels / audio_frame.sampleRate

            time.sleep(0.1)

        for frame in frames:
            data = copy.copy(frame.data)
            frame.data = bytearray()
            for byte in data:
                frame.data.append(byte)

        return frames

    def buffered_captured_audio_frames(self, path: str, count: int = 1, save_to_bin: bool = False,
                                       save_to_wave: bool = False):

        frames = self.download_captured_audio(count)
        i = 0

        for fr in frames:
            if save_to_bin:
                file = open(path + r'\audio_{count}_[{channels}_{sampleSize}_{sampleFormat}_{sampleRate}].bin'
                            .format(count=i, channels=fr.channels, sampleSize=fr.sampleSize,
                                    sampleFormat=fr.sampleFormat, sampleRate=fr.sampleRate), 'wb')
                file.write(fr.data)
                file.close()
            if save_to_wave:
                file = wave.Wave_write(path + ".WAV")
                file.setframerate(fr.sampleRate)
                file.setnchannels(fr.channels)
                file.setsampwidth(fr.sampleSize)
                file.writeframesraw(fr.data)
                file.close()
            i += 1

    @staticmethod
    def combine_frames_to_wave_file(path, sample_rate, channels, sample_size, frames, save_to_bin_file=False):
        if len(frames) > 0:
            file = wave.Wave_write(path + ".WAV")
            file.setframerate(sample_rate)
            file.setnchannels(channels)
            file.setsampwidth(sample_size)
            data = bytearray()
            for fr in frames:
                data += fr.data
            file.writeframesraw(data)
            file.close()
            if save_to_bin_file:
                bin_file = open(path + '.bin', 'wb')
                bin_file.write(data)
                bin_file.close()

    def stop_capture_audio(self):
        try:
            config = 0
            mask = 1
            tsiConfig = 0
            capturingConfig = 0
            capturingConfig &= ~mask
            config &= mask
            capturingConfig |= config
            if capturingConfig & CAP_OPTION_AUDIO:
                tsiConfig |= (1 << 4)
            if capturingConfig & CAP_OPTION_VIDEO:
                tsiConfig |= (1 << 3)
            if capturingConfig & CAP_OPTION_EVENTS:
                tsiConfig |= (1 << 5)
                TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_EVCAP_EVENT_SRC_EN, UCD_ALL_EVENTS)
            if capturingConfig & CAP_OPTION_MODE_LIVE:
                tsiConfig |= (1 << 2)
            else:
                tsiConfig |= (0 << 8)

            TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_CAP_CONFIG, tsiConfig)
            TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_W_CAP_COMMAND, 2)
        except BaseException:
            return -1

    def get_audio_channel_count(self):

        try:
            result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_AUDIO_CHANNELS, c_int)
            return result[1]
        except BaseException:
            return 0

    def get_audio_sample_rate(self):

        try:
            result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_AUDIO_SAMPLE_RATE, c_int)
            return result[1]
        except BaseException:
            return 0

    def get_audio_sample_size(self):

        try:
            result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_R_AUDIO_SAMPLE_SIZE, c_int)
            return result[1]
        except BaseException:
            return 0
