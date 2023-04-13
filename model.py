import sqlite3 as sl

from listrecords import ListRecords


class Model:

    def __init__(self,database):
        self.isConnection = False
        try:
            self.con = sl.connect(database)
        except:
            print('Problem with accessing the database')
            exit()

        with self.con:
            self.con.execute("""
                CREATE TABLE NOTES (
                    id TEXT,
                    title TEXT,
                    text TEXT
                );
            """)
    def get_note_by_id(self,id):
        records = ListRecords()
        return records

    def get_note_by_text(self,text):
        records = ListRecords()
        return records

    def add_record(self,record):
        return True

    def del_records_by_id(self,id):
        count = 0
        return count

    def del_records_by_text(self,text):
        count = 0
        return count

