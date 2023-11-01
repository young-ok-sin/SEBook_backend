import json
import networkx as nx
from sklearn.metrics.pairwise import cosine_similarity
from book.models import Book,LikeBook
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter


class BookRecommender:
    def __init__(self):
        self.data = list(Book.objects.all())  # 데이터베이스에서 책 정보를 가져옵니다.

        descriptions = [book.title for book in self.data]
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(descriptions)
        cosine_sim = cosine_similarity(tfidf_matrix)

        # Graph 생성하기: 각 Node가 책을, Edge가 유사도(cosine similarity)를 나타내게 합니다.
        self.G = nx.Graph()
        
        for i in range(len(self.data)):
            for j in range(i+1, len(self.data)):
                if self.data[i].categoryId_book.depth3 == self.data[j].categoryId_book.depth3:
                    self.G.add_edge(self.data[i].title, self.data[j].title, weight=cosine_sim[i][j])
                    
                    
    def recommend_books(self, userNum):
        like_books = LikeBook.objects.filter(userNum_like_book=userNum).order_by('-like_bookNum')
        user_books = [like_book.isbn13_like_book for like_book in like_books]
        
        if not user_books:
            # 아무 데이터나 5개 반환
            random_books = []
            for book in self.data[:5]:
                random_books.append({
                    'title': book.title,
                    'author': book.author,
                    'cover': book.cover,
                    'description': book.description
                })
            return random_books

        # 최근에 좋아요를 누른 도서와 같은 카테고리의 도서 최대 5권을 추천
        latest_book = user_books[0]
        same_category_books = Book.objects.filter(categoryId_book=latest_book.categoryId_book).exclude(isbn13=latest_book.isbn13)
        
        if len(same_category_books) > 5:
            same_category_books = same_category_books[:5]
        
        recommendations = [{
            'title': book.title,
            'author': book.author,
            'cover': book.cover,
            'description': book.description
        } for book in same_category_books]

        if len(user_books) > 1:
            # 나머지 도서들은 사용자가 좋아한 책들의 카테고리 비율에 따라 10권을 추천
            user_categories = [book.categoryId_book for book in user_books[1:]]
            category_counts = Counter(user_categories)
            total = sum(category_counts.values())
            category_ratios = {category: count / total for category, count in category_counts.items()}

            for category, ratio in category_ratios.items():
                num_books = int(ratio * 10)
                category_books = Book.objects.filter(categoryId_book=category).exclude(isbn13__in=[book.isbn13 for book in user_books])[:num_books]
                recommendations += [{
                    'title': book.title,
                    'author': book.author,
                    'cover': book.cover,
                    'description': book.description
                } for book in category_books]

        return recommendations

# class BookRecommender:
#     def __init__(self):
#         self.data = list(Book.objects.values())  # 데이터베이스에서 책 정보를 가져옵니다.

#         descriptions = [book['title'] for book in self.data]
#         vectorizer = TfidfVectorizer()
#         tfidf_matrix = vectorizer.fit_transform(descriptions)
#         cosine_sim = cosine_similarity(tfidf_matrix)

#         # Graph 생성하기: 각 Node가 책을, Edge가 유사도(cosine similarity)를 나타내게 합니다.
#         self.G = nx.Graph()
        
#         for i in range(len(self.data)):
#             for j in range(i+1, len(self.data)):
#                 if self.data[i]["depth3"] == self.data[j]["depth3"]:
#                     self.G.add_edge(self.data[i]['title'], self.data[j]['title'], weight=cosine_sim[i][j])
    # def recommend_books(self, user_book):
    #     if not user_book or not self.G.has_node(user_book):
    #         # 아무 데이터나 5개 반환
    #         random_books = []
    #         for book in self.data[:5]:
    #             random_books.append({
    #                 'title': book['title'],
    #                 'author': book['author'],
    #                 'cover': book['cover'],
    #                 'description': book['description']
    #             })
    #         return random_books
            
    #     related_books = sorted(self.G[user_book].items(), key=lambda x: x[1]['weight'], reverse=True)
        
    #     if not related_books:
    #         return []
        
    #     recommendations = []
    #     for book in related_books[:5]:
    #         for data in self.data:
    #             if data['title'] == book[0]:
    #                 recommendations.append({
    #                     'title': data['title'],
    #                     'author': data['author'],
    #                     'cover': data['cover'],
    #                     'description': data['description']
    #                 })
    #                 break
    