import glob
from txt import ask_for_direction

path = './more_txt/*.txt'
FOLDER = 'more_txt'

content = ''
for f in glob.glob(path):
    with open(f, 'r', encoding='utf-8') as f:
        content += f.read() + '\n'

print(content)

ask_for_direction(content, FOLDER)



        


