import sqlite3
from sqlite3 import Error
import xlsxwriter 

class db_mgmt:
    def __init__(self,file_path):
        self.file_path = file_path
        self.conn = sqlite3.connect(self.file_path)
        self.c = self.conn.cursor()

    def read(self,table_name):   
        self.c.execute(f"SELECT * FROM {table_name}")
        rows = self.c.fetchall()
        return rows

    def close(self):
        self.c.close()
        self.conn.close()

class xls_mgmt:
    def __init__(self,file_name="OUTPUT.xlsx"):
        self.file_path = file_name
        self.workbook = xlsxwriter.Workbook(file_name)
        self.worksheet = self.workbook.add_worksheet() 
    
    def write_to_xlsx(self,data):
        for row in data:
            for cell in row:
                    self.worksheet.write(int(data.index(row)),int(row.index(cell)),cell) 

    def close(self):
        self.workbook.close() 


if __name__ == "__main__":
    db_name,table_name = input("enter database name and table name:\nexample: linkedin_db,linkedinposts\n:").split(",")
    db = db_mgmt(f"./{db_name}.db")
    data = db.read(table_name)
    excel = xls_mgmt()
    excel.write_to_xlsx(data)
    excel.close()

