def CHK_line(input_line):
    CHK_dict = {
        "Rectype": input_line[0:3],
        "Company": input_line[3:7],
        "Pay Group": input_line[7:9],
        "Pay End Date": input_line[9:17],
        "Offcycle Indicator": input_line[17:18],
        "Employee ID": input_line[18:29],
        "Pay Check Number": input_line[29:44],
        "Check/Advice": input_line[44:45],
        "Check Date": input_line[45:53],
        "Pay Frequency": input_line[53:58],
        "Employee SSN": input_line[58:78],
        "Employee Type": input_line[78:79],
        "Employee Last Name": input_line[79:109],
        "Employee First Name": input_line[109:139],
        "Employee Middle Name": input_line[139:169],
        "Name Suffix": input_line[169:184],
        "Initials": input_line[184:189],
        "Location": input_line[189:199],
        "Location Name": input_line[199:229],
        "Location Address1": input_line[229:284],
        "Location Address2": input_line[284:339],
        "Location Address3": input_line[339:394],
        "Location Address4": input_line[394:449],
        "City": input_line[449:479],
        "State": input_line[479:485],
        "Postal": input_line[485:497],
        "Country Code": input_line[497:500],
        "Works at Home Indicator": input_line[500:501],
        "Department": input_line[501:511],
        "Cost Center": input_line[511:521],
        "Contract": input_line[521:532],
        "Expenditure": input_line[532:535],
        "Task": input_line[535:538],
        "Subtask": input_line[538:540],
        "Business Group": input_line[540:545],
        "Finance Organization": input_line[545:550],
        "Currency": input_line[550:553],
        "Total Gross Earnings": input_line[553:565],
        "Total Deductions Taken": input_line[565:577],
        "Total Taxes": input_line[577:589],
        "Net Pay": input_line[589:601],
        "Benefit Plan": input_line[601:607],
        "Benefit Plan Module": input_line[607:609]
    }
    for k, v in CHK_dict.items():
        CHK_dict[k] = v.strip()
    return CHK_dict


def ERN_line(input_line):
    ERN_dict = {
        "Rectype": input_line[0:3],
        "Company": input_line[3:7],
        "Pay Group": input_line[7:9],
        "Pay End Date": input_line[9:17],
        "Offcycle Indicator": input_line[17:18],
        "Employee ID": input_line[18:29],
        "Paycheck Number": input_line[29:44],
        "Job Code": input_line[44:50],
        "Job Code Title": input_line[50:80],
        "Earnings Begin Date": input_line[80:88],
        "Earnings End Date": input_line[88:96],
        "Gross Up Indicator": input_line[96:97],
        "Default Account Code": input_line[97:127],
        "Alternate Account Code": input_line[127:157],
        "Earnings Code": input_line[157:161],
        "Special Accumulator Indicator": input_line[161:162],
        "Cash/Non Cash Indicator": input_line[162:163],
        "Add to Gross": input_line[163:164],
        "Budget Effect": input_line[164:165],
        "Comp/Hourly Rate": input_line[165:184],
        "Earn Hours": input_line[184:191],
        "Earnings Rate Used": input_line[191:212],
        "Earnings Amount": input_line[210:222]
    }
    for k, v in ERN_dict.items():
        ERN_dict[k] = v.strip()
    return ERN_dict


def DED_line(input_line):
    DED_dict = {
        "Rectype": input_line[0:3],
        "Company": input_line[3:7],
        "Pay Group": input_line[7:9],
        "Pay End Date": input_line[9:17],
        "Offcycle Indicator": input_line[17:18],
        "Employee ID": input_line[18:29],
        "Paycheck Number": input_line[29:44],
        "Benefit Plan Type": input_line[44:48],
        "Benefit Plan Code": input_line[48:54],
        "Deduction Code": input_line[54:58],
        "Deduction Type": input_line[58:59],
        "401K Election Percentage": input_line[59:66],
        "Deduction Amount": input_line[66:78],
        "Deduction Payback Amount": input_line[78:90],
        "Deduction Refund Amount": input_line[90:102],
        "Deduction Not Taken": input_line[102:114],
        "Garnishment Company Fee": input_line[114:126]
    }
    for k, v in DED_dict.items():
        DED_dict[k] = v.strip()
    return DED_dict


def TAX_line(input_line):
    TAX_dict = {
        "Rectype": input_line[0:3],
        "Company": input_line[3:7],
        "Pay Group": input_line[7:9],
        "Pay End Date": input_line[9:17],
        "Offcycle Indicator": input_line[17:18],
        "Employee ID": input_line[18:29],
        "Pay Check Number": input_line[29:44],
        "FED/State": input_line[44:47],
        "Locality": input_line[47:57],
        "Tax Type": input_line[57:61],
        "Indicator for EE or ER": input_line[61:63],
        "Resident": input_line[63:64],
        "No Limit Gross Amount": input_line[64:76],
        "Taxable Gross Amount": input_line[76:88],
        "Tax Amount": input_line[88:100]
    }
    for k, v in TAX_dict.items():
        TAX_dict[k] = v.strip()
    return TAX_dict
