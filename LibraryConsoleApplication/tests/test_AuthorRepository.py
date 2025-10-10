from DataAccess.AuthorRepository import AuthorRepository
import unittest
from Exceptions.Exceptions import RepositoryMethodNotAllowedError

from Models.Models import AuthorModel


class TestAuthorRepository(unittest.TestCase):
    
    def setUp(self) -> None:
        self.cursor = AuthorRepository._get_cursor()
        
    def tearDown(self) -> None:
        self.cursor.connection.rollback()
        self.cursor.connection.close()
        
    def rollback(self) -> None:
        self.cursor.connection.rollback()
        
    # ─────────────────────────────── Tests ───────────────────────────────
        
    def test_forbidden_methods(self):
        model = AuthorModel(name = 'احمد')
        
        with self.assertRaises(RepositoryMethodNotAllowedError):
            AuthorRepository.remove(model, cursor = self.cursor)
        with self.assertRaises(RepositoryMethodNotAllowedError):
            AuthorRepository.clear(cursor = self.cursor)
        
    def test_get_one(self):
        model = AuthorModel(name = 'احمد شاملو')
        
        db_model = AuthorRepository.get_one(model, cursor = self.cursor)
        
        expected_model = AuthorModel(
            id = 1,
            name = 'احمد شاملو',
            biography= 'شاعر، نویسنده و مترجم ایرانی که به عنوان یکی از تأثیرگذارترین شاعران معاصر شناخته می‌شود.'
        )
        
        self.assertEqual(db_model, expected_model)


        