file = open("OriginalData/u.item", "r", encoding="ISO_8859_15")

movies = []

for line in file:
    parts = line.split('|')
    name = parts[1]
    year = name[-7:]
    name = name[:-7]
    if name[-5:] == ', The':
        name = 'The ' + name[:-5]
    parts[1] = name + year
    movies.append('|'.join(parts))

if not file.closed:
    file.close()

file = open("OriginalData/u.item", "w")

for line in movies:
    file.write(str(line))

if not file.closed:
    file.close()