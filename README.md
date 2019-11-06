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
