import sqlite3
from sqlite3 import Error
import xlsxwriter 

class db_mgmt:
    def __init__(self,file_path):
        self.file_path = file_path
        self.conn = sqlite3.connect(self.file_path)
        self.c = self.conn.cursor()

    def tables_in_sqlite_db(self):
        self.c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        table_names_list = self.c.fetchall()
        return table_names_list
    
    def columns_in_table(self,table_name):
        self.c.execute(f"select * from {table_name} where 1=0;")
        return [d[0] for d in self.c.description]

    def read(self,table_name):
        rows = []
        
        rows.append(tuple(self.columns_in_table(table_name)))
        self.c.execute(f"SELECT * FROM {table_name}")
        rows_temp = self.c.fetchall()
        rows += rows_temp
        return rows

    def close(self):
        self.c.close()
        self.conn.close()

class xls_mgmt:
    def __init__(self,file_name="OUTPUT.xlsx"):
        self.file_path = file_name
        self.workbook = xlsxwriter.Workbook(file_name)
        
    def write_to_xlsx(self,table_name,data):
        self.worksheet = self.workbook.add_worksheet(table_name) 
        for row in data:
            for cell in row:
                    self.worksheet.write(int(data.index(row)),int(row.index(cell)),cell)  
    
    def close(self):
        self.workbook.close() 


if __name__ == "__main__":
    db_name = input("enter database name: ")
    db = db_mgmt(f"./{db_name}.db")
    excel = xls_mgmt()
    tables = db.tables_in_sqlite_db()
    for table in tables:
        data = db.read(table[0])
        excel.write_to_xlsx(table[0],data)
    excel.close()

