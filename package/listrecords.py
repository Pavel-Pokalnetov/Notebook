
from copy import copy
from typing import TypedDict
from package.record import Record
import json
class ListRecords:
    

    listRecords = {}

    def __init__(self):
        self.clean()

    def get_dict(self):
        return copy(self.listRecords)

    def add(self, record:Record):  # ok
        self.listRecords[record.id] = record
        return record.get_id()

    def clean(self):
        self.listRecords = {}

    def get_by_text(self, text):
        result = []
        for record in self.listRecords.values():
            if record.getTextRecord().lower().find(text) != -1:
                result.append(record)
        return result

    def del_by_id(self, id):
        if id in self.listRecords:
            self.listRecords.pop(id)

    def get_by_id(self, id):
        return self.listRecords[id]

    def get_JSON(self):
        record: Record
        jsondict = {}
        for id, record in self.listRecords.items():
            jsondict[id] = {'title': record.get_title(),
                            'text': record.get_text()}
        return json.dumps(jsondict,
                          sort_keys=False,
                          ensure_ascii=False,
                          separators=(',', ':'))

    def get_CSV(self):
        # record:Record
        csv_raw = ""
        for record in self.listRecords.values():
            csv_raw += record.get_csv()+"\n"
        return csv_raw

    def get_AllNotes(self):
        result = []
        for record in self.listRecords.values():
            result.append(record)
        return result

    def __len__(self):
        return len(self.listRecords)
