class ElasticsearchService:
    def __init__(self, elasticsearch_dao):
        self.elasticsearch_dao = elasticsearch_dao

    def get_book_by_id(self, book_id):
        if self.elasticsearch_dao.exists(book_id):
            return self.elasticsearch_dao.get_book(book_id)
        return f"book_id {book_id} does not exist", 404

    def search(self, user_input):
        return self.elasticsearch_dao.search(user_input)