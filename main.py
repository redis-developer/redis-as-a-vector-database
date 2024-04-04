from schema import schema

from redisvl.index import SearchIndex
from redisvl.query import VectorQuery
from redisvl.query.filter import Tag

from sentence_transformers import SentenceTransformer

REDIS_URL = "redis://localhost:6379"
schema_path = 'schema.yaml'
model_name = "all-MiniLM-L6-v2"

model = SentenceTransformer(model_name)

# Alternative method for creating search index from a yaml file
# index = SearchIndex.from_yaml(
#     schema_path,
#     redis_url=REDIS_URL
# )

index = SearchIndex.from_dict(
    schema, 
    redis_url=REDIS_URL
)

if not index.exists():
    index.create(overwrite=False)

query = model.encode("Dinosaurs are still on the earth")

tag_filter = Tag("genres") == "Science Fiction"

query = VectorQuery(
    vector = query,
    vector_field_name = "embedding",
    return_fields = ["title", "author", "description", "genres"],
    filter_expression = tag_filter,
    dialect = 3,
    num_results = 3
)

import pprint
pp = pprint.PrettyPrinter(indent=2)

results = index.query(query)
pp.pprint(results)
