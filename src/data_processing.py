import pickle,time,random,copy
from argparse import ArgumentParser
def data_preprocess(path,dim):
    movie_user, tuple_movie_user = {}, []
    with open(path) as f:
        f.readline()
        for row in f:
            r = row.split(",")
            movie = int(r[1])
            user = int(r[0])-1
            rating = float(r[2])
            if movie not in movie_user:
                movie_user[movie] = [0.0]*dim
            movie_user[movie][user] = rating
            tuple_movie_user.append((movie,user))

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

def export_dataset(movie_user,export_path):
    pickle.dump(movie_user, open(export_path, "wb") )

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-rf", help="read path of the csv", default="../data/ml-latest-small/ratings.csv")
    parser.add_argument("-d", help="write path of the pickle", default="../data/unmasked_dataset.p")
    parser.add_argument("-train", help="write path of the pickle", default="../data/train_dataset.p")
    parser.add_argument("-test", help="write path of the pickle", default="../data/test_dataset.p")
    parser.add_argument("-dim", help="dimension", default=610,type=int)
    args = parser.parse_args()
    
    movie_user, tuple_movie_user = data_preprocess(path = args.rf, dim = int(args.dim))
    train_data, test_data = train_test_split(movie_user, tuple_movie_user)
    export_dataset(movie_user, export_path = args.d)
    export_dataset(train_data,export_path = args.train)
    export_dataset(test_data,export_path = args.test)

# EXAMPLE COMMAND TO RUN:  python data_processing.py -rf ../data/ml-latest-small/ratings.csv -wp ../data/small-movie-user.p -dim 610