import requests
import time
import json
from auth_data import token

def get_groupsUsers(gr_id):
  
    count_users = 10000
    offset = 0
    count = 1000
    data_users = []
    i = 1
    
    while offset < count_users:

        url = 'https://api.vk.com/method/groups.getMembers'
        params = {
            'group_id': gr_id,
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
        time.sleep(3)
        with open(f"{gr_id}.json","w",encoding="utf-8") as file:
            json.dump(data_users,file,indent=4,ensure_ascii=False)
        print(str(i) +' итерация пройдена')
        i = i + 1     


def main():
    pub = input("Введите id/краткое имя группы: ")
    get_groupsUsers(pub)


if __name__ == '__main__':
    main()