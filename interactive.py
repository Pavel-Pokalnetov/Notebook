def add_note(controler):
    title = input('Заголовок: ')
    if title=='' :return
    text = input('Текст заметки')
    if text == '':return
    controler.add(title,text)
    return


def del_note(controler):
    return None


def search_notes(controler):
    text = input('Строка поиска:')
    return None


def export_notes(controler):
    return None


def import_notes(controler):
    return None