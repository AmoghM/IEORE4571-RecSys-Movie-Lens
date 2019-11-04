import pickle,time,random,copy,json,gc
from argparse import ArgumentParser
import pandas as pd
def data_preprocess(path):
    df = pd.read_csv(path)
    dim = df['userId'].nunique()
    del df

    movie_user, tuple_movie_user, usr_to_id, id_to_usr = {}, [], {}, {}
    with open(path) as f:
        f.readline()
        id = 0
        for en, row in enumerate(f):
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

    return movie_user, tuple_movie_user, usr_to_id, id_to_usr

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
        test_data[user] = {movie:rating}
        train_data[movie][user] = 0
    return train_data, test_data

def export_dataset(data,export_path):
    # pickle.dump(movie_user, open(export_path, "wb") )
    json.dump(data,open(export_path,'w'))

def json_export(data,path):
    json.dump(data,open(path,'w'))

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-rf", help="read path of the csv", default="../data/ml-latest-small/ratings.csv")
    parser.add_argument("-d", help="write path of the pickle", default="../data/unmasked_dataset.json")
    parser.add_argument("-train", help="write path of the pickle", default="../data/train_dataset.json")
    parser.add_argument("-test", help="write path of the pickle", default="../data/test_dataset.json")
    args = parser.parse_args()

    movie_user, tuple_movie_user, uid, idu = data_preprocess(path = args.rf)
    train_data, test_data = train_test_split(movie_user, tuple_movie_user)
    export_dataset(movie_user, export_path = args.d)
    export_dataset(train_data,export_path = args.train)
    export_dataset(test_data, args.test)
    export_dataset(uid,export_path ='../data/user_to_id.json')
    export_dataset(idu,export_path ='../data/id_to_user.json')

# EXAMPLE COMMAND TO RUN:  python data_processing.py -rf ../data/ml-latest-small/ratings.csv -wp ../data/small-movie-user.p -dim 610