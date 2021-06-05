class ElasticsearchDAO:
    def __init__(self, es):
        self.es = es
        self.index = "book"

    def get_book(self, book_id):
        body = {"_source": ["title", "author", "genre", "description", "avg_rating", "publish_date"],
                "query": {"term": {"book_id": book_id}}}
        return self.es.search(index=self.index, body=body)

    def exists(self, book_id):
        id = book_id
        return self.es.exists(index=self.index, id=id)

    def search(self, user_input):
        body = {"_source": ["title", "author", "genre", "avg_rating", "publish_date"],
                "query": {"multi_match": {"query": user_input, "fields": ["*"]}}}
        return self.es.search(index=self.index, body=body)
