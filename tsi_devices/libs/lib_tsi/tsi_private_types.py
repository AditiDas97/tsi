TSI_VR_DPRX_BASE = 0x90000000 + 0x21000
TSI_VR_DPRX_DSC_DPCD_CONTROL = TSI_VR_DPRX_BASE + 0x50
TSI_VR_DPRX_DSC_DPCD_PROPERTIES = TSI_VR_DPRX_BASE + 0x51
TSI_DPRX_DSC_TEST_CRC = 0x50000000 + 0x21000 + 0x43
TSI_DPRX_CRD_FEATURES = 0x50000000 + 0x21000 + 0x63
TSI_DPRX_ALPM_LT_INFO_R = 0x50000000 + 0x21000 + 0x38
TSI_DPRX_ALPM_STATS_CONTROL_W = 0x50000000 + 0x21000 + 0x60
TSI_DPRX_ALPM_STATS_STATUS_R = TSI_DPRX_ALPM_STATS_CONTROL_W
TSI_DPRX_ALPM_STATS_VB_R = 0x50000000 + 0x21000 + 0x61
TSI_DPRX_ALPM_STATS_IFP_R = 0x50000000 + 0x21000 + 0x62
TSI_DPRX_ALPM_STATS_CTRL_W = TSI_DPRX_ALPM_STATS_CONTROL_W

TSI_GENERIC_STATUS = 0x210  # TSI State flags. NOTE: Access mode changes to R+W

TSI_CRC_DEFINITIONS = 0x00010300 + 14  # CRC definitions. Default setting is 0
TSI_CRC_WINDOW_0_0 = 0x00010300 + 15  # Left border/window pixel for first window 15..0. Top border/window line for first window 31..16. Default setting is 0
TSI_CRC_WINDOW_0_1 = 0x00010300 + 16  # Right border pixel/ window width for first window. 15..0. Bottom border line / window height for first window 31..16. Default setting is 0
TSI_CRC_WINDOW_1_0 = 0x00010300 + 17  # Left border/window pixel for second window 15..0. Top border/window line for second window 31..16. Default setting is 0
TSI_CRC_WINDOW_1_1 = 0x00010300 + 18  # Right border pixel/ window width for second window. 15..0. Bottom border line / window height for second window 31..16. Default setting is 0
TSI_CRC_WINDOW_2_0 = 0x00010300 + 19  # Left border/window pixel for third window 15..0. Top border/window line for third window 31..16. Default setting is 0
TSI_CRC_WINDOW_2_1 = 0x00010300 + 20  # Right border pixel/ window width for third window. 15..0. Bottom border line / window height for third window 31..16. Default setting is 0
TSI_CRC_WINDOW_3_0 = 0x00010300 + 21  # Left border/window pixel for fourth window 15..0. Top border/window line for fourth window 31..16. Default setting is 0
TSI_CRC_WINDOW_3_1 = 0x00010300 + 22  # Right border pixel/ window width for fourth window. 15..0. Bottom border line / window height for fourth window 31..16. Default setting is 0

TSI_R_LC_COUNT = 0x80000010  # Number of licenses available.
TSI_W_LC_SELECT = 0x80000011  # Index from 0 to LC_Count-1: Select which license to access through the CI's below
TSI_R_LC_CODE = 0x80000012  # License ID (To identify type of license: "Basic" / "Advanced" / etc...)
TSI_R_LC_NAME = 0x80000013  # Human readable name for license.
TSI_R_LC_GET_KEY = 0x80000014  # Key string (40 characters, including the terminating NULL)
TSI_W_LC_ADD_KEY = 0x80000015  # -> Write license key string. Matching key is validated and added.
TSI_W_LC_REMOVE_KEY = 0x80000016  # -> Write license key string. Matching key is deleted.
TSI_W_LC_HAS_CODE = 0x80000017  # Check if specified code is available on device.
TSI_R_LC_SHA_TYPE = 0x80000018  # Check SHA type used in device.

TSI_DSC_TX_CONTROL = 0x50000000 + 0x32000 + 0x00
TSI_DSC_TX_STATUS = 0x50000000 + 0x32000 + 0x00
TSI_DSC_TX_CRC = 0x50000000 + 0x32000 + 0x01

TSI_VIDCAP_HDCP_PROTECTED_R = 0x8000f000
TSI_VIDCAP_HDCP_DECRYPTED_R = 0x8000f001
TSI_HDCP_COMPLIANT_R = 0x8000f002
