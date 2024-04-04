import json
import concurrent.futures
from sentence_transformers import SentenceTransformer
from redisvl.index import SearchIndex

# Your data and Redis index setup
index = SearchIndex.from_yaml(
    "./schema.yaml", 
    redis_url="redis://localhost:6379"
)
index.create(overwrite=True)

# Function to create an embedding for a book
def create_embedding(book):
    description = book.get("description", "")
    embedding = model.encode(description)
    embedding_list = embedding.tolist()
    book["embedding"] = embedding_list

# Load the sentence transformer model
model_name = "all-MiniLM-L6-v2"
model = SentenceTransformer(model_name)

# Specify the batch size
BATCH_SIZE = 128

# Specify the path to your JSON file
json_file_path = 'science_fiction_books.json'

# Read and load data from the JSON file
with open(json_file_path, 'r') as file:
    data = json.load(file)

# Use ThreadPoolExecutor for parallel embedding creation
with concurrent.futures.ThreadPoolExecutor() as executor:
    # Iterate over the data in batches
    for i in range(0, len(data), BATCH_SIZE):
        book_batch = data[i:i+BATCH_SIZE]

        # Parallelize embedding creation
        futures = [executor.submit(create_embedding, book) for book in book_batch]
        concurrent.futures.wait(futures)

        # Gather embeddings and load in a single batch
        embeddings = [book["embedding"] for book in book_batch]
        index.load(book_batch)
        print(f'Loaded batch #{int((i/BATCH_SIZE)+1)}.')

print(f"Loaded {len(data)} books into Redis.")