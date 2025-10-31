# Viendo: Content-Based Movie Recommender System
**[Demo Viendo](https://viendo-movie-recommender-bnulati3xkdeugqxvl6rhe.streamlit.app/)** (Might need to wait till the app builds).

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
2.  **Install Dependencies:**
```bash
    pip install -r requirements.txt
```
3.  **Data Preparation (Crucial Step):**
- The `model.py` script needs to run once to process the CSV data, calculate the similarity matrix, and generate the required `movies_dict.pkl` file.
```bash
python model.py
```

---
## ▶️ Usage
To launch the Streamlit web application, run the following command in your terminal:
```bash
streamlit run app.py




