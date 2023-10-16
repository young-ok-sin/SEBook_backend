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
        
        idx = next((i for i, book in enumerate(self.data) if book["title"] == user_book), None)
        
        if idx is None:
            return []
        
        # 동일한 depth3 카테고리의 책만 선택
        same_depth3_books_indices = [i for i, book in enumerate(self.data) if book["depth3"] == self.data[idx]["depth3"]]
        
        sim_scores = [(i, score) for i, score in enumerate(self.cosine_sim[idx]) if i in same_depth3_books_indices]
    
        sim_scores.sort(key=lambda x: x[1], reverse=True)
        
        # 만약 추천 가능한 도서가 없다면 빈 리스트 반환
        if not sim_scores:
            return []

        return [self.data[i[0]]['title'] for i in sim_scores[1:11]]
