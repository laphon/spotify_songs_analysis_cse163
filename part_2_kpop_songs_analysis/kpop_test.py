"""
This Python file tests functions from
kpop_songs_analysis.py
"""
from kpop_songs_analysis import sub_genres_comparison
from kpop_songs_analysis import kpop_and_all_songs_comparison
from kpop_songs_analysis import identify_kpop_type
import pandas as pd


test_kpop = pd.read_csv("test_datasets/test_kpop_dataset")
test_all = pd.read_csv("test_datasets/test_all_songs_dataset")


def test_sub_genres_comparison():
    """
    Tests the method sub_genres_comparison
    from kpop_songs_analysis.py.
    """
    test_kpop['kpop_type'] = test_kpop['genres'].apply(identify_kpop_type)
    sub_genres_comparison(test_kpop, 2009, 'danceability', 'test_results')
    sub_genres_comparison(test_kpop, 2009, 'energy', 'test_results')


def test_kpop_and_all_songs_comparison():
    """
    Tests the method kpop_and_all_songs_comparison
    from kpop_songs_analysis.py.
    """
    test_kpop['kpop_type'] = test_kpop['genres'].apply(identify_kpop_type)
    test_all['dataset'] = 'all_songs'
    test_kpop['dataset'] = 'kpop_songs'
    df = pd.concat([test_all, test_kpop], sort=False)
    kpop_and_all_songs_comparison(df, 2000, 'danceability', 'test_results')
    kpop_and_all_songs_comparison(df, 2000, 'energy', 'test_results')


def main():
    test_sub_genres_comparison()
    test_kpop_and_all_songs_comparison()


if __name__ == "__main__":
    main()
