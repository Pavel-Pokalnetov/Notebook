from os import system


class Menu:  # класс меню
    '''
    класс меню
    elements = список кортежей
        кортеж = ("маркер","описание",метод)
        если метод в кортеже==-1 то menu.run() возвращает True
        это нужно для реализации выхода из меню реализованных
        во вложенных методах'''

    def __init__(self, elenemts=[]):
        self.elements = elenemts
        self.prefixtext = ''

    def print(self):
        print(self.prefixtext, end='')
        for (mark, text, _) in self.elements:
            print('{} - {}'.format(mark, text))

    def run(self, prompt='выберите команду: ', pause=False):
        self.clrscr()
        while True:
            self.print()
            user_choice = input(prompt)
            for (mark, _, rummethod) in self.elements:
                if user_choice.lower() == mark.lower():
                    if rummethod == -1:
                        return True
                    # self.clrscr()
                    rummethod()
                    if pause:
                        input("Ввод для продолжения...")
                        self.clrscr()
                    break

    def __len__(self):  # размер меню
        return len(self.elements)

    def clrscr(self):
        system('cls')
