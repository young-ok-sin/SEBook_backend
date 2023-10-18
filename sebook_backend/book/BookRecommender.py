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
    # def recommend_books(self, user_book):
        
    #     if not self.G.has_node(user_book):
    #         return []
            
    #     # 해당 Node와 연결된 Edge들 중 Weight(cosine similarity)가 가장 높은 Node들 선택하기.
    #     related_books = sorted(self.G[user_book].items(), key=lambda x: x[1]['weight'], reverse=True)
        
    #     # 만약 추천 가능한 도서가 없다면 빈 리스트 반환
    #     if not related_books:
    #         return []
        
    #     return [book[0] for book in related_books[:5]]

    
# class BookRecommender:
#     def __init__(self):
#         self.data = list(Book.objects.values())  # 데이터베이스에서 책 정보를 가져옵니다.

#         descriptions = [book['title'] for book in self.data]
#         vectorizer = TfidfVectorizer()
#         tfidf_matrix = vectorizer.fit_transform(descriptions)
#         self.cosine_sim = cosine_similarity(tfidf_matrix)

#     def recommend_books(self, user_book):
        
#         idx = next((i for i, book in enumerate(self.data) if book["title"] == user_book), None)
        
#         if idx is None:
#             return []
        
#         # 동일한 depth3 카테고리의 책만 선택
#         same_depth3_books_indices = [i for i, book in enumerate(self.data) if book["depth3"] == self.data[idx]["depth3"]]
        
#         sim_scores = [(i, score) for i, score in enumerate(self.cosine_sim[idx]) if i in same_depth3_books_indices]
    
#         sim_scores.sort(key=lambda x: x[1], reverse=True)
        
#         # 만약 추천 가능한 도서가 없다면 빈 리스트 반환
#         if not sim_scores:
#             return []

#         return [self.data[i[0]]['title'] for i in sim_scores[1:11]]
