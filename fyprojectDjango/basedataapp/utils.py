
def generate_new_code(code):
    return str(code).zfill(6)  # 6 digits
def generate_Event_code(year,company , struc, count ):
    YEAR= str(year).upper()
    COMPANY= str(company).upper()
    STRUC= str(struc).upper()
    COUNT= str(count).zfill(6)
    code= "_".join([YEAR,COMPANY,STRUC,COUNT])
    return code
