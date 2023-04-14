import sqlite3 as sl

from package.listrecords import ListRecords
from package.record import Record


class Model:

    def __init__(self, database):
        try:
            self.con = sl.connect(database)
            self.con.execute("""
                CREATE TABLE IF NOT EXISTS NOTES (
                    id TEXT,
                    title TEXT,
                    text TEXT
                ) ;
            """)
        except:
            print('Problem with accessing the database')
            exit()

    def load_notes(self):
        try:
            cursor = self.con.cursor()
            cursor.execute("""
            SELECT id,title,text FROM NOTES;
            """)
            records_slq = cursor.fetchall()
        except:
            print('Problem with accessing the database')
            exit()
        records = ListRecords()
        for id, title, text in records_slq:
            records.add(Record(title, text, id))
        return records

    def save_notes(self, records):
        if len(records) == 0: return
        try:
            cursor = self.con.cursor()
            cursor.execute("DROP TABLE IF EXISTS NOTES")
            self.con.execute("""
                            CREATE TABLE IF NOT EXISTS NOTES (
                                id TEXT,
                                title TEXT,
                                text TEXT
                            ) ;
                        """)
        except:
            print('Problem with accessing the database')
            exit()

        for record in records:
            id = record.get_id()
            title = record.get_title()
            text = record.get_text()
            insert_command="""INSERT INTO NOTES (id,title,text) VALUES ("{}","{}","{}");""".format(id,title,text)
            # print(insert_command)
            self.con.execute(insert_command)
        self.con.commit()
