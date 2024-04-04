# Redis as a Vector Database
This repository mirrors the content delivered in the Redis as a Vector Database Explainer Video.

**science_fiction_books**: contains approximately 11,000 book json objects that will be added and indexed in a Redis Database

Sample JSON object:
```json
  {
    "title": "Ready Player One",
    "author": "Ernest Cline",
    "score": 4.25,
    "votes": 904565,
    "description": "IN THE YEAR 2044, reality is an ugly place...",
    "year_published": 2011,
    "url": "https://www.goodreads.com/book/show/9969571-ready-player-one",
    "genres": [
      "Science Fiction",
      "Fiction",
      "Young Adult",
    ],
    "editions": [
      "English",
      "French",
      "Japanese",
    ],
    "pages": 1741
  },
```

**batch_loader.py**: loads the json objects in the above file in chunks into a Redis Database. The file assumes there is a working local Redis Database at `localhost:6379`.

**main.py**: demonstrates a simple semantic search query

**Working With Vector Embeddings.ipynb**: contains the code in main.py in Jupyter Notebook form.

**schema.py / schema.yaml**: defines the schema for the book objects to be indexed. Either one may be used in `main.py`

