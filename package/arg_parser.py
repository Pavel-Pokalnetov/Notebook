import argparse

def argParser():
    pars = argparse.ArgumentParser(prog='NOTES', add_help=False,exit_on_error=False,)
    group = pars.add_mutually_exclusive_group(required=False)
    group.add_argument("-a", "--add", action='store_true', help="добавление заметок", )
    group.add_argument("-d", "--delete", action='store_true', help="удаление заметок")
    group.add_argument("-v", "--search_notes", action='store_true', help="просмотр или поиск заметок")
    group.add_argument("-e", "--exp", nargs=1, default='-', choices=["csv", "json"],
                       help="Экспорт в CSV или JSON")
    group.add_argument("-i", "--imp", nargs=1, default='-', choices=["csv", "json"],
                       help="Импорт из CSV или JSON")
    group.add_argument("-h","--help",action='store_true', help="справка о программе")
    pars.add_argument("--title", nargs="*", default="", help="заголовок заметки")
    pars.add_argument("--text", nargs="*", default="", help="текст заметки или строка поиска")
    pars.add_argument("--date", nargs="*", default="", help="дата в формате YYYY-MM-DD")
    
    pars.add_argument("--id", nargs="?", default="", help="идентификатор заметки")
    pars.add_argument("--filename", nargs=1, default="", help="имя файла") 

    return pars
