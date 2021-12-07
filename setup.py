import os
print('\n\n')

part = 0

def createDir(name):
    try: 
        os.mkdir(name)
    except FileExistsError:
        print('Папка "{}" уже существует.'.format(name))

# print('Введи путь к каталогу:')
# use_dir = input()
use_dir = 'titles/Kawaii Dake Janai Onnanoko'
name_title = use_dir.split('/')[-1]

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
        
        i = 0
        while next_page <= len_files-1:
            try:
                os.replace(item + '/' + str(i) + '.jpeg', name_title + '/' + partDir + '/' + str(next_page) + '.jpeg')
            except FileNotFoundError:
                if str(i)+'.png' in files:
                    os.replace(item + '/' + str(i) + '.png', name_title + '/' + partDir + '/' + str(next_page) + '.png')
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
            os.replace(item + '/' + f, name_title + '/' + partDir + '/' + f)
            next_page += 1
    
    os.rmdir(item)
    
    
