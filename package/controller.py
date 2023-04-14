from texttable import Texttable
from package.arg_parser import argParser
from package.menu import Menu
from package.record import Record


class Controller:
    def __init__(self, model):
        self.model = model
        self.records = self.model.load_notes()

    def interactive_start(self):
        """
        старт в интерактивном режиме
        с ткствовым меню
        :return:
        """
        menuitems = [
            ("V", "Показать все заметки", self.view_all),
            ("A", "Добавить заметку", self.add_note),
            ("D", "Удалить заметку", self.del_notes_dialog),
            ("S", "Поиск заметки", self.search_notes_dialog),
            ("E", "Экспорт", self.export_notes),
            ("I", "Импорт", self.import_notes),
            ("H", "Помощь", self.print_help),
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

    def del_notes_dialog(self):
        return None

    def search_notes_dialog(self):
        while True:
            text = input('Строка поиска (пусто для выхода): ')
            if text == '': return
            result = self.records.get_by_txt(text.lower())
            # print(result)
            if len(result) == 0:
                print("ничего не найдено")
            else:
                print('найдено {} записей'.format(len(result)))
                table = Texttable(max_width=100)
                table.header(["Заголовок", "Текст", "ID"])
                for r in result:
                    table.add_row(r.get_tuple())
                print(table.draw())
            print()

    def view_all(self):
        records = self.records.get_AllNotes()
        print("Всего записей {}".format(len(records)))
        if len(records) > 0:
            table = Texttable(max_width=100)
            table.header(["Заголовок", "Текст", "ID"])
            for record in records:
                title, text, id = record.get_tuple()
                table.add_row([title, text, id])
            table.set_cols_align(['l', 'l', 'r'])
            # table.set_deco(Texttable.HEADER | Texttable.BORDER)
            print(table.draw())

    def export_notes(self, filename):
        return None

    def import_notes(self, filename):
        return None

    def exit_notes(self):
        self.model.save_notes(self.records.get_AllNotes())
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

    def print_help(self):
        Menu().clrscr()
        try:
            with open('help', encoding='utf-8', mode="r") as help_file:
                text = help_file.read()
                print(text, end='\n\n')
        except:
            print('help not found')
