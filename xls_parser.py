import xlrd


def pars_xls(file_path):
    data = []
    rb = xlrd.open_workbook(file_path)
    sheet = rb.sheet_by_index(0)
    tmp = True
    headers = ['Login', 'Password', 'Middle_name', 'Card_number', 'Date', 'Cvv']
    for rownum in range(sheet.nrows):
        row = sheet.row_values(rownum)
        if tmp:
            if row != headers:
                return ("Wrong header params, should be:  Login, Password, Middle_name, Card_number, Date, Cvv")
            else:
                tmp = False
        else:
            data.append(row)
    return data
