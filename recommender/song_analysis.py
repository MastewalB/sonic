# import csv
# import uuid
import os
import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# songs = pd.read_csv('songdata.csv')

# songs.head()


# input_file = "songdata.csv"
# output_file = "songdata_updated.csv"


# def add_unique_id(input_file, output_file):
#     with open(input_file, "r") as input, open(output_file, "w") as output:
#         reader = csv.reader(input)
#         writer = csv.writer(output)

#         # read header
#         header = next(reader)
#         # append new column name
#         header.append("ID")
#         # write header
#         writer.writerow(header)

#         # write rows
#         for row in reader:
#             # create unique id
#             row.append(str(uuid.uuid4()))
#             writer.writerow(row)

csv_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'shrunk_dataset.csv')

songs = pd.read_csv(csv_file_path)
songs.head()


# songs = songs.groupby('artist').head(10)


# songs = songs.sample(n=10000).drop('link', axis=1).reset_index(drop=True)
songs = songs.drop('link', axis=1).reset_index(drop=True)
songs.head()


# songs['text'] = songs['text'].str.replace(r'\n', '')
# the below one is an updated version
songs['text'] = songs['text'].str.replace(r'\n', '', regex=True)


tfidf = TfidfVectorizer(analyzer='word', stop_words='english')

lyrics_matrix = tfidf.fit_transform(songs['text'])

cosine_similarities = cosine_similarity(lyrics_matrix)


def recommend(new_song_lyrics):
    # new_song_lyrics.str.replace(r'\n', '', regex=True)
    new_lyrics_matrix = tfidf.transform([new_song_lyrics])

    similarities = cosine_similarity(new_lyrics_matrix, lyrics_matrix)
    similar_indices = np.argsort(similarities[0])[::-1]

    similar_songs = songs.iloc[similar_indices[1:]
                               ][['song_id', 'song', 'artist']].values.tolist()
    
    return similar_songs
