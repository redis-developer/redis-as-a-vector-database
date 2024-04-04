schema = {
    "index": {
        "name": "book_index",
        "prefix": "book",
        "storage_type": "json",
    },
    "fields": [
        {"name": "id", "type": "tag"},
        {"name": "editions", "type": "tag", "path": "$.editions[*]"},
        {"name": "genres", "type": "tag", "path": "$.genres[*]"},
        {"name": "author", "type": "text"},
        {"name": "description", "type": "text"},
        {"name": "title", "type": "text"},
        {"name": "pages", "type": "numeric"},
        {"name": "year_published", "type": "numeric"},
        {"name": "votes", "type": "numeric"},
        {"name": "score", "type": "numeric"},
        {
            "name": "embedding",
            "type": "vector",
            "attrs": {
                "dims": 384,
                "distance_metric": "cosine",
                "algorithm": "flat",
                "datatype": "float32",
            },
        },
    ],
}
