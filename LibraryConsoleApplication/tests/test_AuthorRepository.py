from DataAccess.AuthorRepository import AuthorRepository
import unittest
from Exceptions.Exceptions import RepositoryMethodNotAllowedError

from Models.Models import AuthorModel, UserType, UserWithoutPasswordViewModel


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


        