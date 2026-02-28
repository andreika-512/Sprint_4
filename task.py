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

    def test_add_book_in_favorites(self):
        collector = BooksCollector()
        book_name = 'Дюна'
        
        collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)
        
        assert book_name in collector.get_list_of_favorites_books()
        assert len(collector.get_list_of_favorites_books()) == 1

    def test_delete_book_from_favorites(self):
        collector = BooksCollector()
        book_name = 'Дюна'
        
        collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)
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

    def test_get_book_genre_for_existing_book_with_genre(self):
        collector = BooksCollector()
        book_name = 'Дюна'
        
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, 'Фантастика')
        
        genre = collector.get_book_genre(book_name)
        
        assert genre == 'Фантастика'

    def test_get_book_genre_for_existing_book_without_genre(self):
        collector = BooksCollector()
        book_name = 'Дюна'
        
        collector.add_new_book(book_name)
        
        genre = collector.get_book_genre(book_name)
        
        assert genre == ''

    def test_get_book_genre_for_nonexistent_book(self):
        collector = BooksCollector()
        
        genre = collector.get_book_genre('Несуществующая книга')
        
        assert genre is None

    def test_get_book_genre_after_genre_change(self):
        collector = BooksCollector()
        book_name = 'Дюна'
        
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, 'Фантастика')
        collector.set_book_genre(book_name, 'Ужасы')
        
        genre = collector.get_book_genre(book_name)
        
        assert genre == 'Ужасы'

    def test_get_list_of_favorites_books_returns_empty_list_initially(self):
        collector = BooksCollector()
        
        favorites = collector.get_list_of_favorites_books()
        
        assert isinstance(favorites, list)
        assert len(favorites) == 0

    def test_get_list_of_favorites_books_returns_correct_books(self):
        collector = BooksCollector()
        
        collector.add_new_book('Дюна')
        collector.add_new_book('Властелин колец')
        collector.add_new_book('Оно')
        
        collector.add_book_in_favorites('Дюна')
        collector.add_book_in_favorites('Властелин колец')
        
        favorites = collector.get_list_of_favorites_books()
        
        assert len(favorites) == 2
        assert 'Дюна' in favorites
        assert 'Властелин колец' in favorites
        assert 'Оно' not in favorites

    def test_get_list_of_favorites_books_after_removing_from_favorites(self):
        collector = BooksCollector()
        
        collector.add_new_book('Дюна')
        collector.add_book_in_favorites('Дюна')
        collector.delete_book_from_favorites('Дюна')
        
        favorites = collector.get_list_of_favorites_books()
        
        assert len(favorites) == 0

    def test_get_list_of_favorites_books_with_duplicate_additions(self):
        collector = BooksCollector()
        book_name = 'Дюна'
        
        collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)
        collector.add_book_in_favorites(book_name)
        
        favorites = collector.get_list_of_favorites_books()
        
        assert len(favorites) == 1
        assert book_name in favorites

    def test_get_books_genre_returns_empty_dict_initially(self):
        collector = BooksCollector()
        
        books_genre = collector.get_books_genre()
        
        assert isinstance(books_genre, dict)
        assert len(books_genre) == 0

    def test_get_books_genre_after_adding_books(self):
        collector = BooksCollector()
        
        collector.add_new_book('Дюна')
        collector.add_new_book('Властелин колец')
        
        books_genre = collector.get_books_genre()
        
        assert len(books_genre) == 2
        assert 'Дюна' in books_genre
        assert 'Властелин колец' in books_genre

    def test_get_books_genre_with_multiple_genres(self):
        collector = BooksCollector()
        
        collector.add_new_book('Дюна')
        collector.add_new_book('Властелин колец')
        collector.add_new_book('Оно')
        
        collector.set_book_genre('Дюна', 'Фантастика')
        collector.set_book_genre('Властелин колец', 'Фантастика')
        collector.set_book_genre('Оно', 'Ужасы')
        
        books_genre = collector.get_books_genre()
        
        assert books_genre['Дюна'] == 'Фантастика'
        assert books_genre['Властелин колец'] == 'Фантастика'
        assert books_genre['Оно'] == 'Ужасы'

    def test_get_books_genre_immutability(self):
        collector = BooksCollector()
        
        collector.add_new_book('Дюна')
        collector.set_book_genre('Дюна', 'Фантастика')
        
        books_genre = collector.get_books_genre()
        books_genre['Дюна'] = 'Ужасы'
        
        assert collector.get_book_genre('Дюна') == 'Фантастика'
