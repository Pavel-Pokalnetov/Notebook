from texttable import Texttable
from package.arg_parser import argParser
from package.listrecords import ListRecords
from package.menu import Menu
from package.model import Model
from package.record import Record


class Controller:
    records: ListRecords
    model: Model

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
            ("V", "Показать все заметки", self.view_all),  # ok
            ("A", "Добавить заметку", self.add_note),  # ok
            ("D", "Удалить заметку", self.del_notes_dialog),  # ok
            ("S", "Поиск заметки", self.search_notes_dialog),  # ok
            ("E", "Экспорт", self.export_notes),
            ("I", "Импорт", self.import_notes),
            ("H", "Помощь", self.print_help),  # ok
            ("Q", "Выход", self.exit_notes)]
        mainmenu = Menu(menuitems)
        mainmenu.prefixtext = "Заметки.\nГлавное меню\n"
        mainmenu.run()

    def cli_start(self, commandline_args):
        """
        старт в не интерактивном режиме
        :param commandline_args: аргументы командной строки
        """
        arg = argParser(commandline_args)
        # print(arg)
        self.records = self.model.load_notes()
        title = ' '.join(arg.title)
        text = ' '.join(arg.text)
        print(arg)
        self.view_all()
        print('#'*40)
        force = False
        if arg.add:  # добавление строки OK
            self.add_cli(title, text)

        elif arg.delete:
            self.delete_cli(id=arg.id, text=arg.text)  # удаление
            force = True

        elif arg.search_notes:
            self.search_notes(id=arg.id, text=text)

        elif arg.imp != '-':
            self.import_notes(filename=arg.filename)

        elif arg.exp != '-':
            self.export_notes(filename=arg.filename)

        else:
            exit(1)
        self.view_all()

        self.model.save_notes(self.records, force)
        exit(0)

    def add_cli(self, title, text):
        if (title == '' and text != ''):
            print(" пропущен обязательный параметр --tite ")
            exit()
        if (title != '' and text == ''):
            print(" пропущен обязательный параметр --text ")
            exit()
        if (title == '' and text == ''):
            self.add_note()
        else:
            self.records.add(Record(title, text))

    def add_note(self):
        title = input('Заголовок: ')
        if title == '':
            return
        text = input('Текст заметки: ')
        if text == '':
            return
        self.records.add(Record(title, text))
        return

    def del_notes_dialog(self):
        text = input(
            "Укажите ID или фрагмент текста для удаления заметки\n(пусто для отмены): ")
        if text == '':
            return

        self.del_by_text(text)
        return

    def del_by_text(self, text):  # ok
        result: Record = []
        for id, record in self.records.get_dict().items():
            if record.getTextRecord().lower().find(text.lower()) != -1:
                result.append(id)
        if len(result) == 0:
            print('нет записей для удаления')
            return
        print('будет удалено', len(result), 'записей')

        while True:
            response = input('Удаляем?(Y/N):')
            if response.upper() == 'N':
                return
            if response.upper() == 'Y':
                for id in result:
                    # print(id)
                    self.records.del_by_id(id)
                return

    def search_notes_dialog(self):
        while True:
            text = input('Строка поиска (пусто для выхода): ')
            if text == '':
                return
            result = self.records.get_by_text(text.lower())
            if len(result) == 0:
                print("ничего не найдено")
            else:
                print('найдено {} записей'.format(len(result)))
                self.printTable(result)
            print()

    def printTable(self, result):
        table = Texttable(max_width=100)
        table.header(["Заголовок", "Текст", "ID"])
        for r in result:
            table.add_row(r.get_tuple())
        print(table.draw())

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

    def export_notes(self):
        menuitems = [
            ("C", "Экспорт в CSV", self.export_to_CSV_interact),
            ("J", "Экспорт в JSON", self.export_to_JSON_interact),
            ("Q", "Назад в главное меню", -1)]
        export_menu = Menu(menuitems)
        export_menu.prefixtext = "\nЭкспорт\n"
        export_menu.run(pause=False)

    def export_to_JSON_interact(self):
        fname = input("Укажите имя JSON файла(пусто для отмены): ")
        if fname == '':
            return
        self.save_to_JSON_CSV(fname, typeFile='j')

    def export_to_CSV_interact(self):
        fname = input("Укажите имя CSV файла(пусто для отмены): ")
        if fname == '':
            return
        self.save_to_JSON_CSV(fname, typeFile='c')

    def save_to_JSON_CSV(self, filename, typeFile):
        if typeFile == 'j':
            content = self.records.get_JSON()
        elif typeFile == 'c':
            content = self.records.get_CSV()
        else:
            return
        print(content)
        with open(filename, "w", encoding="utf-8") as fl:
            fl.write(content)

    def import_notes(self):
        return None

    def exit_notes(self):
        self.model.save_notes(self.records)
        exit(0)

    def delete_cli(self, id, text):
        if (id == '' and text == ''):
            self.records.clean()
        if (id != ''):
            self.records.del_by_id(id)
        if (text != ''):
            self.records.del_by_Text(text)

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
            with open('data\help', encoding='utf-8', mode="r") as help_file:
                text = help_file.read()
                print(text, end='\n\n')
        except:
            print('help not found')
    
    def delay():
        input("Ввод для продолжения...")