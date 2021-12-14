import os, shutil, img2pdf
from os.path import normpath
from colorama import init as colorInit, Style, Fore, Back

colorInit()

print(Style.BRIGHT + Fore.CYAN + 'MangaCreatorPDF v1.4.2-beta\nFor files with Mangal1b\n' + Style.RESET_ALL)

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
        return normpath(data)

def askPart():
    print('\nВведи c какого тома начинать делать мангу в PDF:')
    try:
        data = int(input())
        return data
    except ValueError:
        print(Fore.RED + 'Введено не корректное значение. Пустота и буквы не проходят. \nПовтори ещё раз...\n' + Fore.RESET)
        return askPart()  

def askDeletedImages(dirs):
    user_answer = input('\nУдалить отсортированные страницы манги? [Y/n]: ')
    if user_answer in ['Y', 'y', 'Д', 'д']:
        for item in dirs:
            shutil.rmtree(item, ignore_errors=True)
        print(Back.RED + Fore.BLACK + 'Удалено!' + Style.RESET_ALL)
    elif user_answer in ['N', 'n', 'Н', 'н']:
        print('\nОтсортированные страницы и PDF файлы находяться по этому пути:\n"{}".\n'.format(Style.BRIGHT + Fore.YELLOW + os.getcwd() + Style.RESET_ALL))
    else:
        print('\nВведён не корректный ответ. Повтори ещё раз... ')
        askDeletedImages(dirs)
        
def createDir(name):
    try: 
        os.mkdir(name)
    except FileExistsError:
        pass

# Counters
count_part, count_pages, count_del_png = 0, 0, 0

os.chdir(askDir())
list_dirs = [i for i in os.listdir() if os.path.isdir(i) and 'Глава' in i]
list_dirs.sort(key=lambda x: int(x.split()[x.split().index('Том')+1]))
list_dirs.sort(key=lambda x: float(x.split()[x.split().index('Глава')+1]))

name_title = os.path.basename(os.getcwd())
createDir(name_title)
os.chdir(name_title)

for item in list_dirs:
    current_part = item.split()[item.split().index('Том')+1]
    partDir = name_title + ' Том ' + current_part
    files = sorted(os.listdir('../' + item), key=lambda x: int(x.split('.')[0]))
    
    if int(current_part) > count_part:
        createDir(normpath(partDir))
        next_page = 0 
        count_part = int(current_part)
    
    for page in files:
        new_name_file = str(next_page) + '.' + page.split('.')[1]
        count_pages += 1                                            # Counter for statistic

        if not page.endswith(".png"):                               # Move images
            os.replace(normpath('../' + item + '/' + page), normpath(partDir + '/' + new_name_file))
        else:                                                       # DELETE PNG
            os.remove(normpath('../' + item + '/' + page))
            count_del_png += 1                                      # Counter for statistic
        next_page += 1
    
    os.rmdir('../' + item)

print('\nВыполнена сортировка страниц и удалены ненужные папки.\n')

# # # # # # # # # 
# CREATING PDF  # 
# # # # # # # # # 

list_dirs = [i for i in os.listdir() if os.path.isdir(i) and 'Том' in i]
list_dirs.sort(key=lambda x: int(x.split()[x.split().index('Том')+1]))

for item in list_dirs:
    files = sorted(os.listdir(item), key=lambda x: int(x.split('.')[0]))
    with open(item+".pdf", "wb") as page:
        page.write(img2pdf.convert([normpath(item+'/'+i) for i in files]))
    print('Создан файл "' + item + '.pdf"')

askDeletedImages(list_dirs)

print('\n' + Back.GREEN + Fore.BLACK + 'Конвертирование манги в PDF завершено' + Style.RESET_ALL)
print('Всего обработано {} тома(-ов) и {} страниц(-ы) из которых удалено {} PNG файла(-ов)'.format(count_part, count_pages, count_del_png))
input('\nДля завершения программы, нажмите Enter...')