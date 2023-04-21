# Notebook

## Записная книжка на python

Работа с заметками в командной строке CLI через параметры командной строки или в интерактивном режиме. Используется кодировка UTF8. Локальное хранение данных в базе sqlite

---
### Запуск 
    python notes.py [COMMAND OPTION]   
COMMAND - команды    
OPTION - опции команд
- -a,--add --title TITLE --text TEXT - добавить заметку  
    --title TITLE - заголовок заметки  
    --text TEXT - закст заметки  
     
- -d,--delete  - удаление заметок  
   --id ID - удаление по ID  
   --text TEXT - удаление по TEXT  
   без опций - удаление всех заметок

- -v,--search_notes - поиск заметок  
    --id ID - поиск по ID  
    --text TEXT - поиск по TEXT  
    без опций - вывод всех записей

- -e csv --filename FILENAME - экспорт в CSV
- -e json --filename FILENAME - экспорт в JSON

- -i csv --filename FILENAME - импорт из CSV
- -i json -- filename FILENAME - импорт из JSON

- -h,--help - вывод справки  

TITLE,TEXT - одно или несколько слов в кодировке UTF8,  
FILENAME - имя файла, обязательно заключить в кавычки  
ID - внутренний идентификатор заметки
если в имени файла или тексте есть пробелы то оборачиваем в кавычки

Запуск __python notes.py__ без аргументов - интерактивный режим

Пример:
    - notes -a --title "На пятницу" --text "Поменять заголовки проекта. Залить на тестсервер"  
    ;добавление заметки с заголовком и текстом  

    - notes -v  
    ;показ всех заметок  

    - notes -d --text "тестсервер"  
    ;удаление заметки с текстом __тестсервер__  

    - notes -i csv --filename '~\myNotes'  
    ;импорт заметок из файла '~\myNotes'  

Запуск __python notes.py__ без аргументов - интерактивный режим

### Коды возврата
    0 - успешное завершение  
    1 - ошибка в параметрах командной строки

### Зависимости

texttable - https://pypi.org/project/texttable/


### Установка
рекомендуется работа с виртуальным окружением  

    python -m venv venv  
    venv\Scripts\activate.bat  
    pip install texttable  
