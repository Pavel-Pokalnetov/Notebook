import uuid


class Record():
    def __init__(self, title, text, id=''):
        self.id = uuid.uuid1() if id == '' else id
        self.title = title
        self.text = text

    def getTextRecord(self):
        txt = f"{self.title}{self.text}{self.id}"
        return txt

    def get_id(self):
        return self.id

    def get_title(self):
        return self.title

    def get_text(self):
        return self.text

    def get_tuple(self):
        return [self.title,self.text,self.id]