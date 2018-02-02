def get_company(adp_company):
    if adp_company == "1033":
        desc = "US1"
    elif adp_company == "1034":
        desc = "US2"
    elif adp_company == "1090":
        desc = "YFUSA"
    else:
        desc = "Not Found"

    return desc
