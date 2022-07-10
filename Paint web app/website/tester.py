from openpyxl import Workbook
import openpyxl
import sqlite3

wb = Workbook()

path = "C:\\Users\\Gustaf\\Downloads\\Colors.xlsx"

wb = openpyxl.load_workbook(path, data_only=True)

ws = wb.active



conn = sqlite3.connect('database3.db')
c = conn.cursor()

for row in ws.iter_rows(min_row=1, max_col=1, values_only=True):
    


    c.execute('''
            INSERT INTO paints(paint_name) 
            VALUES 
                (?)''', (row[0],))

         


conn.commit()
conn.close()



