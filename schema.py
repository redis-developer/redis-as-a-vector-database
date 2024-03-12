schema = {
    "index": {
        "name": "book_index",
        "prefix": "book",
        "storage_type": "json",
    },
    "fields": {
        "tag": [
            {"name": "id"},
            {"name": "$.editions[*]", "as_name" : "editions"},
            {"name": "$.genres[*]", "as_name" : "genres"},
        ],
        "text": [
            {"name": "author"},
            {"name": "description"},
            {"name": "title"},
        ],
        "numeric": [
            {"name": "pages"},
            {"name": "$.year_published", "as_name": "year_published"},
            {"name": "$.votes", "as_name" : "votes"},
            {"name": "$.score", "as_name" : "score"}
        ],
        "vector": [{
            "name": "embedding",
            "as_name": "embedding",
            "dims": 384,
            "distance_metric": "cosine",
            "algorithm": "flat",
            "datatype": "float32"
        }]
    },
}
        