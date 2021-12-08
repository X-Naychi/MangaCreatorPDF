import os
import shutil
#import colorama

print('MangaCreatorPDF v1.1\n')

def createDir(name):
    try: 
        os.mkdir(name)
    except FileExistsError:
        print('Папка "{}" уже существует.'.format(name))

def deleteSortedPage(dirs):
    user_answer = input('\nУдалить отсортированные страницы манги? [Y/n]: ')
    if user_answer in ['Y', 'y', 'Д', 'д']:
        for item in dirs:
            shutil.rmtree(item, ignore_errors=True)
        print('Удалено.')
    elif user_answer in ['N', 'n', 'Н', 'н']:
        print('\nОтсортированные страницы и PDF файлы находяться по этому пути:\n"{}".\n'.format(os.getcwd()))
    else:
        print('\nВведён не корректный ответ. Повторите ещё раз... ')
        deleteSortedPage(dirs)
        

# variables
print('Введи путь к каталогу:')
use_dir = input()
name_title = use_dir.split('/')[-1]
part = 0
sum_pages = 0

# Running algorithm
os.chdir(use_dir)
list_dirs = os.listdir()
list_dirs.sort()

createDir(name_title)

for item in list_dirs:
    try:
        files = os.listdir(item)
    except NotADirectoryError:
        continue
        

    if name_title == item:
        continue
    elif 'Том ' + str(part) in item:
        len_files += len(files)
        sum_pages += len(files)

        i = 0
        while next_page <= len_files-1:
            try:                                    # EDIT!
                name_file = str(next_page) + '.jpeg'
                os.replace(item + '/' + str(i) + '.jpeg', name_title + '/' + partDir + '/' + name_file.zfill(10))
            except FileNotFoundError:
                if str(i)+'.png' in files:
                    name_file = str(next_page) + '.png'
                    os.replace(item + '/' + str(i) + '.png', name_title + '/' + partDir + '/' + name_file.zfill(9))
                else:
                    print('Файла "' + item+'/'+str(i)+'.png" - не существует!')
                    print('Аварийное завершение программы!')
                    exit() 
            next_page += 1
            i += 1
            if i == len(files):
                i = 0
            
    else:
        part += 1
        next_page = 0
        len_files = len(files)
        partDir = name_title + ' Том ' + str(part)

        createDir(name_title + '/' + partDir)
        
        for f in files:
            if not f.endswith(".png"):              # EDIT!
                os.replace(item + '/' + f, name_title + '/' + partDir + '/' + f.zfill(10))
            else:
                os.replace(item + '/' + f, name_title + '/' + partDir + '/' + f.zfill(9))
            next_page += 1

    os.rmdir(item)

print('Выполнена сортировка страниц и удалены ненужные папки.\n')
    
import img2pdf

os.chdir(name_title)
list_dirs = os.listdir()
list_dirs.sort()

for item in list_dirs:
    try:
        files = os.listdir(item)
        files.sort()
    except NotADirectoryError:
        continue

    with open(item+".pdf", "wb") as f:
        f.write(img2pdf.convert([item+'/'+i for i in files]))
    print('Создан файл "' + item+ '.pdf"')

deleteSortedPage(list_dirs)

print('\nКонвертирование манги в PDF завершено.')
print('Всего обработано {} тома(-ов) и {} страниц(-ы).\n'.format(part, sum_pages))
input('Для завершения программы, нажмите Enter...')