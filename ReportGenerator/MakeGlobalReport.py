import json
import ReportGenerator as rg
import os
import datetime
import inspect
import os
import sys


def get_script_dir(follow_symlinks=True):
    if getattr(sys, 'frozen', False):
        path = os.path.abspath(sys.executable)
    else:
        path = inspect.getabsfile(get_script_dir)
    if follow_symlinks:
        path = os.path.realpath(path)
    return os.path.dirname(path)


def make_global_report(path=os.getcwd() + '\\Output\\', use_case=''):
    def order(s):
        if s.find('Initial_LT') >= 0:
            return 0
        elif s.find('ILT') >= 0:
            return 0
        elif s.find('ALPM') >= 0:
            return 1
        elif s.find('VB') >= 0:
            return 2
        elif s.find('IFP') >= 0:
            return 3
        else:
            return 100

    if not os.path.exists(path):
        print(path + ' NOT EXIST!')
        exit(-1)
    files = os.listdir(path)

    report_files = []
    f = "BulkReportNxTx Report.json"

    for file in files:
        if os.path.isfile(os.path.join(path, file)) \
                and (file.find('TestReport') == -1) \
                and (file.find('.json') != -1):
            report_files.append(os.path.join(path, file))

    report_files.sort(key=lambda i_file: order(i_file))

    now = datetime.datetime.now()
    rname = 'GlobalTestReport_%4d%02d%02d_%02d%02d%02d' %\
            (now.year, now.month, now.day, now.hour, now.minute, now.second)

    report = rg.ReportGenerator()
    report.add_header(rname, 1, rg.RGStyle(16, align='center'))
    if use_case:
        report.add_header(use_case, 1, rg.RGStyle(14, align='center'))

    report.read_from_json_file(report_files)

    headers = [header for header in report.objects if header.__class__ == rg.RGHeader and header.table != 0]
    headers.sort(key=lambda header: order(header.header_style.id))
    for i in range(len(headers)):
        header = headers[i]
        header_text = header.content.replace(': ', '.'*(45 - len(header.content)))
        "<a href='#Initial_LT'>Header</a>"
        head = "<a href='#" + header.header_style.id + "'>" + header_text + "</a>"
        report.objects.insert(i + 1, rg.RGHeader(head, 1, rg.RGStyle(12, align='center')))
        if i == len(headers) - 1:
            report.objects.insert(i + 2, rg.RGHeader(" ", 1, rg.RGStyle(12, align='center')))
    report.objects.insert(len(headers) + 1, rg.BreakPage())

    # report = rg.ReportGenerator()
    #
    # report.read_from_json_file(["D:\\Project\\Project_python\\ReportGenerator\\Output\\BulkReportFrames_Geometry.json"])

    report.save_to_html("global")
    report.save_to_pdf("global")


if __name__ == '__main__':
    make_global_report()
