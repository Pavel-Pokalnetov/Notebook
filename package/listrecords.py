
class ListRecords:
    listRecords = {}

    def __init__(self):
        self.clean()

    def add(self, record):
        self.listRecords[record.id] = record

    def get_by_txt(self, textToSearch):
        result = []
        for _, record in self.listRecords.items():
            if record.getTextRecord().find(textToSearch) != -1:
                result.append(record)
        return result

    def clean(self):
        self.listRecords = {}

    def del_by_Id(self, id):
        self.listRecords.pop(id)

    def get_by_Id(self, id):
        return self.listRecords[id]

    def get_JSON(self):
        pass

    def get_CSV(self):
        pass

    def get_AllNotes(self):
        result = []
        for _, record in self.listRecords.items():
            result.append(record)
        return result

    def __len__(self):
        return len(self.listRecords)
