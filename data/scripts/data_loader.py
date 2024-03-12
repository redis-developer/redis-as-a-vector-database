
import argparse
import io
import json
import os
from redisvl.index import SearchIndex
from sentence_transformers import SentenceTransformer

# Load the sentence transformer model
model_name = "all-MiniLM-L6-v2"
model = SentenceTransformer(model_name)

def create_embedding(description):
    return model.encode(description)

index = SearchIndex.from_yaml(
    "../../schema.yaml", 
    redis_url="redis://localhost:6379"
)
index.create(overwrite=True)

import json

# Specify the path to your JSON file
json_file_path = '../data/larger_science_fiction.json'

# Read and load data from the JSON file
with open(json_file_path, 'r') as file:
    data = json.load(file)

# # Iterate over each object in the JSON array



# for filename in os.listdir(args.books_dir):
#     f = os.path.join(args.books_dir, filename)

#     if os.path.isfile(f):
#         book_file = io.open(f, encoding="utf-8")
books_loaded = 0
BATCH_SIZE = 32
for i in range(0, len(data), BATCH_SIZE):
    book_batch = data[i:i+BATCH_SIZE]
    for book in book_batch:
            description = book.get("description","")
            embedding = create_embedding(description)
            embedding_list = embedding.tolist()
            book["embedding"] = embedding_list
        # book = json.dumps(book)
    index.load(book_batch)
    books_loaded += 1

print(f"Loaded {books_loaded} books into Redis.")

