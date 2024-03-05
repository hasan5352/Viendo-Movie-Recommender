import numpy as np
import pandas as pd
import os
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem.porter import PorterStemmer
from sklearn.metrics.pairwise import cosine_similarity
import requests


# GET DATA
#transform datasets to dfs
def get_datasets_as_dfs(directory: str):
    """ gets datasets from specified directory, transforms into pandas dataframes and returns dictionary of dfs
        Returns: {dataset_names: dataframes}
    """
    dataframes = {}

    for filename in os.listdir(directory):               # get all files in specified dir
        filepath = os.path.join(directory, filename)     # join file name with directory to acess file (directory/filenane)
        df = pd.read_csv(filepath)                      # construct df
        df_name = os.path.splitext(filename)[0]          # remove extension from filename and return file name 
        dataframes[df_name] = df

    return dataframes

dataframes = get_datasets_as_dfs('data')


# MERGING DATAFRAMES
# Finding common columns to use those for merging dfs
common_columns = set(dataframes['tmdb_5000_credits'].columns).intersection(set(dataframes['tmdb_5000_movies'].columns))
# mergining dfs on the 0eth common column
movies = dataframes['tmdb_5000_credits'].merge(dataframes['tmdb_5000_movies'], on=list(common_columns)[0])


# Auxillary Functions
def extract_genres_keywords(listOf_Dicts):
    """ extracts genres and keywords of every movies from respective column of df (list of dicts).
        Returns: list of genres
    """
    genres = []
    for dictionary in eval(listOf_Dicts):
        genres.append(dictionary['name'])

    return genres

def extract_cast(listOf_Dicts):
    """ extracts top given number of actors for every movie from cast column of df (list of dicts).
        Returns: list of 3 actors
    """
    num_actors = 3
    cast = []
    for i in eval(listOf_Dicts):
        cast.append(i['name'])
        num_actors -= 1
        if num_actors == 0:
            break

    return cast

def extract_director(listOf_Dicts):
    """ extracts director from crew column of df (list of dicts).
        Returns: list of 1 director
    """
    director = []
    for i in eval(listOf_Dicts):
        if i['job'].lower() == 'director':
            director.append(i['name'])
            break
    return director

def text_to_words(value):
    """ converts text to list of words - for overview column.
        removes spaces from words in a list for all columns
        Returns: list of words
    """
    if type(value) == list:
        for i, element in enumerate(value):
            element = element.replace(' ', '')
            value[i] = element
        return value
    
    words = value.split(' ')
    return words

columns_to_concat = ['crew', 'cast', 'genres', 'keywords', 'overview']
def concatColumns_intoOne(row):
    """ combines 
    """
    merged_vals = []
    for column in columns_to_concat:
        merged_vals.extend(row[column])

    return merged_vals

def list_to_str(value):
    return ' '.join(value)

def stemming_words(text):
    """ stems each word of text to its base word
    """
    stemmer = PorterStemmer()
    words = text.split(' ')

    for i, word in enumerate(words):
        stemmed_word = stemmer.stem(word)
        words[i] = stemmed_word

    return ' '.join(words)


# DATA PRE PROCESSING
# 1. Remove unecessary columns
#     necessary columns: 'movie_id', 'title', 'cast', 'crew', 'genres', 'overview', 'keywords'
# 2. check how many missing values in each column, if less, then drop those instances
# 3. drop duplicate instances
# 4. clean and extract genres from genres column
# 5. clean and extract keywords from keywords column
# 6. clean and extract to cast from cast column
# 7. extract director from crew column
# 8. convert overview to a list of words to standardize all columns as list of words
# 9. remove spaces from words in columns except overview and title 
# 10. create tags columns from crew, cast, keywords, overview, genres
# 11. convert tags to str from list
# 12 Stem each tag to its base word.


# 1
movies = movies[['movie_id', 'title', 'cast', 'crew', 'genres', 'overview', 'keywords']].copy()   # creating copy to avoid errors
# 2
movies.isnull().sum()    # checking missing values = 3 in overview column
movies.dropna(inplace=True)         # dropping instances with missing values
# 3
movies.drop_duplicates(inplace=True)
# 4
movies['genres'] = movies['genres'].apply(extract_genres_keywords)
# 5
movies['keywords'] = movies['keywords'].apply(extract_genres_keywords)
# 6
movies['cast'] = movies['cast'].apply(extract_cast)
# 7
movies['crew'] = movies['crew'].apply(extract_director)
# 8
movies['overview'] = movies['overview'].apply(text_to_words)
# 9
movies['keywords'] = movies['keywords'].apply(text_to_words)
movies['genres'] = movies['genres'].apply(text_to_words)
movies['cast'] = movies['cast'].apply(text_to_words)
movies['crew'] = movies['crew'].apply(text_to_words)
# 10
movies['tags'] = movies.apply(concatColumns_intoOne, axis=1)
movies.drop(columns_to_concat, axis=1, inplace=True)
# 11
movies['tags'] = movies['tags'].apply(list_to_str).str.lower()
# 12
movies['tags'] = movies['tags'].apply(stemming_words)


# VECTORIZATION :- Bag of Words technique
#join the tags of each movie which will result in a huge corpus of words. remove the stop words. 
#fetch most frequent n number of words in the corpus and call it most_frequent_words. 
# Count the number of times each word in most_frequent_words occurs in each movie tag. 
# This will result in a list of numbers representing 'tags' of a movie with len(list) = n, where each number is the frequency of 
#   each word in most_frequent_words occuring in tags. 
# This list is the vector representation of the movie in n-dimensions

vectorizer = CountVectorizer(max_features=5000, stop_words='english')
vectors = vectorizer.fit_transform(movies['tags']).toarray()


# SIMILARITY CALCULATIOn - using cosine similarity
# calculating distance of each movie with all other movies
# result: matrix of arrays where each array is a movie and each element of the array is the distance of that movie with all other movies

similarity_matrix = cosine_similarity(vectors)


# FETCH POSTER OF MOVIE
def get_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=faf9bc56e1efbb55d2f86f58773dfd65'.format(movie_id))
    data = response.json()

    return 'https://image.tmdb.org/t/p/w500' + data['poster_path']


# reccommend Algorithm - get the n most similar movies
def recommend(movie_name, n):
    """ fetches the titles of n most similar movies to movie_name and returns in a list
    """
    movie_name = movie_name.lower()
    movie_index = movies[movies['title'].str.lower() == movie_name].index[0]        # get index of the row in data in which title = movie_name 
    distances = similarity_matrix[movie_index]                          # get similarity array of requested movie 
    index_tracker_movies = list(enumerate(distances))              # tracing index of movies along with the similarity scores wrt requested movie
    nearest_movie_scores = sorted(index_tracker_movies, reverse=True,key=lambda x: x[1])[1:n+1]      # picking n most similar movies (excluding the requested movie itself)

    nearest_movie_indices = [movie[0] for movie in nearest_movie_scores]

    nearest_movie_titles = [movies.iloc[i].title for i in nearest_movie_indices]
    similar_movie_posters = [get_poster(movies.iloc[i].movie_id) for i in nearest_movie_indices]         # get poster for each movie

    return nearest_movie_titles, similar_movie_posters




import pickle
pickle.dump(dict(movies), open('movies_dict.pkl', 'wb'))
