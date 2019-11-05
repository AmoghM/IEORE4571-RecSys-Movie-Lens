import pandas as pd
import index
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
import math
import time
import json
    
    
def get_errors(test_data, tag, k):
    ratings = pd.read_csv("../data/ratings_subset"+ tag +".csv", encoding="ISO-8859-1")
    ##ISO 8859-1 is a single-byte encoding that can represent the first 256 Unicode characters
    with open("../data/id_to_user"+ tag +".json", "r") as read_file:
        id_to_user = json.load(read_file)
    with open("../data/user_to_id"+ tag +".json", "r") as read_file:
        user_to_id = json.load(read_file)
    dim = len(ratings['userId'].unique())
    an = index.load_annoy(r"../data/train"+ tag +".ann", dim)
    
    predicted_dataset = get_predicted_ratings(test_data, ratings, id_to_user, an, k)    
    test_data_ratings_list = []
    pred_ratings_list = []
    for entry in predicted_dataset: #for each userId. entry = entry_user
        entry_id = user_to_id[str(entry)]
        for each in predicted_dataset[entry]: #for each userId, movieId pair (both loops together)
            test_data_ratings_list.append(test_data[str(entry_id)][str(each)]) #true
            pred_ratings_list.append(predicted_dataset[entry][each]) #predicted
    #mae, rmse
    mae = mean_absolute_error(test_data_ratings_list, pred_ratings_list) #(y_true, y_pred)
    mse = mean_squared_error(test_data_ratings_list, pred_ratings_list) #(y_true, y_pred)
    rmse = math.sqrt(mse)
    return mae, rmse
    
    
    
def get_predicted_ratings(test_data, ratings, id_to_user, an, k):
    predicted_dataset = {}
    similar_items = {}
    for entry in test_data: #entry = id (str)
        entry_user = id_to_user[entry]
        user_u_ratings = ratings.loc[ratings['userId'] == entry_user][['movieId', 'rating']]
        predicted_dataset[entry_user] = {} #user
        for each in test_data[entry]: #for each userId, movieId pair (both loops together)
            Num = 0
            Den = 0
            each = int(each) ##
            similar_items[each] = index.get_nearest_items(an, each, k)
            for item, its_sim in zip(similar_items[each][0], similar_items[each][1]):
                if item in user_u_ratings['movieId'].tolist():
                    u_rate = (user_u_ratings.loc[user_u_ratings['movieId'] == item][['rating']])['rating'].tolist()
                    Num = Num + (u_rate[0] * its_sim)
                    Den = Den + its_sim
            if Den != 0:
                predicted_dataset[entry_user][each] = Num/Den
            else:
                ratings_u = (ratings.loc[ratings['userId'] == entry_user][['rating']])['rating'].tolist()
                sum_ratings_u = sum(ratings_u)
                if len(ratings_u) != 0:
                    u_rate = sum_ratings_u/len(ratings_u)
                    predicted_dataset[entry_user][each] = u_rate
                else:
                    predicted_dataset[entry_user][each] = 0
    return predicted_dataset