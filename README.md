### Step to follow for recommendation on Movie Lens dataset:
a) Pre-run step:
* Clone the repository
* Download "20MI" dataset from MovieLens here: https://grouplens.org/datasets/movielens/
* Place the extracted folder into the `data/` of the repository
* Run `data_subset.ipynb` in the `src` folder. It generates the subset of data on an annual basis starting from 2015 and going backward.

b) For ALS and FM model:
* Run src/ALS.ipynb
* Run recommendation_LightFM_WARP.ipynb

c) For Item-Item collaborative filtering:
* Run commmand to create train, test, user mapping dataset for each annual data subsets: `./src/item-item-colab/data_gen.sh`
* Run command to create annoy indexes for each annual data subsets:  `./src/item-item-colab/create_annoy.sh`
* Run `python src/item-item-colab/item_colab_metric_plot.py` to generate metric plots in `output/`

### output
The output consists of plots RMSE vs Latent Factor at different levels of regularizing parameters. <br>
```File format: rmse_<regularizing_parameter>_<year>.png``` For example: `rmse_0.01_2015.png`

### src
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
default settings : `python data_preprocessing.py`[The default setting assumes your ratings.csv files are in data/ folder]<br> 
custom path settings: `python data_processing.py -rf ../data/ml-latest-small/ratings.csv -wp ../data/small-movie-user.p -dim 610`

where 
1. rf: reading csv file path
2. wp: write path for pickle
3. dim: dimension of the user (total unique user in the dataset)

#### COMMANDS TO RUN FOR ANNOY INDEX
default settings: `python index.py` [The default setting assumes your files are in data/ folder]<br>
custom path settings: `python index.py -rp ../data/small-movie-user.p -annoy ../data/small-movie-user.ann -dim 610`

where:
1. rp: reading pickle file path
2. annoy: writing annoy index path
3. dim: dimension of the user (total unique users in the dataset)
