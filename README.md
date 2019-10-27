1. `data_preprocessing.py` reads the ratings.csv file in the data/ directory and generates a pickle file.
The file pickled is of the format:
    ```
    { 
    movie-id-1 : [<list of user's rating>],

    movie-id-2 : [<list of user's rating>]
    ...
    }
    ```

2. `index.py` reads the generated pickle file and creates an annoy index <br>
#### COMMANDS TO RUN FOR DATA PREPROCESSING
default settings : `python data_preprocessing.py`<br>
custom path settings: `python data_processing.py -rf ../data/ml-latest-small/ratings.csv -wp ../data/small-movie-user.p -dim 610`

where 
1. rf: reading csv file path
2. wp: write path for pickle
3. dim: dimension of the user (total unique user in the dataset)

#### COMMANDS TO RUN FOR ANNOY INDEX
default settings: `python index.py`<br>
custom path settings: `python index.py -rp ../data/small-movie-user.p -annoy ../data/small-movie-user.ann -dim 610`

where:
1. rp: reading pickle file path
2. annoy: writing annoy index path
3. dim: dimension of the user (total unique users in the dataset)
