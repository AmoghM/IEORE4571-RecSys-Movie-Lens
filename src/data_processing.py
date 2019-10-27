import pickle,time
from argparse import ArgumentParser
def data_preprocess(path,dim):
    movie_user={}
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
    return movie_user

def export_dataset(movie_user,export_path):
    pickle.dump(movie_user, open(export_path, "wb") )

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-rf", help="read path of the csv", default="../data/ml-latest-small/ratings.csv")
    parser.add_argument("-wp", help="write path of the pickle", default="../data/small-movie-user.p")
    parser.add_argument("-dim", help="dimension", default=610,type=int)
    args = parser.parse_args()
    
    movie_user = data_preprocess(path = args.rf, dim = int(args.dim))
    export_dataset(movie_user,export_path = args.wp)

# EXAMPLE COMMAND TO RUN:  python data_processing.py -rf ../data/ml-latest-small/ratings.csv -wp ../data/small-movie-user.p -dim 610