import sys

from arg_parser import argParser
from listrecords import ListRecords
from menu import Menu
from record import Record


class Controller:
    def __init__(self, model):
        self.print_help = None
        self.model = model
        self.records = self.model.load_notes()

    def interactive_start(self):
        menuitems = [
            ("1", "Показать все заметки", self.view_all),
            ("2", "Добавить заметку", self.add_note),
            ("3", "Удалить заметку", self.del_note),
            ("4", "Поиск заметки", self.search_notes_dialog),
            ("5", "Экспорт", self.export_notes),
            ("6", "Импорт", self.import_notes),
            ("2", "Помощь", self.print_help),
            ("Q", "Выход", self.exit_notes)]
        menu = Menu(menuitems)
        menu.prefixtext = "Заметки.\nГлавное меню\n"
        menu.run()

    def cli_start(self, commandline_args):
        """
        старт в не интерактивном режиме
        :param commandline_args: аргументы командной строки
        """
        arg = argParser(commandline_args)
        print(arg)
        if arg.add:
            records = self.model.load_notes()
            records.add(title=arg.title, text=arg.text)
        elif arg.delete:
            self.delete(id=arg.id, text=arg.text)
        elif arg.search_notes:
            self.search_notes(id=arg.id, text=arg.text)
        elif arg.imp != '-':
            self.import_notes(filename=arg.filename)
        elif arg.exp != '-':
            self.export_notes(filename=arg.filename)
        else:
            exit(1)
        exit(0)

    def add_note(self):
        title = input('Заголовок: ')
        if title == '': return
        text = input('Текст заметки: ')
        if text == '': return
        self.records.add(Record(title, text))
        return

    def del_note(self):
        return None

    def search_notes_dialog(self):
        while True:
            text = input('Строка поиска(посто для выхода): ')
            if text == '': return
            result = self.records.get_by_txt(text)
            if len(result) == 0:
                print("ничего не найдено")
            else:
                print('найдено {} записей'.format(len(result)))
                for r in result:
                    print(r.getTextRecord)
            print()
    def view_all(self):
        records = self.records.get_AllNotes()
        print("Всего записей {}".format(len(records)))
        if len(records)>0:
            for record in records:
                print(record.getTextRecord())

    def export_notes(self, filename):
        return None

    def import_notes(self, filename):
        return None

    def exit_notes(self):
        self.model.save_notes(self.records)
        exit(0)

    def delete(self, id, text):
        pass

    def search_notes(self, id, text):
        if len(self.records) == 0:
            return []
        search = (text if id == '' else id).lower()
        result = []
        for record in self.records.get_AllNotes():
            if record.getTextRecord().lower().find(search) != -1:
                result.append(record)
        return result
