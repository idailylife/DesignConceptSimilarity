# -*- coding: utf-8 -*-
import xlrd


class ExcelFileIn:
    def __init__(self, filename):
        self.filename = filename
        self.data = xlrd.open_workbook(filename)

    def get_lines(self, sheet_index=0):
        table = self.data.sheets()[sheet_index]
        print("%d rows in..." % table.nrows)
        lines = []
        for row in range(table.nrows):
            lines.append(table.cell_value(row, 0).encode('utf-8').strip())
        return lines

if __name__ == '__main__':
    file = r'C:\Users\inlab-dell\Documents\Tencent Files\397603432\FileRecv\方案条目汇总.xlsx'
    xlsFile = ExcelFileIn(file.decode('utf-8'))
    lines = xlsFile.get_lines()
    print lines