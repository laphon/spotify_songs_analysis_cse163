"""
top_songs_analysis.py
Phoenix Yi
CSE 163 SU 2020 Final Project Part 1
Description:
This file tests all the functions in top_songs_analysis.py.
It is basically testing the functions using a smaller datasets
than the original one. And it will output some testing charts
to the directory of 'Tests' folder.
"""

import top_songs_analysis as tsa
import pandas as pd


def test_trend_analysis(test_top, label):
    """
    test_trend_analysis(test_top, label),
    test_top and label are all dataframes.
    Produces the testing charts of the trend_analysis function
    in the top_songs_analysis.py.
    """
    tsa.trend_analysis(test_top, label, 'dnce', 'Tests')
    tsa.trend_analysis(test_top, label, 'val', 'Tests')
    tsa.trend_analysis(test_top, label, 'spch', 'Tests')


def test_feature_difference(test_top, test_all):
    """
    test_feature_difference(test_top, test_all),
    test_top and test_all are all dataframes.
    Produces the testing charts of the feature_difference function
    in the top_songs_analysis.py.
    """
    features1 = ['dnce', 'val', 'spch']
    features2 = ['nrgy', 'dnce', 'acous', 'val', 'spch', 'live']
    tsa.feature_difference(test_top, test_all, features1, 'Tests')
    tsa.feature_difference(test_top, test_all, features2, 'Tests')


def test_feature_distribution(test_top):
    """
    test_feature_distribution(test_top),
    test_top is a dataframe.
    Outputs the testing charts of the feature_distribution function
    in the top_songs_analysis.py.
    """
    tsa.feature_distribution(test_top, 'dnce', 'Tests')
    tsa.feature_distribution(test_top, 'acous', 'Tests')
    tsa.feature_distribution(test_top, 'val', 'Tests')


def test_mean_feature_all(test_all):
    """
    test_mean_feature_all(test_all),
    test_all is a dataframe.
    Generates the testing charts of the mean_feature_all function
    in the top_songs_analysis.py.
    """
    tsa.mean_feature_all(test_all, 'acous', 'Tests')
    tsa.mean_feature_all(test_all, 'dnce', 'Tests')


def main():
    # Setting up the environment of datasets and add new columns for
    # analysis use.
    top_data = pd.read_csv('top_spotify_songs.csv', encoding='cp1252')
    all_data = pd.read_csv('spotify_songs.csv')
    all_data['dnce'] = all_data['danceability']*100
    all_data['nrgy'] = all_data['energy']*100
    all_data['acous'] = all_data['acousticness']*100
    all_data['val'] = all_data['valence']*100
    all_data['spch'] = all_data['speechiness']*100
    all_data['live'] = all_data['liveness']*100
    all_data['mean dataset'] = 'All songs'
    top_data['mean dataset'] = 'Top songs'
    # Creating smaller counterparts of two datasets.
    test_top = top_data.loc[:200, :]
    test_all = all_data.loc[len(all_data)-1000:len(all_data), :]
    # Merging two datasets(top songs and 160k songs) for labelings.
    label = pd.concat([test_all, test_top], sort=False)
    label2 = label[(label['year'] >= 2010) & (label['year'] <= 2019)]
    # Executing the testing functions.
    test_trend_analysis(test_top, label2)
    test_feature_difference(test_top, test_all)
    test_feature_distribution(test_top)
    test_mean_feature_all(test_all)


if __name__ == '__main__':
    main()
