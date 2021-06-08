class ElasticsearchDAO:
    def __init__(self, es):
        self.es = es
        self.index = "book"

    def get_book(self, book_id):
        body = {"_source": ["title", "author", "genre", "description", "avg_rating", "publish_date"],
                "query": {"ids": {"values": [book_id]}}}
        return self.es.search(index=self.index, body=body)

    def exists(self, book_id):
        id = book_id
        return self.es.exists(index=self.index, id=id)

    def search(self, processed_input):
        body = {"from": 0, "size": 10,
                "min_score": 0.5,
                "_source": ["title", "author", "genre", "publish_date", "avg_rating"],
                "query": {
                    "bool": {
                        "should": [
                            {"nested": {
                                "path": "reviews",
                                "query": {"query_string": {
                                    "query": processed_input['no_stopword_str'],
                                    "fields": ["reviews.review"]
                                }}
                            }},
                            {"query_string": {
                                "query": processed_input['person_str'],
                                "fields": ["author"]
                            }},
                            {"query_string": {
                                "query": processed_input['date_str'],
                                "fields": ["date"]
                            }},
                            {"query_string": {
                                "query": processed_input['title_str'],
                                "fields": ["title"]
                            }},
                            {"query_string": {
                                "query": processed_input['genre_str'],
                                "fields": ["genre"]
                            }}
                        ]
                    }
                }
                }
        return self.es.search(index=self.index, body=body)

    # search again with keywords as filters
    def search_again(self, processed_input, keywords):
        body = {"from": 0, "size": 10,
                "min_score": 0.5,
                "_source": ["title", "author", "genre", "publish_date", "avg_rating"],
                "query": {
                    "bool": {
                        "should": [
                            {"nested": {
                                "path": "reviews",
                                "query": {"query_string": {
                                    "query": processed_input['no_stopword_str'],
                                    "fields": ["reviews.review"]
                                }}
                            }},
                            {"query_string": {
                                "query": processed_input['person_str'],
                                "fields": ["author"]
                            }},
                            {"query_string": {
                                "query": processed_input['date_str'],
                                "fields": ["date"]
                            }},
                            {"query_string": {
                                "query": processed_input['title_str'],
                                "fields": ["title"]
                            }},
                            {"query_string": {
                                "query": "(" + processed_input['genre_str'] + ")^3",
                                "fields": ["genre"]
                            }}
                        ]
                    }
                },
                "post_filter": {
                        "bool": {
                            "must": [
                                {"multi_match": {
                                    "query": keywords,
                                    "fields": ["*"],
                                    "operator": "and"
                                }}
                            ]
                        }

                }
                }
        return self.es.search(index=self.index, body=body)
