import json
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

json_data = '''
{
    "author": "George Mann",
    "id": "0",
    "description": "Free of the hex that has plagued it, the ghoulems head begins to reveal its secrets but its reawakening does not go unnoticed. Meanwhile, Joss, Ichabod and the others attend the  morning ceremony  of their late friend, where tensions run high, and the Celestials pay a visit to the shantytown to make pronouncements on the water crisis.",
    "editions": ["english", "spanish", "french"],
    "genres": ["comics (superheroes)"],
    "inventory": [{
    "status": "available",
    "stock_id": "0_1"
    }, {
    "status": "available",
    "stock_id": "0_2"
    }, {
    "status": "available",
    "stock_id": "0_3"
    }, {
    "status": "maintenance",
    "stock_id": "0_4"
    }, {
    "status": "available",
    "stock_id": "0_5"
    }, {
    "status": "available",
    "stock_id": "0_6"
    }, {
    "status": "available",
    "stock_id": "0_7"
    }, {
    "status": "on_loan",
    "stock_id": "0_8"
    }, {
    "status": "on_loan",
    "stock_id": "0_9"
    }],
    "metrics": {
        "rating_votes": 3,
        "score": 3.67
        },
    "pages": 1188,
    "title": "Engineward #2",
    "url": "https://www.goodreads.com/book/show/55127142-engineward-2",
    "year_published": 2020
}
'''
# Parse the JSON data
data = json.loads(json_data)

# Extract the description field
description = data.get("description", "")

embedding = model.encode(description)

print(embedding)