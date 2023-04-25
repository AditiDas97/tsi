from tsi.tsi_devices.libs.lib_tsi.tsi import *


class FECCounters:

    def __init__(self):
        self.uncorrectedBlockErrors = [0, 0, 0, 0]
        self.correctedBlockErrors = [0, 0, 0, 0]
        self.bitErrors = [0, 0, 0, 0]
        self.parityBlockErrors = [0, 0, 0, 0]
        self.parityBitErrors = [0, 0, 0, 0]


class FECGeneratorSettings:

    def __init__(self):
        self.errorType = int()
        self.lanesCounts = [0, 0, 0, 0]
        self.delayMs = int()


class FecTx:

    def __init__(self, device):
        self.device = device

    def dptx_get_error_counters_fec(self):

        result = FECCounters()
        nl = self.device.dptx_get_link_status_lane_count()

        for i in range(nl):
            address = 0x120
            dpcd = self.device.dptx_read_dpcd(address, 1)
            dpcd[0] &= 1
            dpcd[0] |= (i << 4)
            for j in range(6):
                v = dpcd[0] | (j << 1)
                self.device.dptx_write_dpcd(address, 1, bytearray(v))
                val = self.device.dptx_read_dpcd(0x281, 1)
                if val[0] & 0x8000:
                    val = val[0] & 0x7FFF

                if j == 1:
                    result.uncorrectedBlockErrors[i] = val
                elif j == 2:
                    result.correctedBlockErrors[i] = val
                elif j == 3:
                    result.bitErrors[i] = val
                elif j == 4:
                    result.parityBlockErrors[i] = val
                elif j == 5:
                    result.parityBitErrors[i] = val

        return result

    def dptx_clear_counters_fec(self):

        address = 0x120
        dpcd = self.device.dptx_read_dpcd(address, 1)
        fecReady = dpcd[0] & 0x1
        dpcd[0] = fecReady
        self.device.dptx_write_dpcd(address, 1, dpcd)
        dpcd[0] |= 2
        self.device.dptx_write_dpcd(address, 1, dpcd)

    def dptx_generate_errors_fec(self, settings: FECGeneratorSettings):

        address = 0x120
        dpcd = self.device.dptx_read_dpcd(address, 1)
        dpcd[0] |= 2
        self.device.dptx_write_dpcd(address, 1, dpcd)
        delay = settings.delayMs * 100000
        # TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_VR_MLEG_CONTROL, 0)
        nl = self.device.dptx_get_link_status_lane_count()
        # TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_VR_MLEG_SYMBOL_REPLACE_A, 0x00010000)
        # TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_VR_MLEG_SYMBOL_REPLACE_MASK_A, 0x00010001)
        # TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_VR_MLEG_SYMBOL_REPLACE_B, 0x00000001)
        # TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_VR_MLEG_SYMBOL_REPLACE_MASK_B, 0x00010001)
        # TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_VR_MLEG_DELAY_COUNTER, delay)
        n = settings.lanesCounts[0] << 16
        # TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_VR_MLEG_LANEx_REPLACE_COUNTERS, n)
        n = settings.lanesCounts[1] << 16
        # TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_VR_MLEG_LANEx_REPLACE_COUNTERS + 1, n)
        n = settings.lanesCounts[2] << 16
        # TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_VR_MLEG_LANEx_REPLACE_COUNTERS + 2, n)
        n = settings.lanesCounts[3] << 16
        # TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_VR_MLEG_LANEx_REPLACE_COUNTERS + 3, n)

        ctrl = 0
        idx = settings.errorType
        ctrl |= (idx << 16)
        if nl == 1:
            ctrl |= (1 << 13)
        ctrl |= (1 << 12)
        ctrl |= (0xF << 4)
        ctrl |= (0xF << 4)
        if settings.lanesCounts[0]:
            ctrl |= (1 << 0)
        if settings.lanesCounts[1]:
            ctrl |= (1 << 1)
        if settings.lanesCounts[2]:
            ctrl |= (1 << 2)
        if settings.lanesCounts[3]:
            ctrl |= (1 << 3)

        # TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_VR_MLEG_CONTROL, ctrl)

    def dptx_prefer_enabled_fec(self, enable: bool):

        val = 0
        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_DPTX_FEC_CTRL, c_int)
        val = result[1]
        val |= 0x2 if enable else ~0x2
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_DPTX_FEC_CTRL, val)

    def dptx_enable_fec(self, enable: bool):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_DPTX_FEC_CTRL, c_int)
        val = result[1]
        val |= 0x8 if enable else 0x10
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_DPTX_FEC_CTRL, val)

    def dptx_intent_to_enable_fec(self, enable: bool):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_DPTX_FEC_CTRL, c_int)
        val = result[1]
        val |= 1 if enable else 4
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_DPTX_FEC_CTRL, val)

    def dptx_get_status_fec(self):

        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_DPTX_FEC_STATUS, c_int)
        enabled_status_fec = ((result[1] & 0x1) != 0)
        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_DPTX_FEC_CTRL, c_int)
        enabled_fec = ((result[1] & 0x2) != 0)

        return enabled_status_fec, enabled_fec
