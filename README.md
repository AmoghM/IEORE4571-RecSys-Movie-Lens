### Step to follow for recommendation on Movie Lens dataset:
a) Pre-run step:
* Clone the repository
* Install packages and dependencies: `pip install -r requirements.txt`
* Download "20MI" dataset from MovieLens here: https://grouplens.org/datasets/movielens/
* Place the extracted folder into the `data/` of the repository
* Run `data_subset.ipynb` in the `src` folder. It generates the subset of data on an annual basis starting from 2015 and going backward.

b) For Exploratory Data Analysis: `src/matrix-factorization/EDA_personalization.ipynb`

c) For ALS and FM model:
* Run src/ALS.ipynb
* Run recommendation_LightFM_WARP.ipynb

d) For Item-Item collaborative filtering:
* Run commmand to create train, test, user mapping dataset for each annual data subsets: `./src/item-item-colab/data_gen.sh`
* Run command to create annoy indexes for each annual data subsets:  `./src/item-item-colab/create_annoy.sh`
* Run `python src/item-item-colab/item_colab_metric_plot.py` to generate metric plots in `output/`

**NOTE**: Final report addressing business use cases, assumptions, design choices, metrics, plots, algorithms here:
https://github.com/AmoghM/IEORE4571-RecSys-Movie-Lens/blob/master/Final%20Report%20Movie%20Lens%20RecSys.pdf

**Credits**
1. [Item-based collaborative filtering recommendation algorithms](http://files.grouplens.org/papers/www10_sarwar.pdf)
2. [Apache Spark](https://spark.apache.org/docs/2.2.0/ml-collaborative-filtering.html)
3. [LightFM](https://towardsdatascience.com/solving-business-usecases-by-recommender-system-using-lightfm-4ba7b3ac8e62)
4. [Annoy Index](https://github.com/spotify/annoy)
