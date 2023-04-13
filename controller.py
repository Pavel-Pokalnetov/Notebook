import sys

from arg_parser import argParser
from menu import Menu
import interactive as intr
from record import Record


class Controller:
    def __init__(self,model):
        self.model = model
    def interactive_start(self):
        menuitems = [
            ("P", "Добавить заметку", intr.add_note(self)),
            ("A", "Удалить заметку",intr.del_note(self)),
            ("S", "Поиск заметки", intr.search_notes(self)),
            ("E", "Экспорт", intr.export_notes(self)),
            ("I", "Импорт", intr.import_notes(self)),
            ("Q", "Выход", lambda: exit())]
        menu = Menu([("1","Добавить запись",self.)])
        menu.run()
        exit()


    def add(self,title,text):
        record = Record(title,text)
        self.model.add_record(record)



    def delete(self,id,text):
        return None


    def view(self,id,text):
        return None


    def import_notes(self, filename):
        return None


    def export_notes(self, filename):
        return None

    def cli_start(self, commandline_args):
        """
        старт в не интерактивном режиме
        :param commandline_args: аргументы командной строки
        """
        arg = argParser(commandline_args)
        if arg.add:
            self.add(title=arg.title, text=arg.text)
        elif arg.delete:
            self.delete(id=arg.id, text=arg.text)
        elif arg.view:
            self.view(id=arg.id, text=arg.text)
        elif arg.imp != '-':
            self.import_notes(filename=arg.filename)
        elif arg.exp != '-':
            self.export_notes(filename=arg.filename)
        else:exit(1)
        exit(0)