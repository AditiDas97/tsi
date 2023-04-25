from tsi.tsi_devices.libs.lib_tsi.tsi import *


class FECCounters:

    def __init__(self):
        self.uncorrectedBlockErrors = [0, 0, 0, 0]
        self.correctedBlockErrors = [0, 0, 0, 0]
        self.bitErrors = [0, 0, 0, 0]
        self.parityBlockErrors = [0, 0, 0, 0]
        self.parityBitErrors = [0, 0, 0, 0]


class FecRx:

    def __init__(self, device):
        self.device = device

    def dprx_get_error_counters_fec(self) -> FECCounters:

        result = FECCounters()
        nl = self.device.dprx_get_lane_count()

        for i in range(nl):
            address = 0x120

            dpcd = self.device.dprx_read_dpcd(address, 1)
            dpcd &= 1
            dpcd |= (i << 4)

            for j in range(6):
                v = dpcd | (j << 1)
                self.device.dprx_write_dpcd(address, 1, v)
                val = self.device.dprx_read_dpcd(0x281, 2)
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

    def dprx_clear_counters_fec(self):

        address = 0x120
        dpcd = self.device.dprx_read_dpcd(address, 1)
        fec_ready = dpcd[0] & 0x1
        dpcd[0] = fec_ready
        self.device.dprx_write_dpcd(address, 1, dpcd)
        dpcd[0] |= 2
        self.device.dprx_write_dpcd(address, 1, dpcd)

    def dprx_capable_fec(self, capable: bool, generate_hpd: bool = False):

        val = 0x1 if capable else 0x0
        TSIX_TS_SetConfigItem(self.device.get_handle(), TSI_DPRX_FEC_CTRL, val)
        if generate_hpd:
            self.device.dprx_set_hpd_pulse(1000 * 1000)

    def dprx_get_status_fec(self):

        status = 0
        ctrl = 0
        enabled_fec = bool()
        ready_fec = bool()
        capable_fec = bool()
        # result = TSIX_TS_GetConfigItem(self.get_handle(), TSI_DPRX_FEC_STATUS, c_int)
        # if result[0] >= TSI_SUCCESS:
        #     status = result[1]
        #     enabled_fec = (status & 0x1) != 0
        #     ready_fec = (status & 0x4) != 0
        result = TSIX_TS_GetConfigItem(self.device.get_handle(), TSI_DPRX_FEC_CTRL, c_int)
        ctrl = result[1]
        enabled_fec = (ctrl & 0x1) != 0
        return enabled_fec, ready_fec, capable_fec
