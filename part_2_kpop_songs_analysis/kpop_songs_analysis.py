"""
This Python files performs data visualization
on Spotify k-pop songs and all Spotify songs
"""

import altair as alt
import pandas as pd


def identify_kpop_type(genres):
    """
    Indentify whether genres contains
    'boy group', 'girl group' or neither ot them.
    """
    if 'k-pop boy group' in genres:
        return 'boy group'
    elif 'k-pop girl group' in genres:
        return 'girl group'
    else:
        return 'other'


def sub_genres_comparison(kpop_songs, y, feature, _dir):
    """
    Save a chart in html format made from df to directory _dir,
    comparing features between k-pop sub genres starting from year y.
    """
    df = kpop_songs[kpop_songs['year'] >= y]
    lines = alt.Chart(df).mark_line().encode(
        alt.X('year', scale=alt.Scale(zero=False)),
        alt.Y(f'mean({feature})', scale=alt.Scale(zero=False, padding=1)),
        color='kpop_type'
    ).properties(title=f"{feature} by year")
    rules = alt.Chart(df).mark_rule().encode(
        y=f'mean({feature}):Q',
        color='kpop_type'
    )
    points = alt.Chart(df).mark_circle(opacity=0.15).encode(
        alt.X('year', scale=alt.Scale(zero=False)),
        alt.Y(f'{feature}', scale=alt.Scale(zero=False, padding=1)),
        color='kpop_type',
        tooltip=['name', 'artists', 'kpop_type', f'{feature}']
    )
    (lines+points+rules).save(f"{_dir}/\
                              kpop_sub_genres_{feature}_by_year.html")


def kpop_and_all_songs_comparison(df, y, feature, _dir):
    """
    Save a chart in html format made from df to directory _dir,
    comparing features of all songs and k-pop songs starting from year y.
    """
    df = df[df['year'] >= y]
    chart = alt.Chart(df).mark_line().encode(
        alt.X('year', scale=alt.Scale(zero=False)),
        alt.Y(f'mean({feature})', scale=alt.Scale(zero=False, padding=1)),
        color='dataset'
    ).properties(title=f'{feature} of k-pop songs')
    chart.save(f"{_dir}/kpop_&_all_songs_{feature}.html")


def main():
    # Turn off number of rows limit
    alt.data_transformers.disable_max_rows()

    # Download datasets
    all_songs = pd.read_csv("source_files/spotify_songs.csv")
    kpop_songs = pd.read_csv("source_files/spotify_kpop_songs.csv")

    kpop_songs['kpop_type'] = kpop_songs['genres'].apply(identify_kpop_type)
    kpop_songs['year'] = kpop_songs['release_date'
                                    ].apply(lambda date:
                                            int(date.split('-')[0]))
    features = ['popularity', 'danceability', 'energy', 'acousticness',
                'speechiness', 'liveness', 'valence']
    # Compare features between k-pop sub-genres
    for feature in features:
        sub_genres_comparison(kpop_songs, 2009, feature, 'part_2.2')

    # Concatenate k-pop songs and all songs
    all_songs['dataset'] = 'all_songs'
    kpop_songs['dataset'] = 'kpop_songs'
    df = pd.concat([all_songs, kpop_songs], sort=False)

    # Compare features between k-pop songs and all songs
    for feature in features:
        kpop_and_all_songs_comparison(df, 2000, feature, 'part_2.1')


if __name__ == "__main__":
    main()
