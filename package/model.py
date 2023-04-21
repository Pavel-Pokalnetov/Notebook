import sqlite3 as sl

from package.listrecords import ListRecords
from package.record import Record


class Model:
    def __init__(self, database):
        try:
            self.con = sl.connect(database)
        except:
            print('проблема при открытии базы данных')
            exit(2)
        self.con.execute("CREATE TABLE IF NOT EXISTS NOTES (id TEXT,title TEXT,text TEXT);")

    def load_notes(self):
        try:
            cursor = self.con.cursor()
            cursor.execute("""
            SELECT id,title,text FROM NOTES;
            """)
            records_slq = cursor.fetchall()
        except:
            print('проблема при работе с базой данных')
            exit(2)
        records = ListRecords()
        for id, title, text in records_slq:
            records.add(Record(title, text, id))
        return records

    def save_notes(self, records: ListRecords, force=False):
        if len(records.get_AllNotes()) == 0 and force != True:
            return
        try:
            cursor = self.con.cursor()
            cursor.execute("DROP TABLE IF EXISTS NOTES")
            self.con.execute("CREATE TABLE IF NOT EXISTS NOTES (id TEXT,title TEXT,text TEXT);")
            for record in records.get_AllNotes():
                id = record.get_id()
                title = record.get_title()
                text = record.get_text()
                insert_command = """INSERT INTO NOTES (id,title,text) VALUES ("{}","{}","{}");""".format(
                    id, title, text)
                # print(insert_command)
                self.con.execute(insert_command)
            self.con.commit()
            
        except:
            print('проблема при работе с базой данных')
            exit(2)