import pytest

from unittest.mock import MagicMock
from dao.movie import MovieDAO
from dao.model.movie import Movie
from service.movie import MovieService
from setup_db import db


@pytest.fixture
def movie_dao():
    dao = MovieDAO(db.session)

    movie1 = Movie(
        id=1,
        title='title',
        description='description1',
        trailer='trailer1',
        year='1999',
        rating=2,
        genre_id=1,
        director_id=1)
    movie2 = Movie(
        id=2,
        title='title',
        description='description2',
        trailer='trailer2',
        year='1998',
        rating=2,
        genre_id=2,
        director_id=2)
    movie3 = Movie(
        id=3,
        title='title',
        description='description3',
        trailer='trailer3',
        year='1997',
        rating=2,
        genre_id=3,
        director_id=3)

    dao.get_one = MagicMock(return_value=movie1)
    dao.get_all = MagicMock(return_value=[movie1, movie2, movie3])
    dao.create = MagicMock(return_value=Movie(id=3, title='Horror'))
    dao.update = MagicMock()
    dao.delete = MagicMock()

    return dao


class TestDirectorService:
    @pytest.fixture(autouse=True)
    def movie_service(self, movie_dao):
        self.movie_service = MovieService(dao=movie_dao)

    def test_get_one(self):
        movie = self.movie_service.get_one(1)
        assert movie is not None
        assert movie.id == 1
        assert movie.title == 'title'

    def test_get_all(self):
        movies = self.movie_service.get_all()
        assert len(movies) > 0
        assert len(movies) == 3

    def test_create(self):
        movie_data = {
            'title': 'Horror'
        }
        movie = self.movie_service.create(movie_data)
        assert movie.title == movie_data['title']

    def test_delete(self):
        movie = self.movie_service.delete(1)
        assert movie is None

    def test_update(self):
        movie_data = {'id': 3, 'title': 'Romance'}
        self.movie_service.update(movie_data)
