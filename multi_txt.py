import glob
from txt import write_file

path = './more_txt/*.txt'
FOLDER = 'more_txt'

content = ''
for f in glob.glob(path):
    with open(f, 'r', encoding='utf-8') as f:
        content += f.read() + '\n'

print(content)

write_file(content, FOLDER)



        


