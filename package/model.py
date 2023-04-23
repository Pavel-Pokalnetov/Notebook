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
        self.con.execute(
            "CREATE TABLE IF NOT EXISTS NOTES (id TEXT,title,date TEXT,text TEXT);")

    def load_notes(self):
        try:
            cursor = self.con.cursor()
            cursor.execute("""
            SELECT id,title,text,date FROM NOTES;
            """)
            records_slq = cursor.fetchall()
        except:
            print('проблема при работе с базой данных')
            exit(2)
        records = ListRecords()
        for id, title, text, date in records_slq:
            records.add(Record(title, text, id, date))
        return records

    def save_notes(self, records: ListRecords):
        try:
            cursor = self.con.cursor()
            cursor.execute("DROP TABLE IF EXISTS NOTES")
            self.con.execute(
                "CREATE TABLE IF NOT EXISTS NOTES (id TEXT,title TEXT,text TEXT, date TEXT);")
            if len(records.get_AllNotes()) != 0 : 
                for record in records.get_AllNotes():
                    id = record.get_id()
                    title = record.get_title()
                    text = record.get_text()
                    date = record.get_date()
                    insert_command = """INSERT INTO NOTES (id,title,text,date) VALUES ("{}","{}","{}","{}");""".format(
                        id, title, text, date)
                    # print(insert_command)
                    self.con.execute(insert_command)
            self.con.commit()

        except:
            print('проблема при работе с базой данных')
            exit(2)
