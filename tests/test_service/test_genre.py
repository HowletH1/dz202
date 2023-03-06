import pytest

from unittest.mock import MagicMock
from dao.genre import GenreDAO
from dao.model.genre import Genre
from service.genre import GenreService
from setup_db import db


@pytest.fixture
def genre_dao():
    dao = GenreDAO(db.session)

    action = Genre(id=1, name='action')
    comedy = Genre(id=2, name='comedy')
    thriller = Genre(id=3, name='thriller')

    dao.get_one = MagicMock(return_value=action)
    dao.get_all = MagicMock(return_value=[action, comedy, thriller])
    dao.create = MagicMock(return_value=Genre(id=3, name='Horror'))
    dao.update = MagicMock()
    dao.delete = MagicMock()

    return dao


class TestDirectorService:
    @pytest.fixture(autouse=True)
    def genre_service(self, genre_dao):
        self.genre_service = GenreService(dao=genre_dao)

    def test_get_one(self):
        genre = self.genre_service.get_one(1)
        assert genre is not None
        assert genre.id == 1

    def test_get_all(self):
        genres = self.genre_service.get_all()
        assert len(genres) > 0
        assert len(genres) == 3

    def test_create(self):
        genre_data = {
            'name': 'Horror'
        }
        genre = self.genre_service.create(genre_data)
        assert genre.name == genre_data['name']

    def test_delete(self):
        genre = self.genre_service.delete(1)
        assert genre is None

    def test_update(self):
        genre_data = {'id': 3, 'name': 'Romance'}
        self.genre_service.update(genre_data)
