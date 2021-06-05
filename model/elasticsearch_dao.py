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

    def search(self, processed_input_list):
        body = {"from": 0, "size": 20,
                "min_score": 0.5,
                "_source": ["title", "author", "genre", "publish_date", "avg_rating"],
                "query": {
                    "bool": {
                        "should": [
                            {"nested": {
                                "path": "reviews",
                                "query": {"match": {"reviews.review": processed_input_list[0]}}
                            }},
                            {"match": {"author": processed_input_list[1]}},
                            {"match": {"date": processed_input_list[2]}},
                            {"match": {"title": processed_input_list[3]}},
                            {"match": {"genre": processed_input_list[4]}}
                        ]
                    }
                }
                }
        return self.es.search(index=self.index, body=body)
