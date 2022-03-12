import os, shutil, img2pdf, zipfile
from os.path import normpath
from colorama import init as colorInit, Style, Fore, Back
from PIL import Image

colorInit()

print(Style.BRIGHT + Fore.CYAN + 'MangaCreatorPDF v1.5.3\nFor files with Mangalib.me' + Style.RESET_ALL)

def askDir():
    print('\nEnter the directory path:')
    data = input()
    if not data:
        print(Fore.RED + 'You cannot enter a void. Say it again...\n' + Fore.RESET)
        return askDir()
    elif not os.path.isdir(data):
        print(Fore.RED + 'This folder was not found. Check and repeat...\n' + Fore.RESET)
        return askDir()
    else:
        return normpath(data)

def askDeletedImages(dirs):
    user_answer = input('\nDelete sorted manga pages? [Y/n]: ')
    if user_answer in ['Y', 'y', 'Д', 'д']:
        for item in dirs:
            shutil.rmtree(item, ignore_errors=True)
        print(Back.RED + Fore.BLACK + 'Removed!' + Style.RESET_ALL)
    elif user_answer in ['N', 'n', 'Н', 'н']:
        return
    else:
        print(Fore.RED + '\nIncorrect answer entered. Say it again... ' + Fore.RESET)
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
            print('\n' + Back.RED + Fore.BLACK + 'Warning!' + Style.RESET_ALL)
            print('When unpacking the manga, pages of too high quality were found,')
            print('so during this task, each page of a large size will be compressed.\nThis may take a long time!\n')
            warning = False
        
        quality_procentage = int(to_kb*1024 / file_size * 100)
        with Image.open(path) as img:
            img.save(path, path.split('.')[-1], quality=quality_procentage)

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
    
    statistic[name_title] = {'parts' : 0, 'pages' : 0, 'mismatched files' : 0, 'warning' : True}

    # START EXTRACT

    print('\nUnpacking archives:')
    
    for item in list_zip:
        with zipfile.ZipFile('../' + item) as zf:
            current_part = item.split()[item.split().index('Том')+1]
            partDir = name_title + ' Том ' + current_part
            
            if int(current_part) > statistic[name_title]['parts']:
                print(f'{current_part}st part...')
                
                createDir(normpath(partDir))
                num_page = 0 
                statistic[name_title]['parts'] = int(current_part)
            
            for page in zf.infolist():
                new_name = f'Page.{num_page}.{page.filename.split(".")[1]}'
                statistic[name_title]['pages'] += 1

                if page.filename.endswith(('jpeg', 'jpg', 'gif', 'tiff')):                      # Extract images
                    zf.extract(page.filename, partDir)
                    os.replace(normpath(partDir+'/'+page.filename), normpath(partDir+'/'+new_name))
                    statistic[name_title]['warning'] = checkImage(normpath(partDir+'/'+new_name), warning=statistic[name_title]['warning'])
                else:
                    statistic[name_title]['mismatched files'] += 1
                    continue
                num_page += 1

    # END EXTRACT

    print('\nThe pages are sorted.\n\nConvert to PDF...')

    list_dirs = [i for i in os.listdir() if os.path.isdir(i) and 'Том' in i]
    list_dirs.sort(key=lambda x: int(x.split()[x.split().index('Том')+1]))

    for item in list_dirs:
        files = sorted(os.listdir(item), key=lambda x: int(x.split('.')[1]))
        with open(item+".pdf", "wb") as page:
            page.write(img2pdf.convert([normpath(item+'/'+i) for i in files]))
        print('File created "' + item + '.pdf"')

    askDeletedImages(list_dirs)

    print('\n' + Back.GREEN + Fore.BLACK + f'Convert Manga "{name_title}" to PDF - Completed' + Style.RESET_ALL)

    print('\nThe generated files are in this path:\n"{}".'.format(Style.BRIGHT + Fore.YELLOW + os.getcwd() + Style.RESET_ALL))
    
    while True:
        user_answer = input('\nShall we convert some more manga? [Y/n]: ')

        if user_answer in ['Y', 'y', 'Д', 'д']:
            print('\n'.ljust(30, '='))
            break
        elif user_answer in ['N', 'n', 'Н', 'н']:
            repeat = False
            
            print(Fore.YELLOW + '\nStatistics:')
            for title, values in statistic.items():
                print(f'"{title}" '.ljust(55, '.') + f' Parts: {values["parts"]} | Pages: {values["pages"]} | Mismatched files: {values["mismatched files"]}')
            print(Style.RESET_ALL, end='')
            
            break
        else:
            print(Fore.RED + '\nIncorrect answer entered. Say it again... ' + Fore.RESET)

input('\nTo end the program, press Enter...')