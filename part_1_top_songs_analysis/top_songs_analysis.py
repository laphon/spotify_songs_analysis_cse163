"""
top_songs_analysis.py
Phoenix Yi
CSE 163 SU 2020 Final Project Part 1
Description:
This file will load, store, modify the top songs csv file and
all 160k Spotify songs we found to conduct our research. It will
generate several charts(including interactive and fixed charts)
to show 1) the general trend of all tops compared to the 160k songs;
2) the distribution of those top songs by popularity.
For the datasets, nrgy means energy, dnce means danceability, acous
means acousticness, val means valence, spch means speechiness, and
live means liveness.
"""

import pandas as pd
import altair as alt


def trend_analysis(top_data, label2, feature, _dir):
    """
    trend_analysis(top_data, label2, feature, _dir),
    top_data and label2 are dataframes, feature and _dir are strings.
    label2 is a dataframe that converge the top songs dataset with the
    160k songs dataset.
    This will ouput htmls of charts including the points of feature values
    and the lines of general trends of top songs and 160k songs.
    """
    single_selection = alt.selection_single(on='mouseover')
    lightgray = alt.value('lightgray')
    green = alt.value('#68b0ab')
    # Point chart for top songs.
    chart1 = alt.Chart(top_data).mark_point().encode(
        x='year:N',
        y=alt.Y(feature+':Q', axis=alt.Axis(title='Value of '+feature)),
        color=alt.condition(single_selection, green, lightgray),
        tooltip='title:N'
    ).properties(
        title=feature + '(0-99) Over Years',
        selection=single_selection
    ).interactive()
    # Line chart for converged dataset.
    chart2 = alt.Chart(label2).mark_line().encode(
        x='year:N',
        y='mean('+feature+'):Q',
        color='mean dataset'
    )
    chart = chart1 + chart2
    chart.save(f"{_dir}/spotify_top_trend_{feature}.html")


def feature_difference(top_data, all_data, features, _dir):
    """
    feature_difference(top_data, all_data, _dir),
    top_data and all_data are dataframes and _dir is a string.
    This method output only one bar chart about the differences of
    feature values between the top songs and 160k songs data.
    Also saves the output chart to given directory as a html file.
    """
    diff = []
    # Calculating each value difference.
    for feature in features:
        diff.append(top_data[feature].mean() - all_data[feature].mean())
    # Generating a dataframe containing the differences and features.
    difference = pd.DataFrame({'feature': features, 'value': diff})
    chart = alt.Chart(difference).mark_bar().encode(
        x='feature:N',
        y=alt.Y('value:Q', axis=alt.Axis(title='Difference in Values'))
    ).properties(
        title='Mean Value Differences'
    )
    len_features = len(features)
    chart.save(f"{_dir}/difference_in_{len_features}_features.html")


def feature_distribution(top_data, feature, _dir):
    """
    feature_distribution(top_data, feature, _dir),
    top_data is a dataframe, features and _dir are strings.
    Creates the output of the point chart of feature values
    distribution of the top songs and generates the html file
    to check the chart.
    """
    single_selection = alt.selection_single(on='mouseover')
    lightgray = alt.value('lightgray')
    green = alt.value('#68b0ab')
    chart = alt.Chart(top_data).mark_point().encode(
        x='pop:Q',
        y=alt.Y(feature, axis=alt.Axis(title='Value of '+feature)),
        color=alt.condition(single_selection, green, lightgray),
        tooltip='title:N'
    ).properties(
        title='Distribution of '+feature+' by Popularity',
        selection=single_selection
    ).interactive()
    chart.save(f"{_dir}/distribution_{feature}_over_pop.html")


def mean_feature_all(all_data, feature, _dir):
    """
    mean_feature_all(all_data, feature, _dir),
    all_data is a dataframe, features and _dir are strings,.
    Outputs the html file of the charts that shows the trend of
    the mean values of the given features in the 160k dataset
    over 100 years.
    """
    data = all_data.groupby('year')[feature].mean()
    data = pd.DataFrame({'year': data.index, feature: data.values})
    chart = alt.Chart(data).mark_line().encode(
        x='year:N',
        y=alt.Y(feature+':Q', axis=alt.Axis(title='Mean of '+feature))
    ).properties(
        title='Mean of '+feature+' over Years'
    )
    chart.save(f"{_dir}/mean_value_of_{feature}_all_years.html")


def main():
    # Setting up the environment of datasets and add new columns for
    # analysis use.
    alt.data_transformers.disable_max_rows()
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
    top_2019 = top_data[top_data['year'] == 2019]
    all_2019 = all_data[all_data['year'] == 2019]
    # Merging two datasets(top songs and 160k songs) for lebeling.
    label = pd.concat([all_data, top_data], sort=False)
    label2 = label[(label['year'] >= 2010) & (label['year'] <= 2019)]
    features = ['nrgy', 'dnce', 'acous', 'val', 'spch', 'live']
    # Running through all the analysis charts and generating outputs.
    for feature in features:
        trend_analysis(top_data, label2, feature, 'Part1-1')
    feature_difference(top_2019, all_2019, features, 'Part1-1')
    for feature in features:
        feature_distribution(top_data, feature, 'Part1-2')
    mean_feature_all(all_data, 'acous', 'Part1-2')
    mean_feature_all(all_data, 'spch', 'Part1-2')


if __name__ == '__main__':
    main()
