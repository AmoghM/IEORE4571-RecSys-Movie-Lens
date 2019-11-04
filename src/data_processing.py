import pickle,time,random,copy,json,gc
from argparse import ArgumentParser
import pandas as pd
# def data_preprocess(path):
    # df = pd.read_csv(path)
    # print(len(df['userId'].unique()))

    # movie_user, tuple_movie_user, usr_to_id, id_to_usr = {}, [], {}, {}
    # with open(path) as f:
    #     f.readline()
    #     id = 0
    #     for row in f:
    #         r = row.split(",")
    #         movie = int(r[1])
    #         user = int(r[0])-1
    #         rating = float(r[2])

    #         uid = usr_to_id.get(user,-1)
    #         if uid == -1:
    #             usr_to_id[user] = id
    #             id_to_usr[id] = user

    #         m_id = movie_user.get(movie,-1)
    #         if m_id ==-1:
    #             movie_user[movie]=[(id,rating)]
    #         else:
    #             movie_user[movie].append((id,rating))
    #         tuple_movie_user.append((movie,id))
    #         id+=1
    # return movie_user, tuple_movie_user, usr_to_id, id_to_usr, id

# def construct_item_user_matrix(movie_user,dim):
    # movie_user_dic={}
    # for movie,usr_rate in movie_user.items():
    #     matrix=[0.0]*int(dim)
    #     for ur in usr_rate:
    #         usr = ur[0]
    #         rat = ur[1]
    #         print(ur)
    #         matrix[usr] = rat
    #     movie_user_dic[movie] = matrix
    # return movie_user_dic

def data_preprocess(path):
    df = pd.read_csv(path)
    dim = df['userId'].nunique()
    del df

    movie_user, tuple_movie_user, usr_to_id, id_to_usr = {}, [], {}, {}
    with open(path) as f:
        f.readline()
        id = 0
        for row in f:
            r = row.split(",")
            movie = int(r[1])
            user = int(r[0])
            rating = float(r[2])

            uid = usr_to_id.get(user,-1)
            if uid == -1:
                usr_to_id[user] = id
                id_to_usr[id] = user
                uid = id
                id+=1

            if movie not in movie_user:
                movie_user[movie] = [0.0]*dim

            movie_user[movie][uid] = rating
            tuple_movie_user.append((movie,uid))

    return movie_user, tuple_movie_user

def train_test_split(movie_user, tuple_movie_user):
    train_data = copy.deepcopy(movie_user)
    data_size = len(tuple_movie_user)
    test_size = int(0.10*data_size)

    print("total movie-user items", len(movie_user))
    print("size OF THE test", test_size)
    
    random.shuffle(tuple_movie_user)
    temp_test = random.sample(tuple_movie_user, test_size)
    test_data = {}
    for test in temp_test:
        movie = test[0]
        user = test[1]
        rating = train_data[movie][user]
        test_data[movie] = {user:rating}
        train_data[movie][user] = 0
    
    return train_data, test_data

def export_dataset(data,export_path):
    pickle.dump(movie_user, open(export_path, "wb") )
    # json.dump(data,open(export_path,'w'))

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-rf", help="read path of the csv", default="../data/ml-latest-small/ratings.csv")
    parser.add_argument("-d", help="write path of the pickle", default="../data/unmasked_dataset.p")
    parser.add_argument("-train", help="write path of the pickle", default="../data/train_dataset.p")
    parser.add_argument("-test", help="write path of the pickle", default="../data/test_dataset.p")
    # parser.add_argument("-dim", help="dimension", default=610,type=int)
    args = parser.parse_args()
    
    # movie_user, tuple_movie_user, uid, idu, dim = data_preprocess(path = args.rf)
    # movie_user_rating_matrix = construct_item_user_matrix(movie_user,dim)
    movie_user, tuple_movie_user = data_preprocess(path = args.rf)
    train_data, test_data = train_test_split(movie_user, tuple_movie_user)

    export_dataset(movie_user, export_path = args.d)
    export_dataset(train_data,export_path = args.train)
    export_dataset(test_data,export_path = args.test)
    # export_dataset(uid,export_path ='../data/user_to_id.json')
    # export_dataset(idu,export_path ='../data/id_to_user.json')

# EXAMPLE COMMAND TO RUN:  python data_processing.py -rf ../data/ml-latest-small/ratings.csv -wp ../data/small-movie-user.p -dim 610