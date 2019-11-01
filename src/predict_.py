import index
import time
import pandas as pd
from collections import Counter
import operator
import pickle

ratings = pd.read_csv("../data/ml-latest-small/ratings.csv", encoding="ISO-8859-1")
##ISO 8859-1 is a single-byte encoding that can represent the first 256 Unicode characters
an = index.load_annoy(r"C:\Users\swarn\Desktop\Masters\Fall19\PersonalizationT\project_1\IEORE4571master\data\train.ann", 610)
test_dataset = pd.read_pickle("../data/test_dataset.p")

def user_recommendations(user_u, M): #specific user, number of recommendations you require
    set_items = ratings.loc[ratings['userId'] == user_u][['movieId']]
    set_items = set_items['movieId'].tolist()
    similar_items = {}
    items_list=[]
    item_sim_list = []
    for each_item in set_items:
        similar_items[each_item] = index.get_nearest_items(an, each_item)
        items_list.extend(similar_items[each_item][0])
        item_sim_list.extend(similar_items[each_item][1])
    item_freq = Counter(items_list)
    reco_list = item_freq.most_common()
    reco_list = reco_list[1:(10*M) + 1]
    predictions_user_u = get_predict_ratings(user_u, M, reco_list, similar_items)
    reco_user_u = [t[0] for t in predictions_user_u]
    return(reco_user_u, predictions_user_u) 
    
def get_predict_ratings(user_u, M, reco_list, similar_items): #specific user
    user_u_ratings = ratings.loc[ratings['userId'] == user_u][['movieId', 'rating']]
    pred_rating_list = {}
    for each in reco_list:
        Num = 0
        Den = 0
        try:
            for item, its_sim in zip(similar_items[each[0]][0], similar_items[each[0]][1]):
                u_rate = (user_u_ratings.loc[user_u_ratings['movieId'] == item][['rating']])['rating'].tolist()
                Num += (u_rate[0] * its_sim)
                Den += its_sim
        except:
            pass
        try:
            pred_rating_list[each[0]] = Num/Den
        except:
            pass
    desc_pred_rating_list = sorted(pred_rating_list.items(), key=operator.itemgetter(1), reverse=True)
    return (desc_pred_rating_list[1:M+1])

###test
#st = time.time()
# test_reco = {}
# for entry in test_dataset:
#     #print (entry)
#     test_reco[entry] = user_recommendations(entry, 10)
# end = time.time()
# print("Time for computing predictions of %d users is %f" %( len(test_dataset), end-st))