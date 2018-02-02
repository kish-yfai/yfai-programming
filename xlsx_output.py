import os
import xlsxwriter
from tqdm import tqdm
from company_map import *


def generate_xlsx(pay_checks):
    print("Generating the Excel workbooks...")
    current_path = os.path.curdir
    v = 1
    while os.path.exists(current_path + "\payroll_files_v" + str(v)):
        v += 1
    file_path = current_path + "\payroll_files_v" + str(v)
    os.mkdir(file_path)
    check_header = ["Line Type",
                    "Company",
                    "Paycheck Number",
                    "Offcycle Indicator",
                    "Employee ID",
                    "Employee Type",
                    "First Name",
                    "Middle Name",
                    "Last Name",
                    "Check Date",
                    "Cost Center",
                    "Account Code",
                    "Currency"]
    earnings_header = ["Job Code",
                       "Job Title",
                       "Beginning Period",
                       "Ending Period",
                       "Earnings Code",
                       "Code Description",
                       "Hourly Rate",
                       "Hours",
                       "Rate Used",
                       "Earnings Amount"]
    deductions_header = ["Deduction Code",
                         "Code Description",
                         "401K Election Percentage",
                         "Deduction Amount"]
    tax_header = ["Tax Code",
                  "Code Description",
                  "Liability Indicator",
                  "Tax Amount"]
    trail_header = ["Net Pay"]
    total_header = (check_header +
                    earnings_header +
                    deductions_header +
                    tax_header +
                    trail_header)
    used_codes = []
    # [0] == pc code, [1] == row count
    company_flag = False

    for emp in tqdm(pay_checks):
        company = get_company(emp.company)
        check_date = emp.date
        try:
            pc = int(emp.cost_center[:4])
        except ValueError:
            pc = emp.cost_center
        code_list = [str(pc), company]

        if company != "Not Found":
            company_flag = True
        else:
            company_flag = False

        for code in code_list:
            if code == code_list[1] and company_flag is False:
                continue
            if code not in used_codes:
                wb = xlsxwriter.Workbook(filename=(file_path + "/" +
                                                   code + "_Payroll.xlsx"))
                header_format = wb.add_format({'bold': True,
                                               'align': 'center',
                                               'bg_color': 'green',
                                               'border': True,
                                               'font_color': 'white'})
                ws = wb.add_worksheet(name="Paycheck Summary")

                c = 0
                for i in total_header:
                    ws.write(0, c, i, header_format)
                    c += 1

                r = 1
                for e in pay_checks:
                    if ((e.cost_center[:4] == code) or
                            (get_company(e.company) == code)):
                        common_items = [e.company,
                                        e.paycheck_number,
                                        e.offcycle_indicator,
                                        e.employee_id,
                                        e.employee_type,
                                        e.first_name,
                                        e.middle_name,
                                        e.last_name,
                                        e.date,
                                        e.cost_center,
                                        e.account_code,
                                        e.currency]

                        ern_c = len(check_header)
                        for ern in e.earnings:
                            ws.write(r, 0, "ERN")
                            c = 1
                            for i in common_items:
                                ws.write(r, c, i)
                                c += 1
                            ws.write(r, ern_c + 0, ern.job_code)
                            ws.write(r, ern_c + 1, ern.job_title)
                            ws.write(r, ern_c + 2, ern.begin_period)
                            ws.write(r, ern_c + 3, ern.end_period)
                            ws.write(r, ern_c + 4, ern.earnings_code)
                            ws.write(r, ern_c + 5, ern.earnings_desc)
                            ws.write(r, ern_c + 6, ern.std_rate)
                            ws.write(r, ern_c + 7, ern.hours)
                            ws.write(r, ern_c + 8, ern.ot_rate)
                            ws.write(r, ern_c + 9, ern.total_earnings)
                            r += 1

                        ded_c = len(check_header) + len(earnings_header)
                        for ded in e.deductions:
                            ws.write(r, 0, "DED")
                            c = 1
                            for i in common_items:
                                ws.write(r, c, i)
                                c += 1
                            ws.write(r, ded_c + 0, ded.deduction_code)
                            ws.write(r, ded_c + 1, ded.deduction_desc)
                            ws.write(r, ded_c + 2, ded.election_percent)
                            ws.write(r, ded_c + 3, ded.total_deductions)
                            r += 1

                        tax_c = (len(check_header) +
                                 len(earnings_header) +
                                 len(deductions_header))
                        for tax in e.taxes:
                            ws.write(r, 0, "TAX")
                            c = 1
                            for i in common_items:
                                ws.write(r, c, i)
                                c += 1
                            ws.write(r, tax_c + 0, tax.tax_code)
                            ws.write(r, tax_c + 1, tax.tax_desc)
                            ws.write(r, tax_c + 2, tax.who_paid)
                            ws.write(r, tax_c + 3, tax.total_taxes)
                            r += 1

                        trail_c = (len(check_header) +
                                   len(earnings_header) +
                                   len(deductions_header) +
                                   len(tax_header))
                        ws.write(r, 0, "NET")
                        c = 1
                        for i in common_items:
                            ws.write(r, c, i)
                            c += 1
                        ws.write(r, trail_c + 0, e.net_pay)
                        r += 1
                used_codes.append(code)
                wb.close()
