import sqlite3

from app.eduvis.model.model_db import qry_insert
from app.eduvis.model.model_db import qry_select
from app.eduvis.model.model_db import qry_update
# from app.eduvis.model.model_db import qry_delete
from app.eduvis.model.initialize_db import boot_data

class Connection_DB:
    _db = 'eduvis.db'
    _model_db = 'db_sqlite.sql'
    _conn = None
    _cursor = None

    def connect(self):
        try:
            self._conn = sqlite3.connect(self._db)
            self._cursor = self._conn.cursor()
            
            if not self.db_exist(): #Verify db exist
                self.create_database()
            
            print("Connection with Database has been established.")

        except:
            print("Connection error with Database.")


    def disconnect(self):
        try:
            self._conn.close()
            print("Connection with Database has been closed.")
        except:
            print("Erro to close Database connection.")


    def db_exist(self):
        self._cursor.execute("""SELECT name FROM sqlite_master WHERE type='table';""")
        exist = self._cursor.fetchall()

        if len(exist) == 0:
            return False
        return True


    def create_database(self):
        print('Creating Database...')
        qry = open(self._model_db, 'r').read()
        self._cursor.executescript(qry)
        self.initialize_database()
        print('Database has been created.')


    def initialize_database(self):
        print('Adding default data...')        
        for i in range(0,len(boot_data)):
            table = boot_data[i]['table']
            data = boot_data[i]['data']
            self._cursor.executemany(qry_insert[table],data)
            self._conn.commit()


    def create_backup(self): #TODO
        pass


    def insert(self,table,data,feedback=False):
        try:
            self.connect()
            print("Recording on Database...")
            print(qry_insert[table])
            print(data)            
            self._cursor.execute(qry_insert[table], data)
            self._conn.commit()
            print("Data has been recorded on Database.")
            if feedback:
                return self._cursor.lastrowid
            self.disconnect()
        except:
            print("Error to record on Database.")

    def insert_many(self,table,data):
        try:
            self.connect()
            print("Recording on Database...")
            print(qry_insert[table])
            print(data)            
            self._cursor.executemany(qry_insert[table], data)
            self._conn.commit()
            print("Data has been recorded on Database.")            
            self.disconnect()
        except:
            print("Error to record on Database.")

    def update(self,table,data):
        try:
            self.connect()
            print("Updating on Database...")
            print(qry_update[table])
            print(data)
            self._cursor.execute(qry_update[table], data)
            self._conn.commit()
            print("Data has been updated on Database.")
            self.disconnect()
        except:
            print("Error to update on Database.")

    def update_many(self,table,data):
        try:
            self.connect()
            print("Updating on Database...")
            print(qry_update[table])
            print(data)
            self._cursor.executemany(qry_update[table], data)
            self._conn.commit()
            print("Data has been updated on Database.")
            self.disconnect()
        except:
            print("Error to update on Database.")

    def remove(self,table,data):
        pass


    def select(self,query,param=None):
        res = []
        try:
            self.connect()
            print("Getting data on Database...")
            if param == None:
                self._cursor.execute(qry_select[query])
            else:
                self._cursor.execute(qry_select[query], param)            
            
            for i in self._cursor.fetchall():
                res.append(i)
            
            print("Data has been retrieved from Database.")
            self.disconnect()            
        except:
            print("Error to retrieve data on Database.")

        return res