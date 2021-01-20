import requests, json
import networkx as nx

token = ""


def get_friends_ids(us):
    friends = 'https://api.vk.com/method/friends.get'
    params = {
        'user_id': us,
        'access_token': token,
        'v': 5.126,
        'timeout': 50
    }
    res = requests.get(friends, params=params).json()
    if 'error' not in res:
        return (res['response']['items'])
    else:
        return ''


def get_members(gr):
    group = 'https://api.vk.com/method/groups.getMembers'
    params = {
        'group_id': gr,
        'access_token': token,
        'v': 5.126,
        'timeout': 50
    }
    res = requests.get(group, params=params).json()
    data = res['response']['items']
    count = res['response']['count'] // 1000

    for i in range(1, count + 1):
        group = 'https://api.vk.com/method/groups.getMembers'
        params = {
            'group_id': gr,
            'access_token': token,
            'v': 5.126,
            'timeout': 50,
            'offset': i * 1000
        }
        res = requests.get(group, params=params).json()
        data += res['response']['items']
    return data 


""" pub = input("Введите id/краткое имя группы: ")
members = get_members(pub)
length = len(members) """
graph = {}
id = input("Введите id человека: ")

friends_ids = get_friends_ids(id)
for friend_id in friends_ids:
    print('Processing id: ', friend_id)
    graph[friend_id] = get_friends_ids(friend_id)
    with open(f"{id}.json","w",encoding="utf-8") as file:
        json.dump(graph,file,indent=4,ensure_ascii=False)


""" for i in range(0,length):
    friends_ids = get_friends_ids(members[i])
    for friend_id in friends_ids:
        print('Processing id: ', friend_id)
        graph[friend_id] = get_friends_ids(friend_id)
        with open(f"{pub}.json","w",encoding="utf-8") as file:
            json.dump(graph,file,indent=4,ensure_ascii=False) """

with open('gachi_thread.json', 'r', encoding='utf-8') as f: #открыли файл с данными
    graph = json.load(f)
#graph = json.load('gachi_thread.json')

g = nx.Graph()

for i in graph:
    g.add_node(i)
    for j in graph[i]:
        #if i != j and i in graph and j in graph:
        g.add_edge(i, j)

nx.write_graphml(g, 'asd.graphml')
