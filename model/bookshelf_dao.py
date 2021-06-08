class BookshelfDAO:
    def __init__(self, model, db):
        self.model = model
        self.db = db

    def get_bookshelf(self, user_id):
        book_list_obj = self.model.query.filter_by(user_id=user_id).all()
        book_list = [(row.book_id, row.book_title) for row in book_list_obj]
        return book_list

    def insert_book(self, user_id, book_id, book_title):
        bookshelf = self.model(user_id=user_id, book_id=book_id, book_title=book_title)
        self.db.session.add(bookshelf)
        self.db.session.commit()

    def is_in_bookshelf(self, user_id, book_id):
        book = self.model.query.filter_by(user_id=user_id).filter_by(book_id=book_id).first()
        return True if book else False

    def delete_book(self, user_id, book_id):
        book = self.model.query.filter_by(user_id=user_id).filter_by(book_id=book_id).first()
        self.db.session.delete(book)
        self.db.session.commit()
