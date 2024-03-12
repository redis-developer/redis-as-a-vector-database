import os
from sentence_transformers import SentenceTransformer
import json
import redis

# Set the directory path
directory_path = '../books'

# Load the sentence transformer model
model_name = "all-MiniLM-L6-v2"
model = SentenceTransformer(model_name)

# Connect to Redis
r = redis.from_url("redis://localhost:6379")

def make_key(book_id):
    return f"book:{book_id}"

# Function to create an embedding for a description
def create_embedding(description):
    return model.encode(description)

# Iterate through each JSON file in the directory
for filename in os.listdir(directory_path):   
    if filename.endswith('.json'):
        file_path = os.path.join(directory_path, filename)

        # Read the JSON file
        with open(file_path, 'r') as file:
            try:
              json_object = json.loads(file.read())
            except:
              print("I just cant")
            if json_object is None:
              print("i found nothing!")
              continue
            else:
              print(json_object.get("id",""))
              # Extract the description
              description = json_object.get("description", "")
              id = json_object.get("id", "")

              print(f"embedding {id}...")
              # Create an embedding
              embedding = create_embedding(description)
              embedding_list = embedding.tolist()
              # Add the embedding to the JSON object
              json_object["embedding"] = embedding_list
              
              # Write the updated JSON object to the same file
              with open(file_path, 'w') as file:
                  json.dump(json_object, file, indent=2)

              redis_key = make_key(id)
              result = r.json().set(redis_key, "$.embedding", embedding_list)
              print(result)
              title = json_object.get("title","")
              print(f"Added embedding for {id}:{title}")
