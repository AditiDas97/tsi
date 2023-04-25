from .tsi_device import *
from .modules.PatternGenerator.PGTX import *
from .modules.HDCP.hdcp_tx import *
from .modules.AudioGenerator.audio_tx import *


class TX(TSIDevice):

    def __init__(self, device: TSIDevice):
        """

        General class for TX(source) device. Inherited from class TSIDevice.

        The class contains the following fields:
        pg - Object of PatternGeneratorTx class. Allow set and get some video information (video resolution, bpc,
        colorimetry, color mode and so on)
        hdcp - Object of HdcpTx class. Contain some HDCP control methods.
        audio - Object of AudioGeneratorTx class. Needed to configure audio generator.

        Parameters
        ----------
        device : TSIDevice
            Indicates the device on which the operation is to be carried out

        """
        super().__init__(device.get_handle(), device.get_type(), device.get_ports_and_roles())
        self._pg = PatternGeneratorTx(device)
        self._hdcp = HdcpTx(device)
        self._audio = AudioGeneratorTx(device)

    # HDCP Block
    def hdcptx_get_1x_status_all_info(self) -> HDCPStatusTx:
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
        result : HDCPStatusTx
            HDCP TX status

        """

        return self._hdcp.hdcptx_get_1x_status_all_info()

    def hdcptx_get_2x_status_all_info(self) -> HDCPStatusTx:
        """

        Return status info from RX side for HDCP type 2.X.

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
        result : HDCPStatusTx
            HDCP TX status

        """

        return self._hdcp.hdcptx_get_2x_status_all_info()

    def hdcptx_1_encrypt(self, value: bool):
        """

        Enable or disable HDCP 1.X encrypt.

        Parameters
        ----------
        value : bool
            State of encrypt: True - Enable, False - Disable

        """
        self._hdcp.hdcptx_1_encrypt(value)

    def hdcptx_1_authenticate(self, value: bool):
        """

        Enable or disable HDCP 1.X authentication.

        Parameters
        ----------
        value : bool
            State of authentication: True - Enable, False - Disable

        """
        self._hdcp.hdcptx_1_authenticate(value)

    def hdcptx_1_load_keys(self, value: int):
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
        self._hdcp.hdcptx_1_load_keys(value)

    def hdcptx_2_encrypt(self, value: bool):
        """

        Enable or disable HDCP 2.X encrypt.

        Parameters
        ----------
        value : bool
            State of encrypt: True - Enable, False - Disable

        """
        self._hdcp.hdcptx_2_encrypt(value)

    def hdcptx_2_authenticate(self, value: bool):
        """

        Enable or disable HDCP 2.X authentication.

        Parameters
        ----------
        value : bool
            State of authentication: True - Enable, False - Disable

        """
        self._hdcp.hdcptx_2_authenticate(value)

    def hdcptx_2_load_keys(self, value: int):
        """

        Set type of keys for HDCP 2.X:
            0 - unload keys
            2 - load production keys

        Parameters
        ----------
        value : int
            Type of keys

        """
        self._hdcp.hdcptx_2_load_keys(value)

    def hdcp_get_1x_status(self) -> int:
        """

        Return int value of HDCP 1.X statux.

        Returns
        -------
        result : HDCPStatusTx
            HDCP 1.X status

        """
        return self._hdcp.hdcp_get_1x_status()

    def hdcp_get_2x_status(self) -> int:
        """

        Return int value of HDCP 2.X statux.

        Returns
        -------
        result : int
            HDCP 2.X status

        """
        return self._hdcp.hdcp_get_2x_status()

    # Audio Generator Block
    def start_generate_audio(self, waveform=0, signal_frequency=1000, sample_rate=44100, bits=16, amplitude=60,
                             channels=2, read=False, path=""):
        """

        Parameters
        ----------
        waveform : int
            Type of waveform:
                0 - 'Sine'
                1 - 'Square'
                2 - 'Sawtooth'
        signal_frequency : int
            Signal frequency (Default value = 1000)
        sample_rate : int
            Sample rate (Default value = 44100 Hz (44,100 kHz))
        bits : int
            Count of bits (Default value = 16)
        amplitude : int
            Amplitude in percent (Default value = 60 %)
        channels : int
            Channels count (Default value = 2)
        read : bool
            Flag of read input file
        path : str
            Path to input audio file (available extension: '.bin', '.wav')

        """

        self._audio.start_generate_audio(waveform, signal_frequency, sample_rate, bits, amplitude, channels, read,
                                         path)

    def stop_generate_audio(self):
        """

        Stop generate audio.

        """
        self._audio.stop_generate_audio()

    def get_size_of_file(self, file) -> int:
        """

        Return current size of audio file.

        Returns
        -------
        result : int
            Size of audio file

        """
        return self._audio.get_size_of_file(file)

    def read_audio(self, path="", audio_swap=False, sample_rate=44100, channels=2, bits=16) -> dict:
        """

        Read audio file.

        Parameters
        ----------
        sample_rate : int
            Sample rate (Default value = 44100 Hz (44,100 kHz))
        bits : int
            Count of bits (Default value = 16)
        channels : int
            Channels count (Default value = 2)
        path : str
            Path to input audio file (available extension: '.bin', '.wav')
        audio_swap : bool
            Flag of audio swap data

        Returns
        -------
        result : dict
            Audio info
        """
        return self._audio.read_audio(path, audio_swap, sample_rate, channels, bits)

    # Pattern Generator Block
    def apply_setting(self):
        """

        Apply all Pattern Generator settings.

        """
        self._pg.pg_apply_setting()

    def pg_get_predef_pattern_count(self) -> int:
        """

        Return number of predefined patterns available for the current interface

        Returns
        -------
        result : int
            Predefined patterns count
        """
        return self._pg.pg_get_predef_pattern_count()

    def pg_set_predef_pattern_params(self, params: list):
        """

        Set pattern specific parameters that can be used to alter the appearance of procedurally generated patterns.

        For pattern 'Solid color' (3):
            red = param[0] (min value = 0; max value = 255)
            green = param[1] (min value = 0; max value = 255)
            blue = param[2] (min value = 0; max value = 255)
        For pattern 'White V-Strips' (8):
            white_lines = param[0]
            black_lines = param[1]
        For pattern 'RGB 16 Wide strips' (9) and 'Motion pattern' (12):
            step = param[0]

        Parameters
        ----------
        params : list
            Params for pattern
        """

        self._pg.pg_set_predef_pattern_params(params)

    def pg_get_predef_pattern_params(self) -> int:
        """

        Return current pattern specific parameters.

        Returns
        -------
        result : int
            Pattern parameters

        """
        return self._pg.pg_get_predef_pattern_params()

    def pg_get_predef_timing_count(self) -> int:
        """

        Return the number of predefined timings available for the current interface.

        Returns
        -------
        result : int
            Number of predefined timings

        """
        return self._pg.pg_get_predef_timing_count()

    def pg_get_custom_timing_standart(self) -> int:
        """

        Return current custom timing.

        Returns
        -------
        result : int
            Custom timing

        """
        return self._pg.pg_get_custom_timing_standart()

    def pg_get_custom_timing_id(self) -> int:
        """

        Return current custom timing ID.

        Returns
        -------
        result : int
            Custom timing ID

        """
        return self._pg.pg_get_custom_timing_id()

    def pg_set_command(self, value: int):
        """

        Write value to apply current timing and pattern on the active output.
        Settings will be applied on all active streams.

        Parameters
        ----------
        value : int
            Value for apply settings
        """
        self._pg.pg_set_command(value)

    def pg_set_predef_timing_select(self, value: int):
        """

        Set the predefined timing.

        Parameters
        ----------
        value : int
            Predefined timing

        """
        self._pg.pg_set_predef_timing_select(value)

    def pg_get_enable_stream_count(self) -> int:
        """

        Return the maximum number of streams the currently selected interface can support.

        Returns
        -------
        result : int
            Count of streams

        """
        return self._pg.pg_get_enable_stream_count()

    def pg_set_enable_stream_count(self, value: int):
        """

        Set count of streams.

        Parameters
        ----------
        value : int
            Count of streams

        """
        self._pg.pg_set_enable_stream_count(value)

    def pg_set_link_pattern(self, value: str):
        """

        Select a predefined pattern for use.
        If you want to disable video, you need to select 'Disabled' pattern.
        
        Available patterns:
            "Disabled"
            "Color Bars"
            "Chessboard"
            "Solid color"
            "Solid white"
            "Solid red"
            "Solid green"
            "Solid blue"
            "White V-Strips"
            "RGB 16 Wide strips"
            "Color Ramp"
            "Color Square"
            "Motion pattern"
            "Custom image"
            "Playback"
            "Square Window"
            "DSC"

        Parameters
        ----------
        value : str
            Pattern

        """
        self._pg.pg_set_link_pattern(value)

    def pg_get_link_pattern(self) -> int:
        """

        Return a predefined pattern.

        Returns
        -------
        result : int
            Pattern: value from 0 to 16
            0 - "Disabled"
            1 - "Color Bars"
            2 - "Chessboard"
            3 - "Solid color"
            4 - "Solid white"
            5 - "Solid red"
            6 - "Solid green"
            7 - "Solid blue"
            8 - "White V-Strips"
            9 - "RGB 16 Wide strips"
            10 - "Color Ramp"
            11 - "Color Square"
            12 - "Motion pattern"
            13 - "Custom image"
            14 - "Playback"
            15 - "Square Window"
            16 - "DSC"

        """

        return self._pg.pg_get_link_pattern()

    def pg_set_stream_select(self, value: int):
        """

        Set the stream to be configured.

        Parameters
        ----------
        value : int
             value from 0 to Max stream count
        """
        self._pg.pg_set_stream_select(value)

    def pg_set_h_active(self, value: int):
        """

        Set the width of video frame that is visible on screen as number of pixel clocks.

        Parameters
        ----------
        value : int
            Width of video
        """

        self._pg.pg_set_h_active(value)

    def pg_get_h_active(self) -> int:
        """

        Return the width of video frame that is visible on screen as number of pixel clocks.

        Returns
        -------
        result : int
            Width of video
        """

        return self._pg.pg_get_h_active()

    def pg_set_v_active(self, value: int):
        """

        Set the height of the frame that is visible on screen as number of scanlines.

        Parameters
        ----------
        value : int
            Height of video

        """

        self._pg.pg_set_v_active(value)

    def pg_get_v_active(self) -> int:
        """

        Return the height of the frame that is visible on screen as number of scanlines.

        Returns
        -------
        result : int
            Height of video
        """

        return self._pg.pg_get_v_active()

    def get_resolution_active(self) -> tuple:
        """

        Return Active resolution.

        Returns
        -------
        result : tuple
            Active resolution

        """
        return self._pg.get_resolution_active()

    def pg_set_h_sync(self, value: int):
        """

        Set the width of horizontal sync as number of pixel clocks.

        Parameters
        ----------
        value : int
            Width of horizontal sync

        """

        self._pg.pg_set_h_sync(value)

    def pg_get_h_sync(self) -> int:
        """

        Return the width of horizontal sync as number of pixel clocks.

        Returns
        -------
        result : int
            Width of horizontal sync
        """

        return self._pg.pg_get_h_sync()

    def pg_set_v_sync(self, value: int):
        """

        Set the width of the vertical sync as number of scanlines.

        Parameters
        ----------
        value : int
            Width of the vertical sync

        """

        self._pg.pg_set_v_sync(value)

    def pg_get_v_sync(self) -> int:
        """

        Return the width of the vertical sync as number of scanlines.

        Returns
        -------
        result : int
            Width of the vertical sync
        """

        return self._pg.pg_get_v_sync()

    def get_resolution_sync(self) -> tuple:
        """

        Return Sync resolution.

        Returns
        -------
        result : tuple
            Sync resolution

        """
        return self._pg.get_resolution_sync()

    def pg_set_h_start(self, value: int):
        """

        Set number of pixels from end of H-Sync to start of active area.

        Parameters
        ----------
        value : int
            H Start value

        """

        self._pg.pg_set_h_start(value)

    def pg_get_h_start(self) -> int:
        """

        Return number of pixels from end of H-Sync to start of active area.

        Returns
        -------
        result : int
            H Start value
        """

        return self._pg.pg_get_h_start()

    def pg_set_v_start(self, value: int):
        """

        Set number of scan lines from end of V-Sync to start of active area.

        Parameters
        ----------
        value : int
            V Start value

        """

        self._pg.pg_set_v_start(value)

    def pg_get_v_start(self) -> int:
        """

        Return number of scan lines from end of V-Sync to start of active area.

        Returns
        -------
        result : int
            V Start value
        """

        return self._pg.pg_get_v_start()

    def get_resolution_start(self) -> tuple:
        """

        Return Start resolution.

        Returns
        -------
        result : tuple
            Start resolution

        """
        return self._pg.get_resolution_start()

    def pg_set_h_total(self, value: int):
        """

        Set the total width of a scanline in pixel clocks.

        Parameters
        ----------
        value : int
            Total width

        """

        self._pg.pg_set_h_total(value)

    def pg_get_h_total(self) -> int:
        """

        Return the total width of a scanline in pixel clocks.

        Returns
        -------
        result : int
            Total width
        """

        return self._pg.pg_get_h_total()

    def pg_set_v_total(self, value: int):
        """

        Set the total height of the frame as number of scanlines.

        Parameters
        ----------
        value : int
            Total height

        """

        self._pg.pg_set_v_total(value)

    def pg_get_v_total(self) -> int:
        """

        Return the total height of the frame as number of scanlines.

        Returns
        -------
        result : int
            Total height
        """

        return self._pg.pg_get_v_total()

    def get_resolution_total(self) -> tuple:
        """

        Return Total resolution.

        Returns
        -------
        result : tuple
            Total resolution

        """
        return self._pg.get_resolution_total()

    def pg_set_field_rate(self, rate):
        """

        Set the field rate as mHz (1000 = 1Hz). For non-interlaced timings, the field rate is same
        as frame rate.

        Parameters
        ----------
        rate : int
            Field rate as mHz
        """
        self._pg.pg_set_field_rate(rate)

    def pg_get_field_rate(self) -> int:
        """

        Return the field rate as mHz (1000 = 1Hz).

        Returns
        -------
        result : int
            Field rate as mHz
        """

        return self._pg.pg_get_field_rate()

    def pg_set_timing_flags(self, color_info='RGB', color_depth=8, h_sync_polarity=True, v_sync_polarity=True,
                            timf_meta_reduced_blank=1):
        """

        Set signal output timing flags and color information.
        These settings are used to set up the physical output signal.

        Parameters
        ----------
        color_info : str
            Info about color:
            "RGB", "YCbCr 4:4:4 ITU-601", "YCbCr 4:2:2 ITU-601", "YCbCr 4:2:0 ITU-601",
            "YCbCr 4:4:4 ITU-709", "YCbCr 4:2:2 ITU-709", "YCbCr 4:2:0 ITU-709"
        color_depth : int
            Info about color depth:
            6 bpc, 8 bpc, 10 bpc, 12 bpc, 16 bpc
        h_sync_polarity : bool
            Flag of H Sync polarity
        v_sync_polarity : bool
            Flag of V Sync polarity
        timf_meta_reduced_blank : int
            Value of Pattern generator Timf meta reduced blank (Available values: 0-3)
        """
        self._pg.pg_set_timing_flags(color_info, color_depth, h_sync_polarity, v_sync_polarity,
                                     timf_meta_reduced_blank)

    def pg_get_timing_flags(self) -> int:
        """

        Return the signal output timing flags and color information.

        Returns
        -------
        result : int
            Timing flags and color information
        """
        return self._pg.pg_get_timing_flags()

    def pg_set_pixel_format(self, value: int):
        """

        Set a pixel format:
            0x000 - RGB 8:8:8, 24-bit RGB image
            0x001 - RGB 16:16:16, 48-bit RGB image
            0x100 - YCbCr 8:8:8, 24-bit YCbCr “4:4:4” image
            0x101 - YCbCr 16:16:16, 48-bit YCbCr “4:4:4” image
            0x200 - YCbYCr 8:8:8:8, “16-bit” YCbCr “4:2:2” image
            0x201 - YCbYCr 16:16:16:16, “32-bit” YCbCr “4:2:2” image
            0x300 - YYCbYYCr 8:8:8:8:8:8, “12-bit” YCbCr “4:2:0” image
            0x301 - YYCbYYCr 16:16:16:16:16:16, “24-bit” YCbCr “4:2:0” image

        Parameters
        ----------
        value : int
            Pixel format

        """
        self._pg.pg_set_pixel_format(value)

    def pg_select_pattern_resolution(self, number=None, custom_params=None):
        """

        Enable or disable DSC.

        Parameters
        ----------
        number : int
            Number of default pattern resolution settings.
        custom_params : list
            Custom resolution. Will be used, if 'number' equal 'None'
        """
        self._pg.pg_select_pattern_resolution(number, custom_params)

    def pg_load_image(self, path: str, width: int, height: int):
        """

        Load custom image in Pattern Generator.

        Parameters
        ----------
        path : str
            Path to image
        width : int
            Width of image
        height : int
            Height of image

        """
        self._pg.pg_load_image(path, width, height)

    def pg_load_dsc_image(self, path: str):
        """

        Load DSC image in Pattern Generator.

        Parameters
        ----------
        path : str
            Path to image

        """
        self._pg.pg_load_dsc_image(path)

    def pg_check_status(self) -> str:
        """

        Return current PG status.

        Returns
        -------
        result : str
            PG status

        """
        return self._pg.pg_check_status()

    def pg_get_all_info(self) -> list:
        """

        Return all Pattern Generator information.

        Returns
        -------
        result : list
            PG info

        """
        return self._pg.pg_get_all_info()
