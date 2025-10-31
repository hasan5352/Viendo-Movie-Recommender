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

### Prerequisites
* An API key from The Movie Database (TMDB).
* The `data` folder containing the necessary CSV files.

### Steps
1.  **Clone the Repository:**
```bash
    git clone https://github.com/hasan5352/Viendo-Movie-Recommender.git
    cd Viendo-Movie-Recommender
```
2.  **Verify `requirements.txt`:**
3.  **Install Dependencies:**
```bash
    pip install -r requirements.txt
```
4.  **Data Preparation (Crucial Step):**
- The `model.py` script needs to run once to process the CSV data, calculate the similarity matrix, and generate the required `movies_dict.pkl` file.
```bash
python model.py
```


---

## ▶️ Usage

To launch the Streamlit web application, run the following command in your terminal:

```bash
streamlit run app.py




