class BookshelfService:
    def __init__(self, bookshelf_dao):
        self.bookshelf_dao = bookshelf_dao

    def get_bookshelf(self, user_id):
        return self.bookshelf_dao.get_bookshelf(user_id)

    def put_to_bookshelf(self, user_id, book_id):
        if self.bookshelf_dao.is_in_bookshelf(user_id, book_id):
            return f"book_id {book_id} already exists in {user_id} bookshelf", 409
        self.bookshelf_dao.insert_book(user_id, book_id)
        return f"book_id {book_id} put to {user_id} bookshelf", 200

    def delete_from_bookshelf(self, user_id, book_id):
        self.bookshelf_dao.delete_book(user_id, book_id)
