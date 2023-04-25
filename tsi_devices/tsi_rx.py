from .tsi_device import *
from .modules.HDCP.hdcp_rx import *
from .modules.AudioGenerator.audio_rx import *


class RX(TSIDevice):

    def __init__(self, device: TSIDevice):
        """

        General class for RX(sink) device. Inherited from class TSIDevice.

        The class contains the following fields:
        hdcp - Object of HdcpRx class. Contain some HDCP control methods.
        audio - Object of AudioGeneratorRx class. Needed to capture, downloading and saving events and audio frames.

        Parameters
        ----------
        device : TSIDevice
            Indicates the device on which the operation is to be carried out

        """
        super().__init__(device.get_handle(), device.get_type(), device.get_ports_and_roles())
        self._hdcp = HdcpRx(device)
        self._audio = AudioGeneratorRx(device)

    # HDCP Block
    def hdcprx_get_1x_status_all_info(self) -> HDCPStatusRX:
        """

        Return status info from RX side for HDCP type 1.X.

        Available info:
            active - HDCP status: active/not active (type: bool)
            keysLoaded - keys loaded info (type: int)
            enabled - HDCP status: enable/disable (type: bool)
            authenticated - authenticated status (type: bool)
            hwsupported - info of HW support HDCP (type: bool)
            productionKeysAvailable - production keys available status (type: bool)
            testKeysAvailable - test keys available status (type: bool)

        Returns
        -------
        result : HDCPStatusRX
            HDCP RX status

        """

        return self._hdcp.hdcprx_get_1x_status_all_info()

    def hdcprx_get_2x_status_all_info(self) -> HDCPStatusRX:
        """

        Return status full info from RX side for HDCP type 2.X.

        Available info:
            active - HDCP status: active/not active (type: bool)
            keysLoaded - keys loaded info (type: int)
            enabled - HDCP status: enable/disable (type: bool)
            authenticated - authenticated status (type: bool)
            hwsupported - info of HW support HDCP (type: bool)
            productionKeysAvailable - production keys available status (type: bool)
            testKeysAvailable - test keys available status (type: bool)

        Returns
        -------
        result : HDCPStatusRX
            HDCP RX status

        """

        return self._hdcp.hdcprx_get_2x_status_all_info()

    def hdcprx_1_set_capable(self, value: bool):
        """

        Set or clear HDCP 1.X capable.

        Parameters
        ----------
        value : bool
            State of assert status: True/False

        """
        self._hdcp.hdcprx_1_set_capable(value)

    def hdcprx_1_load_keys(self, value: int):
        """

        Set type of keys for HDCP 1.X:
            0 - unload keys
            1 - load test keys
            2 - load production keys

        Parameters
        ----------
        value : int
            Type of keys

        """
        self._hdcp.hdcprx_1_load_keys(value)

    def hdcprx_2_set_capable(self, value: bool):
        """

        Set or clear HDCP 2.X capable.

        Parameters
        ----------
        value : bool
            State of assert status: True/False

        """
        self._hdcp.hdcprx_2_set_capable(value)

    def hdcprx_2_load_keys(self, value: int):
        """

        Set type of keys for HDCP 2.X:
            0 - unload keys
            2 - load production keys

        Parameters
        ----------
        value : int
            Type of keys

        """
        self._hdcp.hdcprx_2_load_keys(value)

    # Audio block
    def start_capture_audio(self, n_frames=1):
        """

        Start capture audio.

        Parameters
        ----------
        n_frames : int
            Count of audio frames

        """
        self._audio.start_capture_audio(n_frames)

    def download_captured_audio(self, count=1000) -> list:
        """

        Download captured audio frames.

        Parameters
        ----------
        count : int
            Audio length in milliseconds

        Returns
        -------
        result : list
            Captured audio frames list

        """
        return self._audio.download_captured_audio(count)

    def combine_frames_to_wave_file(self, path, sample_rate, channels, sample_size, frames, save_to_bin_file=False):
        """

        Create an audio file with '.wav' extension from audio frames.

        Parameters
        ----------
        path : str
            Path to save 'wav' file.
        sample_rate : int
            Sample rate in audio
        channels : int
            Audio channels count
        sample_size : int
            Audio sample size
        frames : list
            Audio frames list
        save_to_bin_file : bool
            Path to save '.bin' file with all frames

        """
        self._audio.combine_frames_to_wave_file(path, sample_rate, channels, sample_size, frames, save_to_bin_file)

    def buffered_captured_audio_frames(self, path: str, count: int = 1, save_to_bin: bool = False,
                                       save_to_wave: bool = False):
        """

        Capturing and saving frames to files.
        Available extensions for files: bin, wav.

        Parameters
        ----------
        path : str
            Path to save captured frames (folder)
        count : int
            Number of frames to download
        save_to_bin : bool
            Flag for saving to bin file
        save_to_wave : bool
            Flag for saving to WAV file

        """
        self._audio.buffered_captured_audio_frames(path, count, save_to_bin, save_to_wave)

    def stop_capture_audio(self):
        """

        Stop capture audio.

        """
        self._audio.stop_capture_audio()

    def get_audio_channel_count(self) -> int:
        """

        Return current audio channels count.

        Returns
        -------
        result : int
            Audio channels count
        """
        return self._audio.get_audio_channel_count()

    def get_audio_sample_rate(self) -> int:
        """

        Return current audio sample rate.

        Returns
        -------
        result : int
            Audio sample rate

        """
        return self._audio.get_audio_sample_rate()

    def get_audio_sample_size(self) -> int:
        """

        Return current audio sample size.

        Returns
        -------
        result : int
            Audio sample size

        """
        return self._audio.get_audio_sample_size()
