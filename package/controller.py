import json
from os import system
from texttable import Texttable
from package.arg_parser import argParser
from package.listrecords import ListRecords
from package.menu import Menu
from package.model import Model
from package.record import Record
import csv


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
            ("E", "Экспорт", self.export_notes),#ok
            ("I", "Импорт", self.import_notes),
            ("W", "Сохранить изменения", self.save_force),
            ("H", "Помощь", self.print_help),  # ok
            ("Q", "Выход", self.exit_notes)]#ok
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
        filename = '' if arg.filename=='' else arg.filename[0]
        # print(filename)
        force = False
        if arg.add:  # добавление строки OK
            self.add_cli(title, text)

        elif arg.delete:
            self.delete_cli(id=arg.id, text=arg.text)  # удаление
            force = True

        elif arg.search_notes:
            result = self.search_notes(id=arg.id, text=text)
            self.printTable(result)
            return
        
        elif arg.imp != '-':
            if filename=='':
                print('отсутствует обязательный параметр --filename FILENAME')
                exit(0)
            if arg.imp[0].lower()=='json':
                self.load_from_JSON_CSV(filename,typeFile='j')
            elif arg.imp[0].lower()=='csv':
                self.load_from_JSON_CSV(filename,typeFile='c')

        elif arg.exp != '-':
            if filename=='':            
                print('отсутствует обязательный параметр --filename FILENAME')
                exit(0)
            if arg.exp[0].lower()=='json':
                self.save_to_JSON_CSV(filename,typeFile='j')
            elif arg.exp[0].lower()=='csv':
                self.save_to_JSON_CSV(filename,typeFile='c')
            else:
                print('ошибка в опциях параметра -e')
                exit(1)

        elif arg.hlp:
                self.print_help(delay=False)
                exit(0)
        else:
            exit(1)
        
        self.save_force()
        exit(0)

    def add_cli(self, title, text):
        if (title == '' and text != ''):
            print("отсутствует обязательный параметр --tite ")
            exit()
        if (title != '' and text == ''):
            print("отсутствует обязательный параметр --text ")
            exit()
        if (title == '' and text == ''):
            print("отстствуют обязательные параметры --title --text ")
            exit()
        else:
            id = self.records.add(Record(title, text))
            print(f'добавлена заметка с id={id}')

    def add_note(self):
        print("Добавление заметки")
        title = input('Заголовок(пусто для отмены): ')
        if title == '':
            return
        text = input('Текст заметки(пусто для отмены): ')
        if text == '':
            return
        id = self.records.add(Record(title, text))
        print("Добавлена заметка")
        result = self.search_notes(id)
        self.printTable(result)
        self.delay()

    def del_notes_dialog(self):
        text = input(
            "Укажите ID или фрагмент текста для удаления заметки\n(пусто для отмены): ")
        if text == '':
            return

        self.del_by_text(text)
        return

    def del_by_text(self, text, force=False):  # ok
        result = []
        for id, record in self.records.get_dict().items():
            if record.getTextRecord().lower().find(text.lower()) != -1:
                result.append(id)
        if len(result) == 0:
            print('нет записей для удаления')
            return
        if force:
            for id in result:
                self.records.del_by_id(id)
            print('удалено', len(result), 'записей')
            return
            
        print('будет удалено', len(result), 'записей')
        while True:
            response = input('Удаляем?(Y/N):')
            if response.upper() == 'N':
                return
            if response.upper() == 'Y':
                for id in result:
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
        for record in result:
            title, text, id = record.get_tuple()
            table.add_row([title, text, id])
        table.set_cols_align(['l', 'l', 'r'])
        # table.set_deco(Texttable.HEADER | Texttable.BORDER)
        print(table.draw())

    def view_all(self,records = []):
        if records==[]:
            records=self.records.get_AllNotes()
        print("Всего записей {}".format(len(records)))
        if len(records) > 0:
            self.printTable(records)
        self.delay()

    def save_force(self): 
        self.model.save_notes(self.records, force=True)

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
        # print(content)
        with open(filename, "w", encoding="utf-8") as fl:
            fl.write(content)

    def import_notes(self):
        menuitems = [
            ("C", "Импорт из в CSV", self.import_from_CSV_interact),
            ("J", "Импорт из JSON", self.import_from_JSON_interact),
            ("H","Справка по структуре CSV и JSON",self.import_help),
            ("Q", "Назад в главное меню", -1)]
        export_menu = Menu(menuitems)
        export_menu.prefixtext = "\nЭкспорт\n"
        export_menu.run(pause=False)
    
    def import_from_CSV_interact(self):
        fname = input("Укажите имя CSV файла(пусто для отмены): ")
        if fname == '':
            return
        count=self.load_from_JSON_CSV(fname, typeFile='c')
        print('загружено {} записей'.format(count))
        self.delay()

    def import_from_JSON_interact(self):
        fname = input("Укажите имя JSON файла(пусто для отмены): ")
        if fname == '':
            return
        count=self.load_from_JSON_CSV(fname, typeFile='j')
        print('загружено {} записей'.format(count))
        self.delay()

    def load_from_JSON_CSV(self,fname,typeFile):
        count_line=0
        try:
            if typeFile=='c':
                with open(fname,"r",encoding="utf-8") as fl:
                    csv_reader = csv.reader(fl,delimiter=',',quotechar='"')    
                    for line in csv_reader:
                        self.records.add(Record(title=line[1],text=line[2],id=line[0]))
                        count_line+=1
                return count_line
            else:
                with open(fname,"r",encoding="utf-8") as fl:
                    jsondict = json.load(fl)
                    for id, recordict in jsondict.items():
                        title=recordict.get('title')
                        text=recordict.get('text')
                        self.records.add(Record(id=id,title=title,text=text))
                        count_line+=1
                return count_line
        except:
            print("ошибка в процессе импорта")
            return count_line
    
    def import_help(self):
        print("в разработке")

    def exit_notes(self):
        self.model.save_notes(self.records)
        exit(0)

    def delete_cli(self, id, text):
        if (id == '' and text == ''):
            self.records.clean()
        if (id != ''):
            self.records.del_by_id(id)
        if (text != ''):
            self.records.del_by_txt(text)

    def search_notes(self, id:str='', text:str=''):
        if len(self.records) == 0:
            return []
        text = (text if id == '' else id)
        text = text.lower()
        result = []
        for record in self.records.get_AllNotes():
            if record.getTextRecord().lower().find(text) != -1:
                result.append(record)
        return result

    def print_help(self,delay=True):
        Menu().clrscr()
        try:
            with open('data\help', encoding='utf-8', mode="r") as help_file:
                text = help_file.read()
                print(text, end='\n\n')
        except:
            print('help not found')
        if delay: self.delay()

    def delay(self,clrscr=True):
        input("Ввод для продолжения...")
        if clrscr: system("cls")