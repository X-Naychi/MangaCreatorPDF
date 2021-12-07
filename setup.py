import os
print('\n\n')

tome = 1
folder = []
list_titles = os.listdir('./titles')

# print('Введи путь к каталогу:')
# use_dir = input()
use_dir = 'titles'

os.chdir(use_dir)
print(*os.listdir())







# Вариант с walk()
# # listDir = os.walk('./titles')

# # for i in listDir:
# #     folder += [i]


# # for path, dir, files in folder:
    
# #     if 'Том '+ str(n) in path:
# #         print("\nЭто " + str(n) + '-й том!')
# #         n += 1
# #     for file in files:
# #         print(path+'/'+file)
