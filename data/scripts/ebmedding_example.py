import redis
Redis = redis.Redis()

from sentence_transformers import SentenceTransformer

# Load the sentence transformer model
model_name = "all-MiniLM-L6-v2"
model = SentenceTransformer(model_name)

# fetch the book description to embed
book_description = Redis.json.get('book:42', '$.description')

# convert the description text to a vector
embedding = model.encode(book_description).tolist()

# store the vector in the existing JSON object
Redis.json.set('book:42', '$.embedding', embedding)
