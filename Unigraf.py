import sys
from contextlib import contextmanager
from .tsi_lib import *

# sys.path.extend([".\tsi"])
# from tsi.tsi_lib import *


from time import sleep
import errno
import os, json, time

dp20Version = False


class UnigrafAPI:

    device_rx = None

    # def __init__(self):
    #     pass

    def __init__(self, logger = "", log_folder=""):
        self.logger = logger
        self.log_folder = log_folder
        pass

    def initialise_ucd(self):
        self.tsi = TsiLib()
        device = self.tsi.open_device(3, False)  # Selecting UCD Role as USB-C DP Alt-Mode Source and DisplayPort Sink
        self.device_rx = USBCRX500(device)

    def deinitialise_ucd(self):
        print("\n Deinitialise UCD500 device")
        self.tsi.close_device(self.device_rx)

    @contextmanager
    def setup_and_close_ucd(self):
        device_rxx = None
        try:
            print("Opening UCD device..")
            self.logger.info("Opening UCD device..")
            tsi = TsiLib()
            sleep(2)
            device = tsi.open_device(3, False)  # Selecting UCD Role as USB-C DP Alt-Mode Source and DisplayPort Sink
            device_rxx = USBCRX500(device)
            # ---------------------------------------------
            device_rxx.usbc_set_initial_role_ufp()
            print("UCD Device opened.")
            self.logger.info("UCD Device opened.")
            device_rxx.dprx_start_event_capture(
                    event_types=('AUX', 'AUX_BW', 'HPD', 'VBID_CHANGE', 'MSA_CHANGE', 'MSA_ALL', 'SDP', 'LINK_PAT'))
            sleep(3)
            # ---------------------------------------------
            dpcd_dump_dir = os.path.join(self.log_folder, "DPCD Dump")
            if not os.path.exists(dpcd_dump_dir):
                os.makedirs(dpcd_dump_dir)

            device_rxx.dprx_save_dpcd(0x00000000, 0x0021F,
                                          bytearray(device_rxx.dprx_read_dpcd(0x00000000, 0x0021F)),
                                          0x00000000, 0x0021F,
                                          bytearray(device_rxx.dprx_read_dpcd(0x00000000, 0x0021F)),
                                          dpcd_dump_dir + r"\\" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
            # -----------------------------------------------------------------------------------------------------------

            yield device_rxx

        finally:
            if device_rxx:
                # ---------------------------------------------
                device_rxx.dprx_stop_event_capture()
                sleep(3)
                event_log_dir = os.path.join(self.log_folder, "Event_Logs")
                sleep(2)
                try:
                    os.makedirs(event_log_dir)
                except OSError as e:
                    if e.errno != errno.EEXIST:
                        raise  # This was not a "directory exist" error..

                event_data = device_rxx.dprx_download_captured_events(
                    save_to_txt=True, save_to_bin=False, path_to_save=event_log_dir + r"\\" )
                # -------------------------------------------------------------------------------------------------

                print("Closing device")
                self.logger.info("Closing device")
                tsi.close_device(device_rxx)
                sleep(5)
            else:
                print("Device is not found/open")
                self.logger.info("Device is not found/open")


    def open_ucd_device(self, logger = "", log_folder="", config_dir="", aux_log=False):
        self.log_string = ""
        self.logger = logger
        self.aux_log = aux_log
        self.log_folder = log_folder
        # self.tsi = TsiLib()
        # device = self.tsi.open_device(3, False)  # Selecting UCD Role as USB-C DP Alt-Mode Source and DisplayPort Sink
        # self.device_rx = USBCRX500(device)
        self.device_rx.usbc_set_initial_role_ufp()
        sleep(5)
        if aux_log:
            self.device_rx.dprx_start_event_capture(
                event_types=('AUX', 'AUX_BW', 'HPD', 'VBID_CHANGE', 'MSA_CHANGE', 'MSA_ALL', 'SDP', 'LINK_PAT'))
            sleep(5)
        self.print_system_details()
        # self.setting_default_edid()
        self.setting_8k_edid()
        sleep(3)

    def print_system_details(self):
        print(" *********** UCD Software and Firmware details ************\n")
        self.logger.info(
            " *********** UCD Software and Firmware details ************\n"
        )
        self.logger.info(
            f"{self.device_rx.get_full_name()} \n{self.device_rx.get_fw_version()}"
        )
        print(f"{self.device_rx.get_full_name()} \n{self.device_rx.get_fw_version()}")
        print(" ------------------------------------------------------------------------ \n")

    def setting_default_edid(self):
        default_edid_file = os.path.join(
            os.getcwd(), "default_EDID", "default_edid.hex")
        print("***********  Setting up default EDID  ***********")
        self.logger.info("***********  Setting up default EDID  ***********")
        data = self.device_rx.load_edid(default_edid_file)
        self.device_rx.write_edid(data)
        self.device_rx.dprx_set_assert_status(False)
        sleep(4)
        self.device_rx.dprx_set_assert_status(True)
        print(" ------------------------------------------------------------------------ \n")

    def setting_8k_edid(self):
        edid_8k_dell_24hz_file = os.path.join(
            os.path.dirname(__file__), "default_EDID", "7680_4320_24Hz.bin")
        # edid_8k_dell_24hz_file = os.path.join(
        #     os.getcwd(), "default_EDID", "7680_4320_24Hz.bin")
        print("#" * 20 + "Setting up 8K Resolution at 24Hz" + "#" * 20)
        self.logger.info("#" * 20 + "Setting up 8K Resolution at 24Hz" + "#" * 20)
        data = self.device_rx.load_edid(edid_8k_dell_24hz_file)
        self.device_rx.write_edid(data)
        self.device_rx.dprx_set_assert_status(False)
        sleep(4)
        self.device_rx.dprx_set_assert_status(True)
        print(" ------------------------------------------------------------------------ \n")

    def close_ucd_device(self):
        print("\n Closing UCD500 device")
        if self.aux_log:
            self.device_rx.dprx_stop_event_capture()
            sleep(5)
            event_log_dir = os.path.join(self.log_folder, "Event_Logs")
            sleep(2)
            try:
                os.makedirs(event_log_dir)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise  # This was not a "directory exist" error..

            event_data = self.device_rx.dprx_download_captured_events(
                save_to_txt=True, save_to_bin=False, path_to_save=event_log_dir + r"\\"
            )
            sleep(5)
        self.tsi.close_device(self.device_rx)
        print(" ------------------------------------------------------------------------ \n")
        # return

    def change_lanes_and_rate_resolution(self, lanes, rate):
        with self.setup_and_close_ucd() as device_rxx:
            print("#" * 10 + " Setting up lanes and rates in UCD " + "#" * 10 + "\n")
            print(f"Input config to be setup => lanes = {lanes} , rate = {rate}")
            # print(f"type(lanes) = {type(lanes)}")
            # print(f"type(rate) = {type(rate)}")
            print(" ------------------------------------------------------------------------ \n")
            print("UCD Device Version")
            print(f"{device_rxx.get_full_name()} \n{device_rxx.get_fw_version()}")
            device_rxx.dprx_set_max_lanes(lanes)
            sleep(2)
            if rate in (10, 13.5, 20):
                device_rxx.dprx_set_dp20_link_rate(rate)
            else:
                device_rxx.dprx_set_max_link_rate(rate)
            device_rxx.dprx_set_assert_status(False)
            sleep(2)
            device_rxx.dprx_set_assert_status(True)
            sleep(2)

            edid_8k_dell_30hz_file = os.path.join(
                os.path.dirname(__file__), "default_EDID", "7680_4320_30Hz.bin")
            data = device_rxx.load_edid(edid_8k_dell_30hz_file)
            device_rxx.write_edid(data)
            device_rxx.dprx_set_assert_status(False)
            sleep(4)
            device_rxx.dprx_set_assert_status(True)
            print(" ------------------------------------------------------------------------ \n")


    def set_dp_mode(self, dp2_enable=True):
        self.device_rx.dprx_set_link_flags(enableDP2=dp2_enable)

    def configure_lanes(self, lanes: int):
        self.device_rx.dprx_set_max_lanes(lanes)
        sleep(2)

    def configure_lane_rate(self, rate):
        global dp20Version
        # self.device_rx.usbc_set_initial_role_ufp()
        if rate in (10, 13.5, 20):
            dp20Version = True
            self.device_rx.dprx_set_dp20_link_rate(rate)
        else:
            self.device_rx.dprx_set_max_link_rate(rate)

    def get_lanes(self):
        with self.setup_and_close_ucd() as device_rxx:
            lanes = device_rxx.dprx_get_lane_count()
        sleep(2)
        return lanes

    def get_lane_rate(self):
        # global dp20Version
        # if dp20Version :
        with self.setup_and_close_ucd() as device_rxx:
            rate = device_rxx.dprx_get_dp20_link_rate()
            # rate =  round(self.device_rx.dprx_get_link_rate()*0.27, 1)
        sleep(1)
        return rate



    def measure_usbc_info(self):
        usbc_info = {}
        usbc_info["v_vbus"] = self.device_rx.usbc_get_bus_electrical_status()[0] / 1000
        usbc_info["i_vbus"] = self.device_rx.usbc_get_current_bus_electrical_status() / 1000
        usbc_info["cc1"] = self.device_rx.usbc_get_voltage_on_cc1() / 1000
        usbc_info["cc2"] = self.device_rx.usbc_get_voltage_on_cc2() / 1000
        usbc_info["v_conn"] = self.device_rx.usbc_get_vconn_voltage() / 1000
        usbc_info["i_conn"] = self.device_rx.usbc_get_vconn_current() / 1000

        return usbc_info

    def print_usbc_info(self):
        self.logger.info("#" * 20 + " USBC PDC info " + "#" * 20 + "\n")
        self.logger.info("Measuring USBC parameters =>")
        print("#" * 20 + " USBC PDC info " + "#" * 20 + "\n")
        print(" Measuring USBC parameters => ")
        measured_usbc_info = self.measure_usbc_info()
        for x in measured_usbc_info.keys():
            print(x, "=", measured_usbc_info[x])
            self.logger.info(f" {x} =  {measured_usbc_info[x]}")
        print(" ------------------------------------------------------------------------ \n")

    def check_is_dp_alt_mode_active(self):
        state = self.device_rx.usbc_get_dp_alt_mode_status() & 1
        print("#" * 20 + " DisplayPort Alternate Mode: " + "#" * 20 + "\n")
        if state:
            self.logger.info(" DisplayPort alternate mode is active.\n")
            print("DisplayPort alternate mode is active.\n")
            self.log_string += "DisplayPort alternate mode is active.\n"
        else:
            self.logger.info("DisplayPort alternate mode is not in use\n")
            print("DisplayPort alternate mode is not in use.\n")
            self.log_string += "DisplayPort alternate mode is not in use\n"
        print(" ------------------------------------------------------------------------ \n")

    def check_power_role(self):
        self.logger.info("#" * 20 + " Power role " + "#" * 20 + "\n")
        print("#" * 20 + " Power role " + "#" * 20 + "\n")
        self.log_string = ""
        data_role = self.device_rx.usbc_get_data_role()

        if not data_role:
            self.device_rx.usbc_set_role_control(2)
            # self.log_string += "Power Role Swap Requested\n"
            self.device_rx.usbc_set_pdc_control(10)
            time.sleep(1)

        data_role = self.device_rx.usbc_get_data_role()

        self.logger.info(
            "\n UCD-500 Power Role: {}\n"
            " DUT Power Role:     {}\n".format(
                "PD Source" if data_role else "PD Sink",
                "PD Source" if not data_role else "PD Sink",
            )
        )
        print(
            " UCD-500 Power Role: {}\n"
            " DUT Power Role:     {}\n".format(
                "PD Source" if data_role else "PD Sink",
                "PD Source" if not data_role else "PD Sink",
            )
        )
        print(" ------------------------------------------------------------------------ \n")

    def check_usbc_data_role(self):
        self.logger.info("#" * 20 + " Data role " + "#" * 20 + "\n")
        print("#" * 20 + " Data role " + "#" * 20 + "\n")
        if int(self.device_rx.usbc_get_data_role() & 1) == 1:
            self.logger.info("USB is in Down Facing Port (DFP)\n")
            print("USB is in Down Facing Port (DFP)\n")
        else:
            self.logger.info("USB is in Up Facing Port (UFP)\n")
            print("USB is in Up Facing Port (UFP)\n")
        print(" ------------------------------------------------------------------------ \n")

    def check_stream_info(self, device_rxx):
        # with self.setup_and_close_ucd() as device_rxx:
        device_rxx.dprx_set_msa_command(1)
        sleep(5)
        stream_count = device_rxx.dprx_get_msa_stream_count()
        print(f"Number of streams:{stream_count}\n")
        self.logger.info(f"Number of streams:{stream_count}\n")
        if stream_count == 1:
            both_stream_info = {0: {}}
        else:
            both_stream_info = {0: {}, 1: {}}
        for stream in range(stream_count):
            both_stream_info[stream][f"n_video"] = device_rxx.dprx_get_n_video(stream)
            both_stream_info[stream]["m_video"] = device_rxx.dprx_get_m_video(stream)
            both_stream_info[stream]["h_total"] = device_rxx.dprx_get_h_total(stream)
            both_stream_info[stream]["v_total"] =device_rxx.dprx_get_v_total(stream)
            both_stream_info[stream]["h_active"] = device_rxx.dprx_get_h_active(stream)
            both_stream_info[stream]["v_active"] = device_rxx.dprx_get_v_active(stream)
            both_stream_info[stream]["h_start"] = device_rxx.dprx_get_h_start(stream)
            both_stream_info[stream]["v_start"] = device_rxx.dprx_get_v_start(stream)
            both_stream_info[stream]["h_sync"] = device_rxx.dprx_get_h_sync(stream)
            both_stream_info[stream]["v_sync"] = device_rxx.dprx_get_v_sync(stream)
            both_stream_info[stream]["msa_misc"] = device_rxx.dprx_get_misc(stream)
            both_stream_info[stream]["frame_rate"] = device_rxx.dprx_get_frame_rate(stream)
            both_stream_info[stream]["vb_id"] = device_rxx.dprx_get_vbid(stream)
            both_stream_info[stream]["crc"] = device_rxx.dprx_get_crc_values()
        sleep(2)
        return both_stream_info

    def print_stream_info(self):
        self.logger.info("\n STREAM INFORMATION ==>"+"\n")
        print("\n STREAM INFORMATION ==>"+"\n")
        both_stream_info = self.check_stream_info()

        both_stream_info = self.check_stream_info()
        sleep(3)

        for stream_index in both_stream_info.keys():
            print(f"Stream data: {stream_index + 1}")
            each_stream = both_stream_info[stream_index]
            for x in each_stream.keys():
                self.logger.info(f"     {x}={each_stream[x]}")
                print(f"     {x}={each_stream[x]}")
        print(" ----------------------------------------------- \n")
        sleep(3)

    def check_timing_info(self, width, height, freq, all_resolutions):

        # ______Individual Resolution check_____
        if all_resolutions == 0 and height and width:
            self.logger.info(
                "#" * 20 + f" Unigraf_monitor_simulated = {width}X{height}@{freq}Hz "
                + "#" * 20 + "\n"
            )
            print(
                "#" * 20 + f" Unigraf_monitor_simulated = {width}X{height}@{freq}Hz "
                + "#" * 20 + "\n"
            )
            self.compare_edid(width, height, freq)
            print("#" * 40 + "\n")

        # _____All resolutions check_____:
        else:
            timing_directory = os.path.join(os.path.dirname(__file__), "default_EDID")
            for timing_file_name in os.listdir(timing_directory):
                if timing_file_name.endswith(".bin") and not (
                        timing_file_name.startswith("default")
                ):
                    with open(os.path.join(timing_directory, timing_file_name)) as fl:
                        (h, v, f) = timing_file_name[:-6].split("_")
                        self.logger.info(
                            "#" * 20
                            + f" Unigraf_monitor_simulated = {h}X{v}@{f}Hz "
                            + "#" * 20
                            + "\n"
                        )
                        print(
                            "#" * 20
                            + f" Unigraf_monitor_simulated = {h}X{v}@{f}Hz "
                            + "#" * 20
                            + "\n"
                        )
                        self.compare_edid(h, v, f)
                        print("#" * 40 + "\n")

    def compare_edid(self, width, height, freq):

        with self.setup_and_close_ucd() as device_rxx:

            resolution_file_name = str(width) + "_" + str(height) + "_" + str(freq) + "Hz.bin"
            # resolution_file_path = os.path.join(os.getcwd(), "default_EDID", resolution_file_name)
            resolution_file_path = os.path.join(os.path.dirname(__file__), "default_EDID", resolution_file_name)

            with open(resolution_file_path, mode="rb") as file:  # b is important -> binary
                initial_edid = file.read()
            loaded_edid = device_rxx.load_edid(resolution_file_path)
            device_rxx.write_edid(loaded_edid)
            device_rxx.dprx_set_assert_status(False)
            sleep(4)
            device_rxx.dprx_set_assert_status(True)
            sleep(2)
            generated_edid = device_rxx.read_edid()
            resolution = resolution_file_name[:-4].split("_")

            # assert bytearray(generated_edid).hex()[:512] == bytearray(initial_edid).hex()[:512], "EDID mismatch!!!"
            # self.logger.info(f"^Unigraf successfully configured to {resolution[0]} x {resolution[1]} @ {resolution[2]}")
            # print("^Unigraf successfully configured to", resolution[0], "x", resolution[1], "@", resolution[2])
            sleep(5)
            # self.check_stream_info()

            if (
                    int(resolution[0]),
                    int(resolution[1]),
            ) == device_rxx.dprx_get_resolution_active() and round(
                device_rxx.dprx_get_frame_rate()
            ) == int(
                resolution[2][:-2]
            ):
                print(
                    "#Unigraf successfully configured to",
                    resolution[0],
                    "x",
                    resolution[1],
                    "@",
                    resolution[2],
                )
                # self.logger.info(
                #     f"#Unigraf successfully configured to {resolution[0]} x {resolution[1]} @ {resolution[2]}" )

            else:
                print(
                    f"*Unigraf not configured to {resolution[0]}x{resolution[1]}@{resolution[2]}"
                )
                # self.logger.info(
                    # f"*Unigraf not configured to {resolution[0]}x{resolution[1]}@{resolution[2]}" )

    def get_dpcd_dump(self):
        dpcd_dump_dir = os.path.join(
            os.getcwd(), self.log_folder, "DPCD Dump"
        )
        os.makedirs(dpcd_dump_dir)
        self.device_rx.dprx_save_dpcd(0x00000000, 0x0021F,
                                      bytearray(self.device_rx.dprx_read_dpcd(0x00000000, 0x0021F)),
                                      0x00000000, 0x0021F,
                                      bytearray(self.device_rx.dprx_read_dpcd(0x00000000, 0x0021F)),
                                      dpcd_dump_dir + r"\\" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))

    def event_log(self, flag):
        if flag:
            # pass
            # self.device_rx.dprx_start_event_capture(event_types=('AUX',))
            self.device_rx.dprx_start_event_capture(event_types=('AUX', 'HPD', 'VBID_CHANGE', 'MSA_CHANGE', 'MSA_ALL',
                                                                 'SDP', 'LINK_PAT'))
            sleep(5)
            self.device_rx.dprx_set_assert_status(False)
            sleep(2)
            self.device_rx.dprx_set_assert_status(True)
            sleep(5)
            self.device_rx.dprx_stop_event_capture()
            sleep(2)
            event_log_dir = os.path.join(self.log_folder, "Event_Logs")
            try:
                os.makedirs(event_log_dir)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise  # This was not a "directory exist" error..

            captured_events_list = self.device_rx.dprx_download_captured_events(
                save_to_txt=True, save_to_bin=False, path_to_save=event_log_dir + r"\\"
            )
            # return captured_events_list
        else:
            pass

    def check_lanes_rate_resolution(self):
        with self.setup_and_close_ucd() as device_rxx:
            print("#" * 10 + " CHecking lanes and rates and stream information in UCD " + "#" * 10 + "\n")
            MAIN_LINK_CHANNEL_CODING_SET = device_rxx.dprx_read_dpcd(0x00000108, 0x00000001)
            if (MAIN_LINK_CHANNEL_CODING_SET == 1):
                print("   From DPCD Registers: Main Link Channel Encoding Set = 8b/10b")
            elif (MAIN_LINK_CHANNEL_CODING_SET == 2):
                print("   From DPCD Registers: Main Link Channel Encoding Set = 128b/132b")

            LANE_COUNT_SET = device_rxx.dprx_read_dpcd(0x00000101, 0x00000001)
            if (LANE_COUNT_SET == 1):
                print("   From DPCD Registers: Number of lanes = 1")
            elif (LANE_COUNT_SET == 2):
                print("   From DPCD Registers: Number of lanes = 2")
            elif (LANE_COUNT_SET == 4):
                print("   From DPCD Registers: Number of lanes = 4")

            LINK_BW_SET = device_rxx.dprx_read_dpcd(0x00000100, 0x00000001)
            if (MAIN_LINK_CHANNEL_CODING_SET == 1):
                if(LINK_BW_SET == 6):
                    print("   From DPCD Registers: Rate = 1.62 Gbps/lane (RBR)")
                elif(LINK_BW_SET == 10):
                    print("   From DPCD Registers: Rate = 2.7 Gbps/lane (HBR)")
                elif(LINK_BW_SET == 20):
                    print("   From DPCD Registers: Rate = 5.4 Gbps/lane (HBR2)")
                elif(LINK_BW_SET == 30):
                    print("   From DPCD Registers: Rate = 8.1 Gbps/lane (HBR3)")
            elif (MAIN_LINK_CHANNEL_CODING_SET == 2):
                if(LINK_BW_SET == 1):
                    print("   From DPCD Registers: Rate = 10 Gbps/lane (UHBR10)")
                elif(LINK_BW_SET == 2):
                    print("   From DPCD Registers: Rate = 20 Gbps/lane (UHBR20)")
                elif(LINK_BW_SET == 4):
                    print("   From DPCD Registers: Rate = 13.5 Gbps/lane (UHBR13.5)")

            (h_active, v_active) = device_rxx.dprx_get_resolution_active()
            print(f"\n Current Diplay Resolution : {h_active} X {v_active}")

            both_stream_info = self.check_stream_info(device_rxx)
            print("#" * 20 + " Stream info " + "#" * 20 + "\n")

            for stream_index in both_stream_info.keys():
                print(f"Stream data: {stream_index + 1}")
                each_stream = both_stream_info[stream_index]
                for x in each_stream.keys():
                    print(f"     {x}={each_stream[x]}")

            print(" --------------------------------------------- \n")
            return (LANE_COUNT_SET, LINK_BW_SET, h_active, v_active)


