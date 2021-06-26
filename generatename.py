year = []
papername = []
author = []
mentor = []

with open('filenames.txt', 'r') as f:
    for i in f.readlines():
        i = i.split('.')[0]
        year.append(i.split('_')[0])
        papername.append(i.split('_')[1])
        author.append(i.split('_')[2])
        mentor.append(i.split('_')[3])

with open('year.txt', 'w+') as f:
    for i in year:
        f.write(i)
        f.write('\n')

with open('papername.txt', 'w+') as f:
    for i in papername:
        f.write(i)
        f.write('\n')

with open('author.txt', 'w+') as f:
    for i in author:
        f.write(i)
        f.write('\n')

with open('mentor.txt', 'w+') as f:
    for i in mentor:
        f.write(i)
        f.write('\n')


print(year)
print(papername)
print(author)
print(mentor)