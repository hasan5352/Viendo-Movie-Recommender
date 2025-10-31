# Viendo: A Machine Learning Movie Recommender 
- **[Access Viendo here](https://viendo-movie-recommender-bnulati3xkdeugqxvl6rhe.streamlit.app/)**
  - You might need to wait till the app builds since this is a demonstration of the recommendation model and hence the web app might not be stable. 
- Built using the Pandas, NLTK and Scikit-Learn. Deployed utilising Streamlit and Pickle libraries from python.
- All the data that the model operates on is textual.
- **model.py** contains the code of the recommendation system. **app.py** contains the code for deployment of the system on a streamlit website.
  ### The Process:
  1. Collected datasets from a specified directory and transformed them into pandas DataFrames.
  2. Combined dataframes and important features, cleaned the data and stemmed the combined important features.
  3. Used the Bag of Words technique for vectorization of instances (movies) into 5000-dimensions
  4. Generated a similarity matrix with cosine of the angle of each movie (represented as a vector) to every other movie. Each array in vector represents a movie.
  - The distance metric used to calculate the similarity between the movies is cosine similarity
  5. Implemented a recommendation algorithm to suggest the most similar movies based on a given movie name


## ⚙️ Installation and Setup

This project requires Python 3.9+ and the listed libraries in `requirements.txt`.
