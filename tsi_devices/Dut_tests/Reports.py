from .ReportParts import *
from datetime import datetime


class TestInfo:

    def __init__(self, name, test_id, group_name):
        self.name = name
        self.id = test_id
        self.group_name = group_name


class TestReport:

    def __init__(self, test_info):
        self.test_info = test_info
        self.configuration = ""
        self.result = ""
        self.logMessages = ""
        self.startTime = 0
        self.endTime = 0


class TestAdditionalInfo:

    def __init__(self, dutModelName: str = "", dutRevision: str = "", dutSerialNumber: str = "",
                 dutFirmwareVersion: str = "", dutDriverVersion: str = "", testedBy: str = "", remarks: str = ""):
        self.deviceName = str()
        self.deviceSerialNumber = str()
        self.deviceFirmwarePackage = str()
        self.deviceDetailedVdata = str()
        self.pythonVersion = str()
        self.dutModelName = dutModelName
        self.dutRevision = dutRevision
        self.dutSerialNumber = dutSerialNumber
        self.dutFirmwareVersion = dutFirmwareVersion
        self.dutDriverVersion = dutDriverVersion
        self.testedBy = testedBy
        self.remarks = remarks


class Report:

    def __init__(self):
        pass

    @staticmethod
    def replace_additional_info(test_additional_info: TestAdditionalInfo):
        result = DeviceDescription

        result = result.replace("#device_name#", test_additional_info.deviceName)
        result = result.replace("#firmware_package#", test_additional_info.deviceFirmwarePackage)
        result = result.replace("#detailed_vdata#", test_additional_info.deviceDetailedVdata)
        result = result.replace("#python_version#", test_additional_info.pythonVersion)
        date = datetime.now()
        _time = "{}-{}-{} {}:{}".format(date.day, date.month if date.month > 9 else "0{}".format(date.month), date.year,
                                        date.hour, date.minute)
        result = result.replace("#date_time#", _time)
        result = result.replace("#model_name#", test_additional_info.dutModelName)
        result = result.replace("#revision#", test_additional_info.dutRevision)
        result = result.replace("#serial_number#", test_additional_info.dutSerialNumber)
        result = result.replace("#firmware_version#", test_additional_info.dutFirmwareVersion)
        result = result.replace("#driver_version#", test_additional_info.dutDriverVersion)
        result = result.replace("#conducted_by#", test_additional_info.testedBy)
        result = result.replace("#remarks#", test_additional_info.remarks)

        return result

    def generate_html_report(self, path: str, test_additional_info: TestAdditionalInfo, reports: list):
        result = str()

        head = ReportHead
        head = head.replace("#count#", str((len(reports) + 2)))
        result += head

        body = ReportBody
        body = body.replace("#device_description#", self.replace_additional_info(test_additional_info))

        runs = 0
        failed = 0
        skipped = 0
        aborted = 0

        for i in range(len(reports)):
            runs += 1
            if reports[i].result == "FAILED":
                failed += 1
            elif reports[i].result == 'SKIPPED':
                skipped += 1
            elif reports[i].result == 'ABORTED':
                aborted += 1

        passed = runs - failed - skipped - aborted

        body = body.replace("#runs#", str(runs))
        body = body.replace("#passed#", str(passed))
        body = body.replace("#failed#", str(failed))
        body = body.replace("#skipped#", str(skipped))
        body = body.replace("#aborted#", str(aborted))

        options_list = ""
        for i in range(len(reports)):
            line = OptionListLine
            line = line.replace("#number#", str(i + 2))
            line = line.replace("#test_name#", reports[i].test_info.name)
            line = line.replace("#test_result#", reports[i].result)
            options_list += line + "\n"

        body = body.replace("#optionList#", options_list)
        result += body

        tables = Tables
        table_lines = ""
        for i in range(len(reports)):
            line = TestDescriptionLine
            line = line.replace("#handler_number#", str(i + 2))
            line = line.replace("#test_name#", reports[i].test_info.name)
            line = line.replace("#test_group#", reports[i].test_info.group_name)
            line = line.replace("#test_result#", reports[i].result)
            line = line.replace("#ending#", "2" if i % 2 else "")
            line = line.replace("#SUCCESS#", "SUCCESS")
            table_lines += line + "\n"

        tables = tables.replace("#test_description_lines#", table_lines)

        tables_list = ""
        for i in range(len(reports)):
            line = TestTable
            line = line.replace("#number#", str(i + 2))
            line = line.replace("#test_number#", str(i + 1))
            line = line.replace("#test_group#", reports[i].test_info.group_name)
            line = line.replace("#test_name#", reports[i].test_info.name)
            line = line.replace("#result#", reports[i].result)
            line = line.replace("#test_parameters#", reports[i].configuration)

            line = line.replace("#test_log#", reports[i].logMessages)
            tables_list += line + "\n"

        tables = tables.replace("#test_tables_list#", tables_list)

        result += tables

        footer = ReportFooter
        footer = footer.replace("#result#", "PASSED" if failed == 0 else "FAILED")
        result += footer

        file = open(path + ".html", 'w')
        file.write(result)
        file.close()
