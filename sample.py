from redisvl.index import SearchIndex
from redisvl.query import VectorQuery
from sentence_transformers import SentenceTransformer

model_name = "all-MiniLM-L6-v2"
model = SentenceTransformer(model_name)

schema = {
    "index": {
        "name": "user_index",
        "prefix": "user",
        "storage_type": "hash",
    },
    "fields": {
        "tag": [{"name": "user"}, {"name": "credit_score"}],
        "text": [{"name": "job"}],
        "numeric": [{"name": "age"}],
        "vector": [{
            "name": "user_embedding",
            "dims": 3,
            "distance_metric": "cosine",
            "algorithm": "flat",
            "datatype": "float32"
        }]
    },
}

import numpy as np


data = [
    {
        'user': 'john',
        'age': 1,
        'job': 'engineer',
        'credit_score': 'high',
        'user_embedding': np.array([0.1, 0.1, 0.5], dtype=np.float32).tobytes()
    },
    {
        'user': 'mary',
        'age': 2,
        'job': 'doctor',
        'credit_score': 'low',
        'user_embedding': np.array([0.1, 0.1, 0.5], dtype=np.float32).tobytes()
    },
    {
        'user': 'joe',
        'age': 3,
        'job': 'dentist',
        'credit_score': 'medium',
        'user_embedding': np.array([0.9, 0.9, 0.1], dtype=np.float32).tobytes()
    }
]

index = SearchIndex.from_dict(
    schema, 
    redis_url="redis://localhost:6379"
)
index.create(overwrite=False)
keys = index.load(data)

print(keys)

description_query = "Dinosaurs avoided the meteor and still rule the world."
embedding_query = model.encode(description_query)
embedding_list = embedding_query.tolist()


query = VectorQuery(
    vector=[0.1, 0.1, 0.5],
    vector_field_name="user_embedding",
    return_fields=["user", "age", "job", "credit_score", "vector_distance"],
    num_results=3
)

results = index.query(query)
print(results)
