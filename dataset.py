import yaml

from redisvl.index import SearchIndex
from redisvl.query import VectorQuery
from redisvl.query.filter import Tag

from sentence_transformers import SentenceTransformer

schema_path = 'schema.yaml'

model_name = "all-MiniLM-L6-v2"
model = SentenceTransformer(model_name)

index = SearchIndex.from_yaml(
    schema_path, 
    redis_url="redis://localhost:6379"
)
index.create(overwrite=False)

def prepare_query(query_text):
    embedding_query = model.encode(query_text)
    embedding_list = embedding_query
    return embedding_list


query = prepare_query("Interdimensional Travel.")

tag_filter = Tag("genres") == "Science Fiction"

query = VectorQuery(
    vector=query,
    vector_field_name="embedding",
    return_fields=["title", "author", "description", "genres"],
    filter_expression=tag_filter
)

import pprint
pp = pprint.PrettyPrinter(indent=2)

results = index.query(query)
pp.pprint(results)
