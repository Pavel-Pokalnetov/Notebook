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

    def print(self):
        for (mark, text, _) in self.elements:
            print('{} - {}'.format(mark, text))

    def run(self, prompt='выберите команду: '):
        def clrscr(): return system('cls')
        while (True):
            clrscr()
            self.print()
            user_choice = input(prompt)
            for (mark, _, rummethod) in self.elements:
                if user_choice == mark:
                    if rummethod == -1:
                        return True 
                    clrscr()
                    rummethod()
                    break


    def __len__(self):  # размер меню
        return len(self.elements)


