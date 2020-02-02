# Скрипт на Python для преобразования GNotes Backup в Markdown

С некоторых пор приложение для ведения заметок GNotes стало платным, при отсутствии каких-либо значительных улучшений. Было решено мигрировать с этого приложения. Но для этого потребовалось экспортировать заметки, благо для этого есть функция экспорта в настройках GNotes.

GNotes сохраняет бэкап в формате HTML. Это удобно для просмотра архива GNotes в браузере, но не годится для дальнейшего использования заметок. Поэтому был написан скрипт на языке Python для преобразования заметок в простой текстовый формат с разметкой Markdown, который в дальнейшем можно использовать как угодно. На самом деле от разметки Markdown в преобразованных файлах это только обозначение заголовка 4-го уровня и расширение файла. Также добавлена некоторая метаинформация в виде дат создания и модификации заметки, взятая из исходного бэкапа GNotes.

## Возможности

- Сохраняется исходная структура блокнотов GNotes
- Каждая заметка сохраняется в отдельный Markdown файл с именем в виде даты и времени создания заметки
- Кодировка заметок UTF-8
- Если в одну и ту же минуту было создано несколько заметок, то к имени файла добавляется индекс (1), (2), ...
- К каждой заметке добавляется метаинформация в виде дат создания и модификации заметки
- При наличии прикрепленной к заметке фотографии она помещается в директорию `media` текущего блокнота

## Использование

Поместить скрипт в диреткорию рядом с директорией GNotes, содержащей поддиректории блокнотов.

Выполнить 

```
python gnotes_parser.py
```

## Исходный формат GNotes Backup

Директория GNotes Backup представляет собой набор поддиректорий в соответствии с именами блокнотов GNotes.

Каджая директория блокнота содержит набор поддиректорий с именами типа `b26362b7-e9fc-42f5-9c50-76144883b696` или `59b91b89cb3bfc6a51c85ef2`, в которых располагаются файлы с именем `content.html`. Иными словами, каждый такой файл представляет собой заметку в формате HTML. Если у заметки есть вложения, то они также располагаются в этой же диреткории.

Заметки не относящиеся ни к одному блокноту располагаются в директории `Other`.

Типовая структура диреткорий приведена ниже.

```
GNotes
+--.src
|  +--...
|  +--...
+--edu
|  +--b26362b7-e9fc-42f5-9c50-76144883b696
|  |  +--.nomedia
|  |  +--content.html
|  +--59b91b89cb3bfc6a51c85ef2
|  |  +--.nomedia
|  |  +--content.html
|  |  +--picture.jpg
|  +--...
|  +--...
+--Other
|  +--5a2047e65cc442fd9b222c63
|  |  +--.nomedia
|  |  +--content.html
|  +--57c532ee74ca0a7bd854f38e
|  |  +--.nomedia
|  |  +--content.html
|  +--...
|  +--...
+--Work
|  +--5f6ad32b-84ef-4cc6-9957-d809efc3cabe
|  |  +--.nomedia
|  |  +--content.html
|  |  +--picture.jpg
|  +--7867620d-7086-49e2-b776-d189030c5ff5
|  |  +--.nomedia
|  |  +--content.html
|  |  +--image.jpg
|  +--...
|  +--...
+--...
|
```

## Выходной формат Markdown

### Заголовок

Первой строкой идет заголовок 4-го уровня (выделенный символами ####). 

GNotes использует в качестве заголовка первую строку или первое предложение, если нет отдельной выделенной строки с заголовком.

В случае если нет отдельной выделенной строки с заголовком, то длина заголовка ограничивается 50-ю символами.

### Контент

Содержимое заметки вставляется в неизменном виде.

### Метаинформация

В конец заметки добавляется несколько строк с метаинформацией, такой как даты создания и модификации заметки, теги заметки, автор и комментарий.

*[create-date]: 27.05.2014 22:40  
*[modify-date]: 27.05.2014 22:40  
*[note-tags]:   
*[author]:   
*[comment]: Imported from GNotes  

## Системные треования

Работа скрипта проверлась при следующих условиях:

- Python         3.8.1
- beautifulsoup4 4.8.2
- bs4            0.0.1
- html2text      2020.1.16

ОС: Windows 10
