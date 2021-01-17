import requests, time, json, csv
import pandas as pd
from auth_data import token

pub = input("Введите id/краткое имя группы: ")

info = 'https://api.vk.com/method/groups.getMembers'
params = {
        'group_id': pub,
        'access_token': token,
        'v': 5.126
    }
i = requests.get(info, params = params).json()

real_count = i['response']['count']
print('Количество подписчиков данной группы: ' + str(real_count))

count_users = 10000
offset = 0
count = 1000
data_users = []
info = []

while offset < count_users:

    url = 'https://api.vk.com/method/groups.getMembers'
    params = {
        'group_id': pub,
        'count': count,
        'offset': offset,
        'access_token': token,
        'v': 5.126
    }

    r = requests.get(url, params = params).json()
    
    check = True
    if check:
        real_count = r['response']['count']
        if real_count < count_users:
            count_users = real_count
            check = False
    else:
            check = False
    
    data_users += r['response']['items']
    offset += count    
    with open(f"{pub}.json","w",encoding="utf-8") as file:
        json.dump(data_users,file,indent=4,ensure_ascii=False)

offset = 0
step = 1

while offset < real_count:

    result = 'https://api.vk.com/method/users.get'
    params = {
        'user_ids': data_users[0+offset:offset+step],
        'fields': 'photo_id,verified,sex,bdate,city,country,home_town,has_photo,online,domain,has_mobile,contacts,site,education,universities,schools,status,last_seen,followers_count,common_count,occupation,nickname,relatives,relation,personal,connections,exports,activities,interests,music,movies,tv,books,games,about,quotes,timezone,screen_name,maiden_name,photo_max_orig,is_friend,friend_status,career,military',
        'access_token': token,
        'v': 5.126,
        'timeout': 10
    }

    o = requests.get(result, params = params).json()

    info += o['response']
    offset += step
    with open(f"{pub}_info.json","w",encoding="utf-8") as file:
        json.dump(info,file,indent=4,ensure_ascii=False) 
    
    print(str(offset/real_count) + '% выполнено: получены данные ' + str(offset) + ' из ' + str(real_count) + ' пользователей')


##Конвертация данных в txt и далее в таблицы csv##
""" with open(f'{pub}.txt', 'w') as file:
    for item in data_users:
        file.write(str(item)+"\n")

""" 
""" pfile = input("Выберите файл, с которого необходимо считать данные: ")
with open(f'{pfile}.json', 'r') as read:
    stripped = (line.strip() for line in read)
    lines = (line.split(',') for line in stripped if line)
    with open(f'{pfile}.csv', 'w') as output:
        writer = csv.writer(output)
        writer.writerow(('id','info'))
        writer.writerows(lines)  """

