from payroll_codes import get_code
from sap_map import *


class pay_check:
    def __init__(self,
                 company,
                 paycheck_number,
                 offcycle_indicator,
                 first_name,
                 middle_name,
                 last_name,
                 pay_group,
                 employee_type,
                 employee_id,
                 department,
                 date,
                 cost_center,
                 account_code,
                 currency,
                 net_pay,
                 earnings=[],
                 deductions=[],
                 taxes=[]):
        self.company = company
        self.paycheck_number = paycheck_number
        self.offcycle_indicator = offcycle_indicator
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.pay_group = pay_group
        if employee_type == "S":
            self.employee_type = "Salary"
        elif employee_type == "H":
            self.employee_type = "Hourly"
        else:
            self.employee_type = employee_type
        self.employee_id = employee_id
        self.department = department
        self.date = date
        self.co_code = sap_company(cost_center)
        self.cost_center = cost_center
        self.account_code = account_code
        self.currency = currency
        self.net_pay = float(net_pay)
        self.earnings = earnings
        self.deductions = deductions
        self.taxes = taxes


class earnings_line:
    def __init__(self,
                 begin_period,
                 end_period,
                 job_code,
                 job_title,
                 earnings_code,
                 std_rate,
                 hours,
                 ot_rate,
                 total_earnings):
        self.begin_period = begin_period
        self.end_period = end_period
        self.job_code = job_code
        self.job_title = job_title
        self.earnings_code = earnings_code
        self.earnings_desc = get_code(earnings_code)
        self.std_rate = float(std_rate)
        self.hours = float(hours)
        if '-' in ot_rate:
            ot_rate = ot_rate.replace('-', '')
            self.ot_rate = ot_rate * -1
        else:
            self.ot_rate = float(ot_rate)
        self.total_earnings = float(total_earnings)


class deductions_line:
    def __init__(self,
                 deduction_code,
                 election_percent,
                 total_deductions):
        self.deduction_code = deduction_code
        self.deduction_desc = get_code(deduction_code)
        self.election_percent = float(election_percent)
        self.total_deductions = float(total_deductions)


class taxes_line:
    def __init__(self,
                 tax_code,
                 who_paid,
                 total_taxes):
        self.tax_code = tax_code
        self.tax_desc = get_code(tax_code)
        self.who_paid = who_paid
        if who_paid == "EE":
            self.total_taxes = -float(total_taxes)
        else:
            self.total_taxes = float(total_taxes)


class sap_pc:
    def __init__(self,
                 pc_num,
                 company,
                 checks=[]):
        self.pc_num = pc_num
        self.company = company
        self.checks = checks


class sap_balance:
    def __init__(self,
                 cc,
                 account_num,
                 account_desc,
                 account_balance):
        self.cc = cc
        self.account_num = account_num
        self.account_desc = account_desc
        self.account_balance = account_balance
