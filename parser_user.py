import json
import os
import requests
from auth_data import token
import vk_api

def get_wall_posts(check_id):
    req_id = check_id[2:]

    url = f"https://api.vk.com/method/users.get?user_ids={check_id}&fields=photo_id,verified,sex,bdate,city,country,home_town,has_photo,online,domain,has_mobile,contacts,site,education,universities,schools,status,last_seen,followers_count,common_count,occupation,nickname,relatives,relation,personal,connections,exports,activities,interests,music,movies,tv,books,games,about,quotes,timezone,screen_name,maiden_name,photo_max_orig,is_friend,friend_status,career,military,blacklisted,blacklisted_by_me,can_be_invited_group&access_token={token}&v=5.126&"
    req = requests.get(url)
    src = req.json()
    
    with open(f"{check_id}.json","w",encoding="utf-8") as file:
        json.dump(src,file,indent=4,ensure_ascii=False)

    url1 = f"https://api.vk.com/method/groups.get?user_id={req_id}&extended=1&count=1000&access_token={token}&v=5.126&"
    req1 = requests.get(url1)
    src1 = req1.json()

    with open(f"{check_id}_groups.json","w",encoding="utf-8") as file:
        json.dump(src1,file,indent=4,ensure_ascii=False)

    url2 = f"https://api.vk.com/method/friends.get?user_id={req_id}&order=name&name_case=nom&fields=nickname,sex,bdate,city,country,timezone,photo_200_orig,has_mobile,contacts,education,online,relation,last_seen,universities&access_token={token}&v=5.126&"
    req2 = requests.get(url2)
    src2 = req2.json()

    with open(f"{check_id}_friends.json","w",encoding="utf-8") as file:
        json.dump(src2,file,indent=4,ensure_ascii=False)

def main():
    human = input("Введите id человека: ")
    get_wall_posts(human)


if __name__ == '__main__':
    main()