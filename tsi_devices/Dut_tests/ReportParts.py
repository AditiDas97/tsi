
ReportHead = "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.01 Transitional//EN\">\n" \
             "<html><head><title>Unigraf Test Report</title>\n" \
             "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=Windows-1252\">\n<style>\n" \
             " TABLE.DOCUMENT{width: 100%;}\n" \
             " P.CONTENTS{font-weight: bold;font-family: \"Arial\";font-size: 11pt;margin-left: 0.3cm;margin-top: " \
             "10;margin-bottom: 0.3cm;color: #000000;}\n" \
             " P.HEADING{background-color: #BBC3FF;margin-top: 0;margin-bottom: 0.5cm;margin-left: 0cm;font-weight: " \
             "bold;font-family: \"Arial\";font-size: 16pt;color: #000000;}\n" \
             " P.SUBHEADING{background-color: #BBC3FF;margin-top: 1.25cm;margin-bottom: 0.5cm;margin-left: " \
             "0.5cm;margin-right: 0;font-weight: bold;font-family: \"Arial\";font-size: 12pt;color: #000000;" \
             "text-transform: uppercase;}\n" \
             " P.GREENSUBHEADING{background-color: #DCFABC;margin-top: 0.5cm;margin-bottom: 0.5cm;margin-left: 0.6cm;" \
             "    margin-right: 0;    font-weight: bold;font-family: \"Arial\";font-size: 12pt;color: #000000;}\n" \
             " P.BODYTEXT{margin-top: 0;margin-bottom: 0;margin-left: 1.0cm;font-weight: medium;font-family:" \
             " \"Arial\";font-size: 11pt;color: #000000;}\n" \
             " P.TESTBODY{margin-top: 0;margin-bottom: 0;margin-left: 1.0cm;font-weight: medium;font-family: " \
             "\"Courier New\";font-size: 11pt;color: #000000;}\n" \
             " PRE.TESTBODY{margin-top: 0;margin-bottom: 0;margin-left: 1.0cm;font-weight: medium;font-family:" \
             " \"Courier New\";font-size: 11pt;color: #000000;}\n" \
             " P.BODYDETAILTEXT{margin-top: 0;margin-bottom: 0;margin-left: 1.4cm;font-weight: medium;font-family:" \
             " \"Arial\";font-size: 9pt;color: #000000;}\n" \
             "P.CONTENTS SELECT{font-weight: normal;font-family: \"Arial\";font-size: 11pt;width: 98%;margin-top: 0;" \
             "text-align: left;}\n" \
             "P.TABLE_HEADERS{background-color: #DCFABC;margin-top: 0;margin-bottom: 0;margin-left: 1.0cm;" \
             "font-weight: medium;font-family: \"Arial\";font-size: 12pt;color: #000000;}\n" \
             " P.TABLE_LINKS{margin-top: 0;margin-bottom: 0;margin-left: 1.0cm;font-weight: medium;font-family:" \
             " \"Arial\";font-size: 11pt;}\n" \
             "P.TABLE_LINKS2{margin-top: 0;margin-bottom: 0;margin-left: 1.0cm;font-weight: medium;font-family:" \
             " \"Arial\";font-size: 11pt; background-color: #DDDDDD;}\n" \
             "P.FAIL{margin-top: 0;margin-bottom: 0;background-color: #FFBCBC; font-weight: bold;font-family:" \
             " \"Arial\";font-size: 11pt;color: #000000;}\n" \
             "P.SUCCESS{margin-top: 0;margin-bottom: 0;background-color: #BCFFBC; font-weight: bold;font-family:" \
             " \"Arial\";font-size: 11pt;color: #000000;}\n" \
             "P.SKIP{margin-top: 0;margin-bottom: 0;background-color: #BCBCBC; font-weight: bold;font-family:" \
             " \"Arial\";font-size: 11pt;color: #000000;}\n</style>\n<script type=\"text/javascript\">\n" \
             "function Hide(iElementIndex) { document.getElementById(\"ID\"+iElementIndex).style.display = 'none'; }\n" \
             "function Show(iElementIndex) { document.getElementById(\"ID\"+iElementIndex).style.display = 'inline'; }\n" \
             "function HideAll(iDivCount) { for(var i=0;i<iDivCount;i++) { Hide(i); }}\n" \
             "function ShowAll(iDivCount) { for(var i=0;i<iDivCount;i++) { Show(i); }}\n" \
             "function ListHandler (iOptionValue) { if(iOptionValue==-1) { ShowAll(#count#); Hide(1); return; }" \
             " HideAll(#count#); Show(iOptionValue); }\n</script>\n</head>\n"

OptionListLine = "              <option value=\"#number#\"> #test_name# (#test_result#)</option>\n"

TestDescriptionLine = "<tr><td><p class=\"TABLE_LINKS#ending#\"><a href=\"javascript:ListHandler(#handler_number#)\">" \
                      "#test_group# / #test_name#</a></p></td><td><p class=\"#SUCCESS#\">&nbsp;#test_result#&nbsp;</p>" \
                      "</td></tr>\n"


Tables = "<div id=\"ID1\">\n<p class=\"BODYTEXT\">\n<p class=\"SUBHEADING\" style=\"margin-left: 0; margin-top:" \
         " 0;\">&nbsp;&nbsp;&nbsp;Summary of individual test runs</p>\n<table width=\"80%\"><colgroup><col " \
         "span=\"1\" style=\"width: 90%;\"><col span=\"1\" style=\"width: 10%;\"></colgroup>\n<tr><th><p " \
         "class=\"TABLE_HEADERS\">Test name</p></th><th><p class=\"TABLE_HEADERS\" style=\"margin-left: 0;\">Result" \
         "</p></th></tr>\n#test_description_lines#\n</table>#test_tables_list#\n"

DeviceDescription = "<p class=\"BODYTEXT\">\nDevice: #device_name#\n" \
                    "<br>Firmware Release Package: #firmware_package#\n" \
                    "<br>Detailed version data: #detailed_vdata#\n" \
                    "<br>TSI Python Wrapper version: #python_version#\n" \
                    "<br><br>Report generated: #date_time#<br>\n" \
                    "</p></p><p class=\"GREENSUBHEADING\">&nbsp;&nbsp;&nbsp;DUT<p class=\"BODYTEXT\">\n" \
                    "Device/Model name: #model_name#\n" \
                    "<br>HW Revision: #revision#\n" \
                    "<br>Serial number: #serial_number#\n" \
                    "<br>Firmware version: #firmware_version#\n" \
                    "<br>Driver version: #driver_version#\n" \
                    "<br><br>Testing conducted by: #conducted_by#\n" \
                    "<br><br>Remarks: #remarks#\n" \
                    "<p class=\"BODYDETAILTEXT\">\n"

TestTable = "<br><br></p></div><div id=\"ID#number#\">\n" \
            "<p class=\"SUBHEADING\" style=\"margin-left: 0; margin-top: 0;\">&nbsp;&nbsp;&nbsp;Test Details," \
            " Test #test_number#</p>\n" \
            "<p class=\"GREENSUBHEADING\">&nbsp;&nbsp;&nbsp;#test_name#</p>\n" \
            "<p class=\"BODYTEXT\">\n" \
            "Test Result: <b>#result#</b>\n" \
            "<br><br><b>Test Settings:</b></p>\n" \
            "<p class=\"BODYTEXT\">\n" \
            "#test_parameters#\n" \
            "</p><p class=\"GREENSUBHEADING\">&nbsp;&nbsp;&nbsp;Test Log</p><pre class=\"TESTBODY\">" \
            "#test_log#\n*** Test complete -- #result# ***\n"

ReportBody = "<body onload='ListHandler(0);'>\n" \
             "    <div><p class=\"HEADING\" id=\"top\">&nbsp;&nbsp;Unigraf Test Report</p></div>\n    <div>\n" \
             "        <table class=\"DOCUMENT\" cellpadding=\"0\" cellspacing=\"0\">\n            <colgroup>\n" \
             "                <col width=\"200\">\n                <col width=\"*\">\n            </colgroup>\n" \
             "            <td><p class=\"CONTENTS\">Select item to display</p></td>	\n" \
             "            <td><select id=\"testlist\" onclick=\"ListHandler (document.getElementById ('testlist')." \
             "value)\" onkeyup=\"ListHandler (document.getElementById ('testlist').value)\"></span>\n" \
             "               <option value=\"0\">Report Summary</option>\n" \
             "               <option value=\"1\">Test Summary</option>\n#optionList#\n" \
             "                    <option value=\"-1\">Show everything</option>\n                </select>\n" \
             "            </td>\n        </table>\n<div id=\"ID0\">\n" \
             "<p class=\"SUBHEADING\" style=\"margin-left: 0; margin-top: 0;\">&nbsp;&nbsp;&nbsp;Report summary</p>\n" \
             "<p class=\"GREENSUBHEADING\">&nbsp;&nbsp;&nbsp;Unigraf device\n#device_description#\n" \
             "</p></p></p><p class=\"GREENSUBHEADING\">&nbsp;&nbsp;&nbsp;Test results summary<p class=\"BODYTEXT\">\n" \
             "Total number of test runs: #runs#<br>Passed test runs: #passed#<br>Failed test runs: #failed#<br>Skipped" \
             " test runs: #skipped#<br>Aborted test runs: #aborted#\n<br></p></p></div>\n"

ReportFooter = "<br><br></pre></div>	</div>\n    <hr>\n    <p class=\"BODYTEXT\" style=\"text-align: center;\">\n" \
               "Unigraf Oy<span style=\"color:#808080;\"> |</span> Piispantilankuja 4 <span style=\"color:" \
               "#808080;\">|</span> 02240 Espoo <span style=\"color:#808080;\">|</span> Finland <span style=\"" \
               "color:#808080;\">|</span> +358-9-859 550<br />\n" \
               "        E-mail: <a href=\"mailto:info@unigraf.fi\">info@unigraf.fi</a><span style=\"color:" \
               "#808080;\"> |</span> Web site: <a href=\"http://www.unigraf.fi\">www.unigraf.fi</a>\n    </p>\n" \
               "</body>\n</html>\n"
