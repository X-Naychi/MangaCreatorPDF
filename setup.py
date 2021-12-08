import os, shutil, img2pdf
from colorama import init as colorInit, Style, Fore, Back

colorInit()

print(Style.BRIGHT + Fore.CYAN + 'MangaCreatorPDF v1.2\nFor files with Mangal1b\n' + Style.RESET_ALL)

def askDir():
    print('Введи путь к каталогу:')
    data = input()
    if not data:
        print(Fore.RED + 'Нельзя вводить пустоту. Повтори ещё раз...\n' + Fore.RESET)
        return askDir()
    elif not os.path.isdir(data):
        print(Fore.RED + 'Эта папка не найдена. Проверь и повтори ещё раз...\n' + Fore.RESET)
        return askDir()
    else:
        return data

def askPart():
    print('\nВведи c какого тома начинать делать мангу в PDF:')
    try:
        data = int(input())
        return data
    except ValueError:
        print(Fore.RED + 'Введено не корректное значение. Пустота и буквы не проходят. \nПовтори ещё раз...\n' + Fore.RESET)
        return askPart()
        

def deleteSortedPage(dirs):
    user_answer = input('\nУдалить отсортированные страницы манги? [Y/n]: ')
    if user_answer in ['Y', 'y', 'Д', 'д']:
        for item in dirs:
            shutil.rmtree(item, ignore_errors=True)
        print(Back.RED + Fore.BLACK + 'Удалено!' + Style.RESET_ALL)
    elif user_answer in ['N', 'n', 'Н', 'н']:
        print('\nОтсортированные страницы и PDF файлы находяться по этому пути:\n"{}".\n'.format(Style.BRIGHT + Fore.YELLOW + os.getcwd() + Style.RESET_ALL))
    else:
        print('\nВведён не корректный ответ. Повтори ещё раз... ')
        deleteSortedPage(dirs)
        
def createDir(name):
    try: 
        os.mkdir(name)
    except FileExistsError:
        print('Папка "{}" уже существует.'.format(name))


# variables
use_dir = askDir()
name_title = use_dir.split('/')[-1]
part = askPart()-1
sum_pages = 0
count_del_png = 0

# # # # # # # # # # # # 
# Running algorithm # #
# # # # # # # # # # # # 

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
        sum_pages += len(files) # Counter for statistic

        i = 0 # Primordial num file
        while next_page <= len_files-1:
            try:                                # Move JPEG
                name_file = str(next_page) + '.jpeg'
                os.replace(item + '/' + str(i) + '.jpeg', name_title + '/' + partDir + '/' + name_file.zfill(10))
            except FileNotFoundError:
                if str(i)+'.png' in files:      # DELETE PNG
                    name_file = str(next_page) + '.png'
                    os.remove(item + '/' + str(i) + '.png')
                    count_del_png += 1
                else:                           # ERROR NOT FOUNT
                    print('Файла "' + item+'/'+str(i)+'.png" - не существует!')
                    print(Back.RED + Fore.BLACK + 'Аварийное завершение программы!' + Style.RESET_ALL)
                    exit() 
            next_page += 1 # New num file
            i += 1
            if i == len(files):
                i = 0
    else:
        part += 1
        next_page = 0  # New num file
        len_files = len(files)
        sum_pages += len(files) # Counter for statistic
        partDir = name_title + ' Том ' + str(part) # Name for new directory

        createDir(name_title + '/' + partDir)
        
        for f in files:
            if not f.endswith(".png"):              # Move JPEG
                os.replace(item + '/' + f, name_title + '/' + partDir + '/' + f.zfill(10))
            else:                                   # DELETE PNG
                os.remove(item + '/' + f)
                count_del_png += 1 # Counter for statistic
            next_page += 1

    os.rmdir(item)

print('\nВыполнена сортировка страниц и удалены ненужные папки.\n')

# # # # # # # # # 
# CREATING PDF  # 
# # # # # # # # # 

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

print('\n' + Back.GREEN + Fore.BLACK + 'Конвертирование манги в PDF завершено' + Style.RESET_ALL)
print('Всего обработано {} тома(-ов) и {} страниц(-ы) из которых удалено {} PNG файла(-ов)'.format(part, sum_pages, count_del_png))
input('\nДля завершения программы, нажмите Enter...')