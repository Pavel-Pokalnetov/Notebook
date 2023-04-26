import datetime
from hashlib import md5
import uuid


class Record():

    def __init__(self, title, text, id='', date=''):
        self.id = md5(str(title+text).encode('utf-8')).hexdigest() if id == '' else id
        self.title = title
        self.text = text
        if date == '':
            now = datetime.datetime.now()
            formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
            self.date = formatted_date
        else:
            self.date = date

    def get_csv(self):
        return f"{self.id},\"{self.title}\",\"{self.text}\",\"{self.date}\""

    def getTextRecord(self):
        return f"{self.title}{self.text}{self.id}{self.date}"

    def get_id(self):
        return str(self.id)

    def get_title(self):
        return self.title

    def get_text(self):
        return self.text

    def get_date(self):
        return self.date

    def get_tuple(self):
        return [self.title, self.text, self.id, self.date]
