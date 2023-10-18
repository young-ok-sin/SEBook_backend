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
        cosine_sim = cosine_similarity(tfidf_matrix)

        # Graph 생성하기: 각 Node가 책을, Edge가 유사도(cosine similarity)를 나타내게 합니다.
        self.G = nx.Graph()
        
        for i in range(len(self.data)):
            for j in range(i+1, len(self.data)):
                if self.data[i]["depth3"] == self.data[j]["depth3"]:
                    self.G.add_edge(self.data[i]['title'], self.data[j]['title'], weight=cosine_sim[i][j])
    def recommend_books(self, user_book):
            
            if not self.G.has_node(user_book):
                return []
                
            related_books = sorted(self.G[user_book].items(), key=lambda x: x[1]['weight'], reverse=True)
            
            if not related_books:
                return []
            
            # title만 반환하는 대신 title, author, cover, description을 포함한 딕셔너리를 반환합니다.
            recommendations = []
            for book in related_books[:5]:
                for data in self.data:
                    if data['title'] == book[0]:
                        recommendations.append({
                            'title': data['title'],
                            'author': data['author'],
                            'cover': data['cover'],
                            'description': data['description']
                        })
                        break
            return recommendations
