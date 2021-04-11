import requests, tqdm
import networkx as nx
import pandas as pd
import numpy as np
import seaborn as sns
import scipy
import matplotlib.pyplot as plt
from os import environ

def suppress_qt_warnings():
    environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    environ["QT_SCALE_FACTOR"] = "1"

token = 'a11c907635f66b99cd03b178adfd29be6cf0042bf4ed1b0929bc76e2bb9601d4f8210b3361d5e5c127f9c'

def GetPublicSubs(public_id):
    group = 'https://api.vk.com/method/groups.getMembers'
    params = {
        'group_id': public_id,
        'access_token': token,
        'v': 5.126,
        'timeout': 50
    }
    res = requests.get(group, params=params).json()
    data = res['response']['items']
    print('В данной группе ' + str(res['response']['count']) + ' пользователей')
    count = res['response']['count'] // 1000

    for i in range(1, count + 1):
        group = 'https://api.vk.com/method/groups.getMembers'
        params = {
            'group_id': public_id,
            'access_token': token,
            'v': 5.126,
            'timeout': 50,
            'offset': i * 1000
        }
        res = requests.get(group, params=params).json()
        data += res['response']['items']
    return data

def GetFriends(user_id):
    user = 'https://api.vk.com/method/friends.get'
    params = {
        'user_id': user_id,
        'access_token': token,
        'v': 5.126,
        'timeout': 50,
    }
    res = requests.get(user, params=params).json()
    if 'error' not in res:
        return (res['response']['items'])
    else:
        return ''

def GetUserInfo(user_ids):
    friends = 'https://api.vk.com/method/users.get'
    params = {
        'user_ids': user_ids,
        'access_token': token,
        'v': 5.21,
        'fields' : 'first_name, last_name, sex, city, education'
    }
    res = requests.get(friends, params=params).json()
    if 'error' not in res:
        return res['response']
    else:
        return ''

def GetSubsFriendsInfo(public_id):

    ids= GetPublicSubs(public_id)
    
    graph = {}
    deleted_friend_ids = []

    for friend_id in tqdm.tqdm(ids):
        try:
            graph[friend_id] = GetFriends(friend_id)
        except:
            deleted_friend_ids.append(friend_id)

    G = nx.Graph(directed=False)

    for i in graph:
        G.add_node(i)
        for j in graph[i]:
            if i != j and i in ids and j in ids \
            and i not in deleted_friend_ids and j not in deleted_friend_ids:
                G.add_edge(i, j)

    G_nodes = G.nodes.keys()
    friend_ids_str = ', '.join([str(friend_id) for friend_id in G_nodes])
    info = GetUserInfo(friend_ids_str)
    return info, G  

def GetFriendsInfo(user_id):

    ids = GetFriends(user_id)
    graph = {}
    deleted_friend_ids = []

    for friend_id in tqdm.tqdm(ids):
        try:
            graph[friend_id] = GetFriends(friend_id)
        except:
            deleted_friend_ids.append(friend_id)

    graph[int(user_id)] = GetFriends(user_id)
 
    G = nx.Graph(directed=False)

    for i in graph:
        G.add_node(i)
        for j in graph[i]:
            if i != j and i in ids and j in ids \
            and i not in deleted_friend_ids and j not in deleted_friend_ids:
                G.add_edge(user_id,j)
                G.add_edge(i, j)

    G_nodes = G.nodes.keys()
    friend_ids_str = ', '.join([str(friend_id) for friend_id in G_nodes])
    info = GetUserInfo(friend_ids_str)
    return info, G

def corr_analysis(first_score, second_score, G):
    first_score_ranking = list(nx.get_node_attributes(G, first_score+'Rank').values())
    second_score_ranking = list(nx.get_node_attributes(G, second_score+'Rank').values())
    
    plt.plot(first_score_ranking, second_score_ranking, 'g.')
    plt.title(
    'Коэффициент корреляции Пирсона: {} \
    \nКоэффициент ранговой корреляции Спирмена: {}\
    \nКоэффициент ранговой корреляции Кендалла: {}'.format( \
        str(round(scipy.stats.stats.pearsonr(first_score_ranking, second_score_ranking)[0],3)),
        str(round(scipy.stats.stats.spearmanr(first_score_ranking, second_score_ranking)[0],3)),
        str(round(scipy.stats.stats.kendalltau(first_score_ranking, second_score_ranking)[0],3))))
    plt.xlabel(first_score)
    plt.ylabel(second_score)

def main():

    switch = int(input("Выберите действие: \n 1 - Получить данные о подписчиках группы и их дружеских связей \n 2 - Получить данные о пользователе и его дружеских связях \n"))

    if (switch == 1):
        public = input("Введите ccылку на открытое сообщество/группу: ")
        data, Gr = GetSubsFriendsInfo(public)
        
        id_list = [user['id'] for user in data]
        member_name = [user['first_name'] + ' ' + user['last_name'] for user in data]
        member_name = dict(zip(id_list, member_name))
        nx.set_node_attributes(Gr, member_name, 'Name')

        member_gender = [user['sex'] for user in data]
        member_gender = dict(zip(id_list, member_gender))
        nx.set_node_attributes(Gr, member_gender, 'Gender')

        member_city = [user['city']['title'] if 'city' in user else '' for user in data]
        member_city = dict(zip(id_list, member_city))
        nx.set_node_attributes(Gr, member_city, 'City')

        member_university = [user['university_name'] if 'university' in user else '' for user in data]
        member_university = dict(zip(id_list, member_university))
        nx.set_node_attributes(Gr, member_university, 'University')

        nx.write_graphml(Gr, public+'.graphml')

        degree_centrality = nx.degree_centrality(Gr)
        closeness_centrality = nx.closeness_centrality(Gr)
        betweenness_centrality = nx.betweenness_centrality(Gr)
        eigenvector_centrality = nx.eigenvector_centrality(Gr)
        pagerank = nx.pagerank(Gr)

        scores = {'DegreeCentrality': degree_centrality, 'ClosenessCentrality': closeness_centrality,
                'BetweennessCentrality': betweenness_centrality, 'EigenvectorCentrality': eigenvector_centrality,
                'PageRank': pagerank}

        for i, j in scores.items():
            score_ranking_dict = {key: rank for rank, key in enumerate(sorted(j, key = j.get, reverse=True), 1)}
            nx.set_node_attributes(Gr, j, i)
            nx.set_node_attributes(Gr,score_ranking_dict,i+'Rank')

        plt.figure(figsize=(14,4))

        plt.subplot(2,2,1)
        corr_analysis('PageRank', 'DegreeCentrality', Gr)
        plt.subplot(2,2,2)
        corr_analysis('PageRank', 'ClosenessCentrality', Gr)
        plt.subplot(2,2,3)
        corr_analysis('PageRank', 'BetweennessCentrality', Gr)
        plt.subplot(2,2,4)
        corr_analysis('PageRank', 'EigenvectorCentrality', Gr)

        plt.show()
   
    if (switch == 2):
        user = input("Введите короткую ссылку человека: ")
        info, G = GetFriendsInfo(user)

        id_list = [user['id'] for user in info]
        member_name = [user['first_name'] + ' ' + user['last_name'] for user in info]
        member_name = dict(zip(id_list, member_name))
        nx.set_node_attributes(G, member_name, 'Name')

        member_gender = [user['sex'] for user in info]
        member_gender = dict(zip(id_list, member_gender))
        nx.set_node_attributes(G, member_gender, 'Gender')

        member_city = [user['city']['title'] if 'city' in user else '' for user in info]
        member_city = dict(zip(id_list, member_city))
        nx.set_node_attributes(G, member_city, 'City')

        member_university = [user['university_name'] if 'university' in user else '' for user in info]
        member_university = dict(zip(id_list, member_university))
        nx.set_node_attributes(G, member_university, 'University')

        nx.write_graphml(G, user+'.graphml')

        degree_centrality = nx.degree_centrality(G)
        closeness_centrality = nx.closeness_centrality(G)
        betweenness_centrality = nx.betweenness_centrality(G)
        eigenvector_centrality = nx.eigenvector_centrality(G)
        pagerank = nx.pagerank(G)

        scores = {'DegreeCentrality': degree_centrality, 'ClosenessCentrality': closeness_centrality,
                'BetweennessCentrality': betweenness_centrality, 'EigenvectorCentrality': eigenvector_centrality,
                'PageRank': pagerank}

        for i, j in scores.items():
            score_ranking_dict = {key: rank for rank, key in enumerate(sorted(j, key = j.get, reverse=True), 1)}
            nx.set_node_attributes(G, j, i)
            nx.set_node_attributes(G,score_ranking_dict,i+'Rank')

        plt.figure(figsize=(14,4))

        plt.subplot(2,2,1)
        corr_analysis('PageRank', 'DegreeCentrality', G)
        plt.subplot(2,2,2)
        corr_analysis('PageRank', 'ClosenessCentrality', G)
        plt.subplot(2,2,3)
        corr_analysis('PageRank', 'BetweennessCentrality', G)
        plt.subplot(2,2,4)
        corr_analysis('PageRank', 'EigenvectorCentrality', G)

        plt.show()
    
if __name__ == '__main__':
    suppress_qt_warnings()
    main()