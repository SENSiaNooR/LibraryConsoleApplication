from Models import AuthorModel
from BaseRepository import BaseRepository
from BaseRepository import map_to_model

class AuthorRepository(BaseRepository):

    @map_to_model(AuthorModel)
    def get_all_authors(self):
        query = "SELECT * FROM \"Author\""
        with self.get_cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()


if __name__ == '__main__':
    ar = AuthorRepository()
    a = ar.get_all_authors()
    for item in a:
        print(item)