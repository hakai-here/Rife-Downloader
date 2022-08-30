import sqlite3
from src.constants import DATABASE

class Connection:
    def __init__(self):
        self.conn = sqlite3.connect(DATABASE)
        self.cursor = self.conn.cursor()

    def __exit__(self):
        self.conn.commit()
        self.conn.close()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS packages (
            Package TEXT NOT NULL,
            Source TEXT,
            Version TEXT ,
            Repository TEXT,
            Priority TEXT,
            Depends TEXT,
            Description TEXT,
            Size INT ,
            SHA256 TEXT ,
            MD5sum TEXT ,
            Filename TEXT 
        )''')
        
    def search(self, package):
        self.cursor.execute(
            f"SELECT Package,Version,Repository,Depends,Size,SHA256,MD5sum,Filename,Priority FROM packages WHERE Package = '{package}'")
        return self.cursor.fetchall()
    
    def search_by_dep(self, package,repo):
        self.cursor.execute(
            f"SELECT Package,Version,Repository,Depends,Size,SHA256,MD5sum,Filename,Priority FROM packages WHERE Package = '{package}' AND instr(Repository,'{repo}')")
        return self.cursor.fetchall()
    
    def find(self, query):
        self.cursor.execute(
            'SELECT Package,Version,Repository,Description FROM packages WHERE instr(Package,?)', (query,))
        return self.cursor.fetchall()