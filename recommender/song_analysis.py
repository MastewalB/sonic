# import csv
# import uuid
import os
import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

csv_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'shrunk_dataset.csv')

songs = pd.read_csv(csv_file_path)

songs = songs.drop('link', axis=1).reset_index(drop=True)

# cleaning the data
songs['text'] = songs['text'].str.replace(r'\n', '', regex=True)

tfidf = TfidfVectorizer(analyzer='word', stop_words='english')

lyrics_matrix = tfidf.fit_transform(songs['text'].fillna(''))

cosine_similarities = cosine_similarity(lyrics_matrix)

def recommend(new_song_lyrics):
    # new_song_lyrics.str.replace(r'\n', '', regex=True)
    new_lyrics_matrix = tfidf.transform([new_song_lyrics])

    similarities = cosine_similarity(new_lyrics_matrix, lyrics_matrix)
    similar_indices = np.argsort(similarities[0])[::-1]

    similar_songs = songs.iloc[similar_indices[1:]][['song_id']].values.tolist()
    
    return similar_songs
