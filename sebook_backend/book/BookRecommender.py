import json
import networkx as nx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from book.models import Book
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class BookRecommender:
    def __init__(self):
        self.data = list(Book.objects.values())  # 데이터베이스에서 책 정보를 가져옵니다.

        descriptions = [book['title'] for book in self.data]
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(descriptions)
        self.cosine_sim = cosine_similarity(tfidf_matrix)

    def recommend_books(self, user_book):
        
        idx = next(i for i, book in enumerate(self.data) if book["title"] == user_book)
        
        if idx is None:
            return []
        
        sim_scores = list(enumerate(self.cosine_sim[idx]))
        sim_scores.sort(key=lambda x: x[1], reverse=True)
        
        return [self.data[i[0]]['title'] for i in sim_scores[1:11]]
