import record


class ListRecords:
    listRecords = {}

    def __init__(self):
        self.clean()

    def add(self, record):
        self.listRecords[record.id] = record

    def get_by_Text(self, textToSearch):
        result = []
        for key, record in self.listRecords.items():
            if record.getTextRecord() in textToSearch:
                result.append(record)
        return result

    def clean(self):
        self.listRecords = {}

    def del_by_Id(self, id):
        self.listRecords.pop(id)

    def get_by_Id(self, id):
        return self.listRecords[id]

    def getJSON(self):
        pass

    def getCSV(self):
        pass