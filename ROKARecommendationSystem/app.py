from flask import Flask, render_template, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

app = Flask(__name__)

# Sample Dataset: Easily expandable
movies_data = [
    {"id": 1, "title": "The Matrix", "description": "A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.", "genre": "Action, Sci-Fi"},
    {"id": 2, "title": "Inception", "description": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.", "genre": "Action, Sci-Fi"},
    {"id": 3, "title": "Interstellar", "description": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.", "genre": "Adventure, Drama, Sci-Fi"},
    {"id": 4, "title": "The Dark Knight", "description": "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.", "genre": "Action, Crime, Drama"},
    {"id": 5, "title": "Pulp Fiction", "description": "The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.", "genre": "Crime, Drama"},
    {"id": 6, "title": "Fight Club", "description": "An insomniac office worker and a devil-may-care soap maker form an underground fight club that evolves into much more.", "genre": "Drama"},
    {"id": 7, "title": "The Social Network", "description": "As Harvard student Mark Zuckerberg creates the social networking site that would become known as Facebook, he is sued by the twins who claimed he stole their idea.", "genre": "Biography, Drama"},
    {"id": 8, "title": "Steve Jobs", "description": "Takes us behind the scenes of the digital revolution, to paint a portrait of the man at its epicenter.", "genre": "Biography, Drama"}
]

df = pd.DataFrame(movies_data)
# Combine genre and description for better context matching
df['combined_features'] = df['genre'] + " " + df['description']

# Initialize TF-IDF and calculate the similarity matrix
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['combined_features'])
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

def get_recommendations(title, cosine_sim=cosine_sim):
    try:
        # Get the index of the movie that matches the title
        idx = df.index[df['title'].str.lower() == title.lower()].tolist()[0]
        
        # Get pairwise similarity scores
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        # Get the scores of the 3 most similar movies (excluding itself)
        sim_scores = sim_scores[1:4]
        movie_indices = [i[0] for i in sim_scores]
        
        return df.iloc[movie_indices][['title', 'genre', 'description']].to_dict('records')
    except IndexError:
        return []

@app.route('/')
def index():
    # Pass the list of titles to populate the frontend dropdown
    titles = df['title'].tolist()
    return render_template('index.html', titles=titles)

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    movie_title = data.get('movie')
    recommendations = get_recommendations(movie_title)
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True)
else:
    app = app
