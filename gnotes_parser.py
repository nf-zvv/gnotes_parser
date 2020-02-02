import os
import html2text
import shutil
from bs4 import BeautifulSoup
from datetime import datetime


# Имя директории, в которой лежат файлы GNotes
GNotes_folder = 'GNotes'

# Имя новой директории, к которую будут сохранены результаты
GNotes_import = 'GNotes_import'

# Формат даты и времени для указания в новом файле
date_time_format = '%d.%m.%Y %H:%M'

# Расширение новых файлов
file_ext =  '.md'

h = html2text.HTML2Text()
h.unicode_snob = True
h.body_width = False
h.unifiable = True
h.ignore_emphasis = True
h.single_line_break = True

# Полный путь к директории, в которой находимся
BASE_DIR = os.path.dirname(os.path.realpath(__file__))

# Полный путь к директории, в которой находятся файлы GNotes
path = os.path.join(BASE_DIR, GNotes_folder)

# Полный путь к директории, в которой будут сохранены результаты
new_path = os.path.join(BASE_DIR, GNotes_import)

if not os.path.exists(new_path): os.makedirs(new_path)

if os.path.exists(path) and os.path.isdir(path):
    files = os.listdir(path)
    for name in files:
        if os.path.isdir(os.path.join(path, name)) and name[0] != '.':
            if not os.path.exists(os.path.join(new_path, name)): os.makedirs(os.path.join(new_path, name))
            print(name)
            tree = os.walk(os.path.join(path, name))
            for i in tree:
                if 'content.html' in i[-1]:
                    f = open(os.path.join(i[0], 'content.html'), 'r', encoding='UTF-8')
                    html = f.read()
                    parsed_html = BeautifulSoup(html, 'html.parser')
                    title = h.handle(str(parsed_html.body.find('h4', attrs={'class':'text_overflow'})))
                    create_modify_time = h.handle(str(parsed_html.body.find('p', attrs={'class':'create_time'})))
                    note_content = h.handle(str(parsed_html.body.find('p', attrs={'class':'note_content'})))
                    image = parsed_html.body.find('img', attrs={'class':'image'})
                    # Разбиваем строку
                    datetime_str = create_modify_time.split()
                    # Извлекаем из строки подстроки с датой и временем создания файла, формируем в формате %m/%d/%Y %H:%M
                    create_date_time = ''.join([datetime_str[2], ' ', datetime_str[3]])
                    create_date_time = datetime.strptime(create_date_time, '%m/%d/%Y %H:%M')  # '2/4/2016 16:02'
                    # Извлекаем из строки подстроки с датой и временем создания файла
                    modify_date_time = ''.join([datetime_str[6], ' ', datetime_str[7]])
                    modify_date_time = datetime.strptime(modify_date_time, '%m/%d/%Y %H:%M')
                    # Имя файла в формате 20160204_16_02.md
                    new_filename = create_date_time.strftime('%Y%m%d_%H_%M')
                    # На случай, если существуют несколько заметок, сделанных в одно время
                    ver = 0
                    ver_str = ''
                    while os.path.exists(os.path.join(new_path, name, new_filename + ver_str + file_ext)):
                        ver += 1
                        ver_str = '(' + str(ver) + ')'
                    f2 = open(os.path.join(new_path, name, new_filename + ver_str + file_ext), 'w', encoding='UTF-8')
                    # Ограничиваем заголовок заметки 49-ю символами
                    if len(title) > 50: title = title[0:50] + '...'
                    # Заполняем новый файл
                    f2.write(title)
                    f2.write('\n')
                    f2.write(note_content)
                    f2.write('\n')
                    f2.write('*[create-date]: ' + create_date_time.strftime(date_time_format) + '  \n')
                    f2.write('*[modify-date]: ' + modify_date_time.strftime(date_time_format) + '  \n')
                    f2.write('*[note-tags]: ' + '  \n')
                    f2.write('*[author]: ' + '  \n')
                    f2.write('*[comment]: ' + 'Imported from GNotes' + '  \n')
                    if image is not None:
                        if not os.path.exists(os.path.join(new_path, name, 'media')): os.makedirs(os.path.join(new_path, name, 'media'))
                        img_name = str(image['src'])
                        f2.write('*[attachment]: ' + 'media/' + img_name + '  \n')
                        shutil.copyfile(os.path.join(i[0], img_name), os.path.join(new_path, name, 'media', img_name))
                    f2.close
                    print('\t' + new_filename + ver_str)
                    f.close()
            
            