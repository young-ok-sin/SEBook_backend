import json
import networkx as nx
from sklearn.metrics.pairwise import cosine_similarity
from book.models import Book, LikeBook, Category
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter
import numpy as np
import random
import matplotlib.pyplot as plt


class BookRecommender:
    def __init__(self):
        self.data = list(Book.objects.select_related('categoryId_book').all())
        self.G = None

    def recommend_randomBooks(self):
        random_books = random.choices(self.data, k=5)
        random_books = [{
            'title': book.title,
            'author': book.author,
            'cover': book.cover,
            'description': book.description,
            'categoryId': book.categoryId_book.categoryId,
            'isbn13': book.isbn13,
            'num_likes': book.num_likes
        } for book in random_books]
        return random_books
    
    def recommend_books(self, userNum=None):
        if userNum is None:
            return self.recommend_randomBooks()
    
    def recommend_books(self, userNum):
        like_books = LikeBook.objects.filter(userNum_like_book=userNum).order_by('-like_bookNum')
        user_books = [like_book.isbn13_like_book for like_book in like_books]
        user_books_isbn13 = [book.isbn13 for book in user_books]

        if not user_books:
            return self.recommend_randomBooks()

        latest_book = user_books[0]
        same_category_books = list(Book.objects.filter(categoryId_book=latest_book.categoryId_book).exclude(isbn13__in=user_books_isbn13))

        descriptions = [f"{latest_book.title} {latest_book.author} {latest_book.description}" for _ in same_category_books] 
        descriptions += [f"{book.title} {book.author} {book.description}" for book in same_category_books]

        likes_dict = {book.isbn13: book.num_likes for book in same_category_books}

        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(descriptions)
        cosine_sim = cosine_similarity(tfidf_matrix)

        self.G = nx.Graph()
        for i in range(len(same_category_books)):
            if same_category_books[i].isbn13 != latest_book.isbn13:
                weight = cosine_sim[i][0] + 0.1 * np.log(likes_dict[same_category_books[i].isbn13] + 1)
                self.G.add_edge(latest_book.isbn13, same_category_books[i].isbn13, weight=weight)

        edges = sorted(self.G.edges(data=True), key=lambda x: (x[2]['weight'], x[1]), reverse=True)  # 가중치와 isbn13으로 정렬
        recommended_books_isbn13 = []
        for edge in edges:
            if edge[1] not in recommended_books_isbn13:
                recommended_books_isbn13.append(edge[1])
            if len(recommended_books_isbn13) >= 5:
                break
        
        # 그래프 그리기
        # plt.figure(figsize=(10, 10))
        # pos = nx.spring_layout(self.G)
        # nx.draw(self.G, pos, with_labels=True, node_size=5000, font_size=10)
        # edge_labels = nx.get_edge_attributes(self.G, 'weight')
        # nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edge_labels, font_size=8)

        # 그래프 출력
        # plt.show()
        
        if len(user_books) > 1:
            user_categories = [book.categoryId_book for book in user_books[1:]]
            category_counts = Counter(user_categories)
            total = sum(category_counts.values())
            category_ratios = {category: count / total for category, count in category_counts.items()}
            final_list = []
            for category, ratio in sorted(category_ratios.items(), key=lambda item: item[1], reverse=True):
                num_books = int(ratio * (15 - len(recommended_books_isbn13)))
                category_books = Book.objects.filter(categoryId_book=category).exclude(isbn13__in=user_books_isbn13 + recommended_books_isbn13)[:num_books]
                final_list.extend([book.isbn13 for book in category_books])  # 각 도서의 isbn13을 리스트에 추가
                if len(recommended_books_isbn13+final_list) >= 15:
                    break
                    
        recommended_books_isbn13 = recommended_books_isbn13 + final_list
        recommended_books = []
        for isbn13 in recommended_books_isbn13:
            book = Book.objects.get(isbn13=isbn13)  # get 메서드를 사용하여 각 ISBN13에 해당하는 도서를 검색
            recommended_books.append(book)

        recommendations = [{
            'title': book.title,
            'author': book.author,
            'cover': book.cover,
            'description': book.description,
            'categoryId': book.categoryId_book.categoryId,
            'isbn13': book.isbn13,
            'num_likes': book.num_likes
        } for book in recommended_books]

        if not recommendations:
            return self.recommend_randomBooks()
        return recommendations[:15]