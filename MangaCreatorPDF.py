import os, shutil, img2pdf, zipfile
from os.path import normpath
from colorama import init as colorInit, Style, Fore, Back
from PIL import Image

colorInit()

print(Style.BRIGHT + Fore.CYAN + 'MangaCreatorPDF v1.5.1-beta\nFor files with Mangal1b' + Style.RESET_ALL)

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

def checkImage(path, to_kb = 420, warning = True):
    file_size = os.path.getsize(path)
    if file_size/1024 > 1024:
        if warning is not False:
            print('\n' + Back.RED + Fore.BLACK + 'Внимание!' + Style.RESET_ALL)
            print('При распаковке манги, были обнаружены страницы слишком высокого качества,')
            print('поэтому в процессе этой задачи, каждая страница большого размера будет сжиматься.\nЭто может занять длительное время!\n')
            warning = False
        
        quality_procentage = int(to_kb*1024 / file_size * 100)
        with Image.open(path) as img:
            img.save(path, "JPEG", quality=quality_procentage)
        if not path.endswith(".jpeg"):
            os.remove(path)

    return warning

statistic = {}
repeat = True

while repeat:
    os.chdir(askDir())
    list_zip = [i for i in os.listdir() if i.endswith(".zip") and 'Глава' in i]
    list_zip.sort(key=lambda x: int(x.split()[x.split().index('Том')+1]))
    list_zip.sort(key=lambda x: float(x.split()[x.split().index('Глава')+1]))

    name_title = os.path.basename(os.getcwd())
    createDir(name_title)
    os.chdir(name_title)
    
    statistic[name_title] = {'parts' : 0, 'pages' : 0, 'png' : 0, 'warning' : True}

    # START EXTRACT

    print('\nРаспаковка архивов...')
    
    for item in list_zip:
        with zipfile.ZipFile('../' + item) as zf:
            current_part = item.split()[item.split().index('Том')+1]
            partDir = name_title + ' Том ' + current_part
            
            if int(current_part) > statistic[name_title]['parts']:
                if statistic[name_title]["parts"] != 0:
                    print(f'Распакованы рахивы {statistic[name_title]["parts"]}-го тома')
                
                createDir(normpath(partDir))
                num_page = 0 
                statistic[name_title]['parts'] = int(current_part)
            
            for page in zf.infolist():
                new_name = f'Page.{num_page}.{page.filename.split(".")[1]}'
                statistic[name_title]['pages'] += 1

                if not page.filename.endswith(".png"):                      # Extract images
                    zf.extract(page.filename, partDir)
                    os.replace(normpath(partDir+'/'+page.filename), normpath(partDir+'/'+new_name))
                    statistic[name_title]['warning'] = checkImage(normpath(partDir+'/'+new_name), warning=statistic[name_title]['warning'])
                else:
                    statistic[name_title]['png'] += 1
                    continue
                num_page += 1

    # END EXTRACT

    print('\nСтраницы отсортированы.\n\nКонвертация в PDF...')

    list_dirs = [i for i in os.listdir() if os.path.isdir(i) and 'Том' in i]
    list_dirs.sort(key=lambda x: int(x.split()[x.split().index('Том')+1]))

    for item in list_dirs:
        files = sorted(os.listdir(item), key=lambda x: int(x.split('.')[1]))
        with open(item+".pdf", "wb") as page:
            page.write(img2pdf.convert([normpath(item+'/'+i) for i in files]))
        print('Создан файл "' + item + '.pdf"')

    askDeletedImages(list_dirs)

    print('\n' + Back.GREEN + Fore.BLACK + f'Конвертирование "{name_title}" в PDF - завершено' + Style.RESET_ALL)
    
    while True:
        user_answer = input('\nБудем ещё какую-то мангу конвертировать? [Y/n]: ')

        if user_answer in ['Y', 'y', 'Д', 'д']:
            print('\n'.ljust(30, '='))
            break
        elif user_answer in ['N', 'n', 'Н', 'н']:
            repeat = False
            
            print(Fore.YELLOW + '\nСтатистика:')
            for title, values in statistic.items():
                print(f'"{title}" '.ljust(55, '.') + f' Томов: {values["parts"]} | Страниц: {values["pages"]} | Удалено PNG: {values["png"]}')
            print(Style.RESET_ALL, end='')
            break
        else:
            print(Fore.RED + '\nВведён не корректный ответ. Повтори ещё раз... ' + Fore.RESET)

input('\nДля завершения программы, нажмите Enter...')