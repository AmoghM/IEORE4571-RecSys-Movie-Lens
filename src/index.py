from annoy import AnnoyIndex
from argparse import ArgumentParser
import time,pickle,json
def create_annoy_index(pickle_path,write_annoy_path,dim):
    st = time.time()
    movie_user = json.load(open(pickle_path,encoding='utf-8'))
    t = AnnoyIndex(dim, 'angular')
    for k,v in movie_user.items():
        t.add_item(int(k), v)
    t.build(10) # 10 trees
    t.save(write_annoy_path)
    end = time.time()
    print("TIME TOOK TO INDEX %d dim and %d entries is %f" %( 610, len(movie_user), end-st))

def load_annoy(read_annoy_path, dim=610):
    an = AnnoyIndex(dim,'angular')
    an.load(read_annoy_path)
    return an

def get_nearest_items(an,item,knn=10):
    '''
    Returns a tuple containing item list and distance list
    Example:
    ([450, 291, 54, 352], [0.0, 0.8344222903251648, 0.8795796036720276, 0.8832817077636719])
    '''
    return an.get_nns_by_item(item, knn,include_distances=True)

    
if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-rp", help="read movie user pickle", default="../data/train_dataset.json")
    parser.add_argument("-annoy", help="annoy index path", default="../data/train.ann")
    parser.add_argument("-dim", help="dimension", default=610,type=int)

    args = parser.parse_args()
    create_annoy_index(args.rp,args.annoy,args.dim)
    an = load_annoy(args.annoy,args.dim)
    print(get_nearest_items(an,450,10)) #for testing