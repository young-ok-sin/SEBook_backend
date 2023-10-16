import json
import networkx as nx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class BookRecommender:
    def __init__(self):
        with open('/content/drive/MyDrive/dataset/testData.json', 'r') as f:
            self.data = json.load(f)

        self.G = nx.Graph()

        for book in self.data:
            self.G.add_node(book['title'], category=book['depth3'])

        for book1 in self.data:
            for book2 in self.data:
                if book1 != book2 and book1['depth3'] == book2['depth3']:
                    self.G.add_edge(book1['title'], book2['title'])

        descriptions = [book['title'] for book in self.data]
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(descriptions)
        self.cosine_sim = cosine_similarity(tfidf_matrix)

    def recommend_books(self, user_book):
        
        idx = next(i for i, book in enumerate(self.data) if book["title"] == user_book)
        
        sim_scores = list(enumerate(self.cosine_sim[idx]))
        sim_scores.sort(key=lambda x: x[1], reverse=True)
        
        return [self.data[i[0]]['title'] for i in sim_scores[1:11]]