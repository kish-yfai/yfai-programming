import tkinter
from tkinter import filedialog
from payroll_classes import *
from field_definitions import *
from xlsx_output import *
from company_map import *
from sap_output import *
from sap_map import *


# GUI for selecting a file
root = tkinter.Tk()
root.withdraw()
file_paths = filedialog.askopenfilenames(title="Select your ODS data files",
                                         filetypes=(("Text Files", "*.txt"),))
check_array = []
sap_pcs = []
check_total = 0
print("Processing the file(s)...")

for i in file_paths:
    f = open(i, 'r')
    for line in f:
        # Grab the line_type (CHK, ERN, DED, TAX)
        line_type = line[:3]

        # CHK indicates a new employee/paycheck
        if line_type == "CHK" or line_type == "TRL":
            if (line_type == "CHK" and check_total > 0) or line_type == "TRL":
                check_array.append(new_check)
                company_code = sap_company(new_check.cost_center)
                if company_code.lower() != "not found":
                    if len(sap_pcs) > 0:
                        found = False
                        for pc in sap_pcs:
                            if pc.pc_num == new_check.cost_center[:4]:
                                pc.checks.append(new_check)
                                found = True
                                break
                        if not found:
                            temp_pc = sap_pc(new_check.cost_center[:4],
                                             company_code, [])
                            temp_pc.checks.append(new_check)
                            sap_pcs.append(temp_pc)
                    else:
                        temp_pc = sap_pc(new_check.cost_center[:4],
                                         company_code, [])
                        temp_pc.checks.append(new_check)
                        sap_pcs.append(temp_pc)
            if line_type == "CHK":
                line_dict = CHK_line(line)
                new_check = pay_check(line_dict["Company"],
                                      line_dict["Pay Check Number"],
                                      line_dict["Offcycle Indicator"],
                                      line_dict["Employee First Name"],
                                      line_dict["Employee Middle Name"],
                                      line_dict["Employee Last Name"],
                                      line_dict["Pay Group"],
                                      line_dict["Employee Type"],
                                      line_dict["Employee ID"],
                                      line_dict["Department"],
                                      line_dict["Pay End Date"],
                                      line_dict["Cost Center"],
                                      '',
                                      line_dict["Currency"],
                                      line_dict["Net Pay"],
                                      [], [], [])
                check_total += 1
        elif line_type == "ERN":
            line_dict = ERN_line(line)
            new_earnings = earnings_line(line_dict["Earnings Begin Date"],
                                         line_dict["Earnings End Date"],
                                         line_dict["Job Code"],
                                         line_dict["Job Code Title"],
                                         line_dict["Earnings Code"],
                                         line_dict["Comp/Hourly Rate"],
                                         line_dict["Earn Hours"],
                                         line_dict["Earnings Rate Used"],
                                         line_dict["Earnings Amount"])
            new_check.earnings.append(new_earnings)
            if len(line_dict["Default Account Code"]) >= 8:
                new_check.cost_center = line_dict["Default Account Code"][-8:]
                new_check.co_code = sap_company(new_check.cost_center)
            if (len(line_dict["Default Account Code"]) >
                    len(new_check.account_code)):
                new_check.account_code = line_dict["Default Account Code"]
        elif line_type == "DED":
            line_dict = DED_line(line)
            new_deductions = deductions_line(line_dict["Deduction Code"],
                                             line_dict["401K Election Percentage"],
                                             line_dict["Deduction Amount"])
            new_check.deductions.append(new_deductions)
        elif line_type == "TAX":
            line_dict = TAX_line(line)
            new_taxes = taxes_line(line_dict["Tax Type"],
                                   line_dict["Indicator for EE or ER"],
                                   line_dict["Tax Amount"])
            new_check.taxes.append(new_taxes)
    f.close()
print("A total of " + str(check_total) + " checks were processed.\n")
generate_xlsx(check_array)
generate_sap(sap_pcs)
