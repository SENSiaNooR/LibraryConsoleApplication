from DataAccess.AuthorRepository import AuthorRepository
import unittest
import Exceptions
from Exceptions.Exceptions import RepositoryMethodNotAllowedError

from Models.Models import AuthorModel


class TestAuthorRepository(unittest.TestCase):
    
    def setUp(self) -> None:
        self.cursor = AuthorRepository._get_cursor()
        
    def tearDown(self) -> None:
        self.cursor.connection.rollback()
        self.cursor.connection.close()
        
    def test_forbidden_methods(self):
        model = AuthorModel(name = 'احمد')
        
        with self.assertRaises(RepositoryMethodNotAllowedError, AuthorRepository.remove(model, cursor = self.cursor)):
            pass 
        with self.assertRaises(RepositoryMethodNotAllowedError, AuthorRepository.clear(cursor = self.cursor)):
            pass   
        
    def test_get_one(self):
        model = AuthorModel(name = 'احمد شاملو')
        
        db_model = AuthorRepository.get_one(model, cursor = self.cursor)
        
        expected_model = AuthorModel(
            id = 1,
            name = 'احمد شاملو',
            biography= 'شاعر، نویسنده و مترجم ایرانی که به عنوان یکی از تأثیرگذارترین شاعران معاصر شناخته می‌شود.'
        )
        
        self.assertEqual(db_model, expected_model)



if __name__ == '__main__':
    unittest.main()
        