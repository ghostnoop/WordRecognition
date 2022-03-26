import emoji

dic = {}
with open('files/emojies.csv', 'r', encoding='utf-8') as f:
    lines = f.read().strip().split('\n')
    for row in lines:
        a, b = row.split(';')
        dic[emoji.demojize(a).strip()] = b
print(dic)
