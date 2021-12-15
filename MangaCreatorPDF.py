import os, shutil, img2pdf
from os.path import normpath
from colorama import init as colorInit, Style, Fore, Back

colorInit()

print(Style.BRIGHT + Fore.CYAN + 'MangaCreatorPDF v1.4.3-beta\nFor files with Mangal1b' + Style.RESET_ALL)

def askDir():
    print('\nВведи путь к каталогу:')
    data = input()
    if not data:
        print(Fore.RED + 'Нельзя вводить пустоту. Повтори ещё раз...\n' + Fore.RESET)
        return askDir()
    elif not os.path.isdir(data):
        print(Fore.RED + 'Эта папка не найдена. Проверь и повтори ещё раз...\n' + Fore.RESET)
        return askDir()
    else:
        return normpath(data)

def askDeletedImages(dirs):
    user_answer = input('\nУдалить отсортированные страницы манги? [Y/n]: ')
    if user_answer in ['Y', 'y', 'Д', 'д']:
        for item in dirs:
            shutil.rmtree(item, ignore_errors=True)
        print(Back.RED + Fore.BLACK + 'Удалено!' + Style.RESET_ALL)
    elif user_answer in ['N', 'n', 'Н', 'н']:
        print('\nОтсортированные страницы и PDF файлы находятся по этому пути:\n"{}".\n'.format(Style.BRIGHT + Fore.YELLOW + os.getcwd() + Style.RESET_ALL))
    else:
        print(Fore.RED + '\nВведён не корректный ответ. Повтори ещё раз... ' + Fore.RESET)
        askDeletedImages(dirs)

def createDir(name):
    try: 
        os.mkdir(name)
    except FileExistsError:
        pass

statistic = {}
repeat = True

while repeat:
    os.chdir(askDir())
    list_dirs = [i for i in os.listdir() if os.path.isdir(i) and 'Глава' in i]
    list_dirs.sort(key=lambda x: int(x.split()[x.split().index('Том')+1]))
    list_dirs.sort(key=lambda x: float(x.split()[x.split().index('Глава')+1]))

    name_title = os.path.basename(os.getcwd())
    createDir(name_title)
    os.chdir(name_title)
    
    statistic[name_title] = {'parts' : 0, 'pages' : 0, 'png' : 0}

    for item in list_dirs:
        current_part = item.split()[item.split().index('Том')+1]
        partDir = name_title + ' Том ' + current_part
        files = sorted(os.listdir('../' + item), key=lambda x: int(x.split('.')[0]))
        
        if int(current_part) > statistic[name_title]['parts']:
            createDir(normpath(partDir))
            num_page = 0 
            statistic[name_title]['parts'] = int(current_part)
        
        for page in files:
            new_name_file = str(num_page) + '.' + page.split('.')[1]
            statistic[name_title]['pages'] += 1

            if not page.endswith(".png"):                               # Move images
                os.replace(normpath('../' + item + '/' + page), normpath(partDir + '/' + new_name_file))
            else:                                                       # DELETE PNG
                os.remove(normpath('../' + item + '/' + page))
                statistic[name_title]['png'] += 1
            num_page += 1
        
        os.rmdir('../' + item)

    print('\nВыполнена сортировка страниц и удалены ненужные папки.\n')

    print('Конвертация в PDF...')

    list_dirs = [i for i in os.listdir() if os.path.isdir(i) and 'Том' in i]
    list_dirs.sort(key=lambda x: int(x.split()[x.split().index('Том')+1]))

    for item in list_dirs:
        files = sorted(os.listdir(item), key=lambda x: int(x.split('.')[0]))
        with open(item+".pdf", "wb") as page:
            page.write(img2pdf.convert([normpath(item+'/'+i) for i in files]))
        print('Создан файл "' + item + '.pdf"')

    askDeletedImages(list_dirs)

    print('\n' + Back.GREEN + Fore.BLACK + 'Конвертирование "{}" в PDF - завершено'.format(name_title) + Style.RESET_ALL)
    
    while True:
        user_answer = input('\nБудем ещё какую-то мангу конвертировать? [Y/n]: ')

        if user_answer in ['Y', 'y', 'Д', 'д']:
            print('\n'.ljust(30, '='))
            break
        elif user_answer in ['N', 'n', 'Н', 'н']:
            repeat = False
            
            print(Fore.YELLOW + '\nСтатистика:')
            for title, values in statistic.items():
                print(str('"'+title+'" ').ljust(45, '.') + ' Томов: {} | Страниц: {} | Удалено PNG: {}'.format(values['parts'], values['pages'], values['png']))
            break
        else:
            print(Fore.RED + '\nВведён не корректный ответ. Повтори ещё раз... ' + Fore.RESET)

input(Style.RESET_ALL + '\nДля завершения программы, нажмите Enter...')