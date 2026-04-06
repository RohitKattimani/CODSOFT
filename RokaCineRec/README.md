# Enterprise Content-Based Recommendation System

A lightweight, high-performance recommendation engine built with Python, Flask, and Scikit-Learn. It utilizes TF-IDF vectorization and Cosine Similarity to analyze textual features (genres and plot descriptions) to surface highly correlated media items.

## Tech Stack
* **Backend:** Python (Flask)
* **Machine Learning:** Scikit-Learn (TF-IDF, Cosine Similarity), Pandas
* **Frontend:** Vanilla JS, HTML/CSS (Corporate Minimalist Design)
* **Deployment:** Vercel (Serverless Functions)

## Local Setup
1. Clone the repository and navigate to the folder.
2. Install dependencies: `pip install -r requirements.txt`
3. Execute the server: `uvicorn main:app --reload --port 8000`
4. Access via ` http://127.0.0.1:8000`

## How the Algorithm Works
Instead of relying on user history matrices (Collaborative Filtering), this system relies entirely on item metadata (Content-Based Filtering). It converts movie descriptions into a mathematical matrix of word frequencies, penalizing overly common words (TF-IDF). It then calculates the geometric angle between these movie vectors in multi-dimensional space (Cosine Similarity) to determine which movies are "closest" to one another.
