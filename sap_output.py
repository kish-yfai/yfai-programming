from payroll_classes import *
from datetime import datetime
import os
from sap_map import *
from tqdm import tqdm
from xlsx_output import *
from payroll_codes import *


def generate_sap(sap_pcs):
    doc_type = "SA"
    currency = "USD"
    tid = "akishs"
    v = 1
    current_path = os.path.curdir
    while os.path.exists(current_path + "\SAP_payroll_v" + str(v)):
        v += 1
    file_path = current_path + "\SAP_payroll_v" + str(v)
    os.mkdir(file_path)
    fail_path = file_path + '\SAP_rejects.txt'
    fail_text = open(fail_path, 'w')
    fail_list = []
    doc_date = ""
    while doc_date == "":
        doc_date = input("Enter the document date in mm/dd/yyyy format: ")
        if date_check(doc_date) is False:
            doc_date = ""
            print("Invalid date input, try again.")
    post_date = doc_date
    ref_text = "PAYROLL"
    mo_str = str(datetime.now().month)
    day_str = str(datetime.now().day)
    doc_header = "YF_PAYROLL_" + mo_str + "_" + day_str
    new_ref = ""
    print("Generating SAP text files...")
    for pc in tqdm(sap_pcs):
        sap_array = []
        co_str = pc.company
        new_ref = ref_text + pc.pc_num
        dest_path = file_path + '\SAP_output' + pc.pc_num + '.txt'
        sap_text = open(dest_path, 'w')
        sap_text.write("H" + '\t' + co_str + '\t' + doc_type +
                       '\t' + doc_date + '\t' + post_date + '\t' + currency +
                       '\t' + new_ref + '\t' + doc_header + '\t' + '' + '\t' +
                       '' + '\t' + tid + '\t' + '' + '\n')
        for check in pc.checks:
            account_indicator = check.account_code[:5]
            direct = False
            indirect = False
            exception = False
            salary = False
            account_reject = False
            if account_indicator == '53010':
                direct = True
            elif account_indicator == '54000' or account_indicator == '54030':
                indirect = True
            elif account_indicator == '55000' and check.employee_type == 'E':
                exception = True
            elif account_indicator == '55000':
                salary = True
            else:
                account_reject = True
            combo_list = check.earnings + check.deductions + check.taxes
            for line in combo_list:
                if type(line) == earnings_line:
                    code = line.earnings_code
                    amount = line.total_earnings
                elif type(line) == deductions_line:
                    code = line.deduction_code
                    amount = line.total_deductions
                elif type(line) == taxes_line:
                    code = line.tax_code
                    amount = line.total_taxes
                else:
                    code = "error"
                    amount = 0
                if get_code(code, True) is True or amount == 0:
                    continue
                if account_reject:
                    fail_name = check.first_name + " " + check.last_name
                    fail_list.append([check.cost_center,
                                      fail_name,
                                      check.account_code,
                                      code,
                                      get_code(code),
                                      amount])
                    continue
                sap_account = sap_accounts(code,
                                           account_indicator,
                                           direct,
                                           indirect,
                                           exception,
                                           salary)
                if (sap_account.lower() == "not found" or
                        sap_account.lower() == "na"):
                    fail_name = check.first_name + " " + check.last_name
                    if type(line) == earnings_line:
                        fail_list.append([check.cost_center,
                                          fail_name,
                                          check.account_code,
                                          line.earnings_code,
                                          get_code(line.earnings_code),
                                          line.total_earnings])
                    elif type(line) == deductions_line:
                        fail_list.append([check.cost_center,
                                          fail_name,
                                          check.account_code,
                                          line.deduction_code,
                                          get_code(line.deduction_code),
                                          line.total_deductions])
                    elif type(line) == taxes_line:
                        fail_list.append([check.cost_center,
                                          fail_name,
                                          check.account_code,
                                          line.tax_code,
                                          get_code(line.tax_code),
                                          line.total_taxes])
                else:
                    use_company = False
                    if sap_account.lower().find("company code") != -1:
                        sap_account = sap_account[:5]
                        use_company = True
                    if len(sap_array) > 0:
                        found = False
                        for i in sap_array:
                            if use_company is False:
                                sap_cc = check.cost_center
                            else:
                                sap_cc = co_str
                            if use_company is False:
                                if (i.cc == sap_cc and
                                        i.account_num == sap_account):
                                    i.account_balance += amount
                                    found = True
                                    break
                        if found is False:
                            temp_account = sap_balance(sap_cc,
                                                       sap_account,
                                                       get_code(code),
                                                       amount)
                            sap_array.append(temp_account)
                    else:
                        temp_account = sap_balance(check.cost_center,
                                                   sap_account,
                                                   get_code(code),
                                                   amount)
                        sap_array.append(temp_account)
        line_num = 1
        sap_total = 0
        for i in sap_array:
            sap_total += round(i.account_balance, 2)
            if i.account_balance >= 0:
                post_key = '40'
            else:
                post_key = '50'
            if i.account_num[:1] == '5':
                text_cc = i.cc
            else:
                text_cc = ''
            sap_text.write(str(line_num) + '\t' + post_key + '\t' +
                           i.account_num + '\t' +
                           str(abs(round(i.account_balance, 2))) +
                           '\t' + text_cc + '\t' + i.cc[:4] + '\t' +
                           '' + '\t' + '' + '\t' + '' + '\t' + '' + '\t' +
                           i.account_desc + '\n')
            line_num += 1
        sap_text.write(str(line_num) + '\t' + '50' + '\t' +
                       '21290' + '\t' +
                       str(abs(round(sap_total, 2))) +
                       '\t' + '' + '\t' + co_str + '\t' +
                       '' + '\t' + '' + '\t' + '' + '\t' + '' + '\t' +
                       'Payroll Clearing' + '\n')
        sap_text.close()
    for l in fail_list:
        fail_text.write(l[0] + '\t' +
                        l[1] + '\t' +
                        l[2] + '\t' +
                        l[3] + '\t' +
                        l[4] + '\t' +
                        str(l[5]) + '\n')
    fail_text.close()


def date_check(date_str):
    # mm/dd/yyyy
    now = datetime.now()

    if len(date_str) != 10:
        return False
    try:
        if (int(date_str[:2]) > 12) or (int(date_str[:2]) < 1):
            return False
        elif ((int(date_str[-4:]) < now.year - 1) or
                (int(date_str[-4:]) > now.year + 1)):
            return False
        elif (int(date_str[3:5]) < 1 or
                int(date_str[3:5]) > 31):
            return False
        else:
            return True
    except ValueError:
        return False
