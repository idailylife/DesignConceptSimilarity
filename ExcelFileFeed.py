# -*- coding: utf-8 -*-
import xlrd
import Constants

class ExcelFileIn:
    def __init__(self, filename):
        self.filename = filename.decode('utf-8')
        self.data = xlrd.open_workbook(self.filename)

    def get_lines(self, sheet_index=0):
        table = self.data.sheets()[sheet_index]
        print("%d rows in..." % table.nrows)
        lines = []
        for row in range(table.nrows):
            lines.append(table.cell_value(row, 0).encode('utf-8').strip())
        return lines

if __name__ == '__main__':
    file = Constants.EXCEL_INPUT_FILE
    xlsFile = ExcelFileIn(file)
    lines = xlsFile.get_lines()
    print lines