import pytest
from main import BooksCollector

class TestBooksCollector:

    def test_add_new_book_add_two_books(self):
        collector = BooksCollector()

        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')

        assert len(collector.get_books_genre()) == 2

    @pytest.mark.parametrize('book_name', [
        '',
        'Книга с названием длиннее сорока символов, что недопустимо по условию'
    ])
    def test_add_new_book_with_invalid_name_not_added(self, book_name):
        collector = BooksCollector()
        
        collector.add_new_book(book_name)
        
        assert book_name not in collector.get_books_genre()

    def test_add_new_book_duplicate_not_added(self):
        collector = BooksCollector()
        book_name = 'Дюна'
        
        collector.add_new_book(book_name)
        collector.add_new_book(book_name)
        
        assert len(collector.get_books_genre()) == 1

    def test_set_book_genre(self):
        collector = BooksCollector()
        book_name = 'Дюна'
        genre = 'Фантастика'
        
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, genre)
        
        assert collector.get_book_genre(book_name) == genre

    def test_set_book_genre_invalid_genre_not_set(self):
        collector = BooksCollector()
        book_name = 'Дюна'
        invalid_genre = 'Роман'
        
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, invalid_genre)
        
        assert collector.get_book_genre(book_name) == ''

    def test_get_books_with_specific_genre(self):
        collector = BooksCollector()
        
        collector.add_new_book('Дюна')
        collector.add_new_book('Властелин колец')
        collector.add_new_book('Оно')
        
        collector.set_book_genre('Дюна', 'Фантастика')
        collector.set_book_genre('Властелин колец', 'Фантастика')
        collector.set_book_genre('Оно', 'Ужасы')
        
        fantasy_books = collector.get_books_with_specific_genre('Фантастика')
        
        assert len(fantasy_books) == 2
        assert 'Дюна' in fantasy_books
        assert 'Властелин колец' in fantasy_books
        assert 'Оно' not in fantasy_books

    def test_get_books_for_children_excludes_age_rating(self):
        collector = BooksCollector()
        
        collector.add_new_book('Дюна')
        collector.add_new_book('Оно')
        collector.add_new_book('Винни Пух')
        
        collector.set_book_genre('Дюна', 'Фантастика')
        collector.set_book_genre('Оно', 'Ужасы')
        collector.set_book_genre('Винни Пух', 'Мультфильмы')
        
        children_books = collector.get_books_for_children()
        
        assert 'Дюна' in children_books
        assert 'Винни Пух' in children_books
        assert 'Оно' not in children_books
        assert len(children_books) == 2

    def test_add_and_delete_book_in_favorites(self):
        collector = BooksCollector()
        book_name = 'Дюна'
        
        collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)
        
        assert book_name in collector.get_list_of_favorites_books()
        assert len(collector.get_list_of_favorites_books()) == 1
        
        collector.delete_book_from_favorites(book_name)
        
        assert book_name not in collector.get_list_of_favorites_books()
        assert len(collector.get_list_of_favorites_books()) == 0

    def test_get_books_genre_returns_correct_dict(self):
        collector = BooksCollector()
        
        collector.add_new_book('Дюна')
        collector.add_new_book('Властелин колец')
        
        collector.set_book_genre('Дюна', 'Фантастика')
        
        books_genre = collector.get_books_genre()
        
        assert isinstance(books_genre, dict)
        assert len(books_genre) == 2
        assert books_genre['Дюна'] == 'Фантастика'
        assert books_genre['Властелин колец'] == ''

    def test_get_book_genre_scenarios(self):
        collector = BooksCollector()
        
        collector.add_new_book('Дюна')
        collector.set_book_genre('Дюна', 'Фантастика')
        collector.add_new_book('Винни Пух')
        
        assert collector.get_book_genre('Дюна') == 'Фантастика'
        assert collector.get_book_genre('Винни Пух') == ''
        assert collector.get_book_genre('Несуществующая книга') is None
