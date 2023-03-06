import pytest

from unittest.mock import MagicMock
from dao.director import GenreDAO
from dao.model.director import Genre
from service.director import DirectorService
from setup_db import db


@pytest.fixture
def directors_dao():
    dao = GenreDAO(db.session)

    john = Genre(id=1, name='john')
    oliver = Genre(id=2, name='oliver')
    wick = Genre(id=3, name='wick')

    dao.get_one = MagicMock(return_value=john)
    dao.get_all = MagicMock(return_value=[john, oliver, wick])
    dao.create = MagicMock(return_value=Genre(id=3, name='john'))
    dao.update = MagicMock()
    dao.delete = MagicMock()

    return dao


class TestDirectorService:
    @pytest.fixture(autouse=True)
    def directors_service(self, directors_dao):
        self.directors_service = DirectorService(dao=directors_dao)

    def test_get_one(self):
        director = self.directors_service.get_one(1)
        assert director is not None
        assert director.id == 1

    def test_get_all(self):
        directors = self.directors_service.get_all()
        assert len(directors) > 0
        assert len(directors) == 3

    def test_create(self):
        directors_data = {
            'name': 'john'
        }
        director = self.directors_service.create(directors_data)
        assert director.name == directors_data['name']

    def test_delete(self):
        director = self.directors_service.delete(1)
        assert director is None

    def test_update(self):
        director_data = {'id': 3, 'name': 'Dio'}
        self.directors_service.update(director_data)
