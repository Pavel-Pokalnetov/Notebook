import uuid
class Record():
    def __init__(self,title, text):
        self.id = uuid.uuid1()
        self.title = title
        self.text = text

    def getTextRecord(self):
        txt =   f"{self.title}{self.text}"
    
