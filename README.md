# Working with Vector Embeddings - Step By Step

Vector embeddings are numerical representations of objects, words, or phrases in a high-dimensional space, where each point's position reflects its semantic similarity to others. In the context of semantic search, they enable systems to understand and match the contextual meaning behind search queries with relevant content, rather than relying solely on keyword matches. This approach significantly enhances the accuracy and relevance of search results by capturing the nuances of language and concept relationships.

Redis, traditionally known for its key-value store capabilities, has evolved to support vector databases through modules that enable the efficient storage and querying of vector embeddings. This extension of Redis's functionality allows for the rapid execution of semantic searches and similarity assessments in applications, leveraging its high-performance and scalable architecture to handle complex vector operations seamlessly.


## Prerequisites


### Installation requirements: 

Python, [Redis database setup](https://redis.io/docs/install/install-stack/), and the following Python packages: 



* sentence_transformers 
* redisvl

This tutorial complements the insights shared in the video [Redis as a Vector Database](https://youtube.com/tbd), providing practical steps and code examples. For a deeper dive into the concepts and more comprehensive examples, you can explore the full repository at [GitHub](https://github.com/redis-developer/redis-as-a-vector-database). Additionally, to expand your understanding and capabilities with Redis, including its application as a vector database, refer to the [official Redis documentation](https://redis.io/docs/).


## Step 1: Set Up the Environment


### A. Create a Virtual Environment

First, you'll need to create a virtual environment. This is a self-contained directory that contains a Python installation for a particular version of Python, plus a number of additional packages. Creating a virtual environment allows you to manage dependencies for different projects separately.

**For Windows:**

```bash

python -m venv venv

.\venv\Scripts\activate

```

**For macOS and Linux:**

```bash

python3 -m venv venv

source venv/bin/activate

```

After activation, your command line will indicate that you're now working inside the virtual environment. It's a best practice to create and use a virtual environment for Python projects to avoid conflicts between project dependencies.


### B. Install Required Packages

With your virtual environment activated, install the `sentence_transformers` and `redisvl` packages using pip. These packages provide the tools needed to generate vector embeddings from text and interact with Redis as a vector database, respectively.

Run the following command to install both packages:

```bash

pip install sentence_transformers redisvl

```

This command will download and install the `sentence_transformers` library, which is used for generating sentence embeddings, and the `redisvl` library, which is specifically designed for working with vector data in Redis.


## Step 2: Select and Load the Embedding Model**

The [all-MiniLM-L6-v2 model](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) offers an optimal balance between size and performance, making it highly efficient for generating semantically rich text embeddings. Its architecture is fine-tuned for understanding nuanced language representations, ensuring high-quality embeddings for semantic search applications with minimal computational overhead.

To import the `SentenceTransformer` class and load the chosen model, use the following Python code:

```python

from sentence_transformers import SentenceTransformer

# Specify the model name

model_name = "all-MiniLM-L6-v2"

# Load the model

model = SentenceTransformer(model_name)

```

This snippet first imports the `SentenceTransformer` class from the `sentence_transformers` package. Then, it specifies the model name (`"all-MiniLM-L6-v2"`) and loads it, creating an instance of the model that can be used to generate text embeddings.


## Step 3: Convert Text to Vector Embeddings

Let's observe a JSON object representing a book with various fields, including a `description` field that contains text which we want to convert into a vector embedding. Here's how you can extract the description text from this JSON object:

First, let's take a look at the JSON object:

```json

{

  "title": "Fire In His Spirit",  

  "author": "Ruby Dixon",  

  "score": "3.94",  

  "votes": "2754",  

  "description": "Gwen’s never wanted to be a leader, but when no one else stepped up, she took on the role. As the mayor of post-apocalyptic Shreveport, she’s made decisions to protect her people... and most of them have backfired disastrously. When she discovers that the dangerous gold dragon lurking outside of the fort has decided she’s his mate, heartsick Gwen thinks that the best thing she can do is confront him and take him far away from the city. She does this to save her people - her sister, her friends, her fort. She doesn’t expect to understand the dragon. She certainly doesn’t expect to fall in love.",

  "year_published": "2018",  

  "url": "http://www.goodreads.com/book/show/40790825-fire-in-his-spirit",  

  "genres": ["Romance", "Fantasy (Dragons)", "Fantasy", "Romance (Paranormal Romance)", "Fantasy (Paranormal)", "Science Fiction", "Paranormal (Shapeshifters)", "Science Fiction (Aliens)", "Science Fiction (Dystopia)", "Apocalyptic (Post Apocalyptic)"],  

  "editions": ["English", "Japanese", "Arabic", "French"],  

  "pages": 241

}

```

To extract the description from this JSON object in Python, you would first load the JSON into a Python dictionary (assuming this JSON object is already structured as a Python dictionary in this context) and then access the `description` field directly:

```python

# Assuming the JSON object is stored in a variable named 'book'

book = {

  "title": "Fire In His Spirit",  

  "author": "Ruby Dixon",  

  "score": "3.94",  

  "votes": "2754",  

  "description": "Gwen’s never wanted to be a leader, but when no one else stepped up, she took on the role. As the mayor of post-apocalyptic Shreveport, she’s made decisions to protect her people... and most of them have backfired disastrously. When she discovers that the dangerous gold dragon lurking outside of the fort has decided she’s his mate, heartsick Gwen thinks that the best thing she can do is confront him and take him far away from the city. She does this to save her people - her sister, her friends, her fort. She doesn’t expect to understand the dragon. She certainly doesn’t expect to fall in love.",

  "year_published": "2018",  

  "url": "http://www.goodreads.com/book/show/40790825-fire-in-his-spirit",  

  "genres": ["Romance", "Fantasy (Dragons)", "Fantasy", "Romance (Paranormal Romance)", "Fantasy (Paranormal)", "Science Fiction", "Paranormal (Shapeshifters)", "Science Fiction (Aliens)", "Science Fiction (Dystopia)", "Apocalyptic (Post Apocalyptic)"],  

  "editions": ["English", "Japanese", "Arabic", "French"],  

  "pages": 241

}

# Extract the description text

book_description = book["description"]

```

The next step is to convert this text into a vector embedding using the loaded `SentenceTransformer` model. Here's how you can do it:

```python

# Convert the book description text to a vector embedding

embedding = model.encode(book_description)

# Optionally, convert the embedding to a list for easier handling, 

# especially if you need to store it in a JSON-compatible format

embedding_list = embedding.tolist()

```

The `model.encode` method takes the book description as input and returns a vector embedding of the description. This embedding represents the semantic content of the description in a high-dimensional space, where similar meanings are encoded by proximal vectors.

The `embedding` variable now contains the vector representation of the book's description. We'll need to store this embedding in a format that's compatible with RedisVL, so we convert the numpy array to a list using `.tolist()`, resulting in `embedding_list`.


## Step 4: Store Embeddings in Redis

Storing JSON objects in Redis allows for the efficient management and querying of structured data directly within the database, leveraging Redis's high-performance capabilities. This feature supports a wide range of applications, from caching and session storage to complex operations like searching and retrieving nested data within JSON documents.

The book JSON object provided in this tutorial contains several fields that describe attributes of a book, including its title, author, user-provided score, votes, description, publication year, goodreads URL, genres, language editions, and page count. Each field serves a specific purpose, with textual, numerical, and array data types representing the book's metadata and content.


### A. Adding an embedding to an object

To add the vector embedding to this JSON object you would assign the embedding to a new key within the object. To achieve this you would do the following:

```python

# Add the vector embedding to the 'book' dictionary, where 'embedding_list' represents the description's numerical representation

book["embedding"] = embedding_list

```

This operation adds a new key-value pair to the `book` dictionary, where the key is `"embedding"` and the value is the list of numbers representing the vector embedding of the book's description. The JSON object now includes this embedding, making it ready for enhanced search and similarity comparisons in applications leveraging vector embeddings.


### B. Creating a Schema

Creating a Redis schema for indexing vector embeddings and other relevant fields involves defining the structure and types of data your application will store and query within Redis. This schema setup is crucial for efficiently utilizing Redis's capabilities for vector search and other operations. Here's a guide to creating such a schema, particularly focusing on vector embeddings:


#### 1. Understand Your Data

Before creating the schema, you should have a clear understanding of the data you plan to store. In the context of the provided book JSON object, relevant fields include textual data (e.g., title, author, description), numerical data (e.g., score, votes, year_published, pages), and the vector embedding of the description.


#### 2. Define the Schema Structure

A Redis schema for vector embeddings typically includes definitions for:

- **Vector Fields**: Specify the key under which vector embeddings are stored and their dimensions.

- **Text Fields**: Define fields that store textual data, useful for text search.

- **Numeric Fields**: Include fields that store numerical values, allowing range queries.

- **Tag Fields**: Optionally, define tag fields for categorization (e.g., genres, editions).


#### 3. Create the Schema in Python

Using the `redisvl` library, you can define the schema programmatically. Here's an example based on the book data:

```python

from redisvl.index import SearchIndex

from redisvl.query import VectorQuery

from redisvl.query.filter import Tag, Num

schema = {

    "index": {

        "name": "book_index",

        "prefix": "book",

        "storage_type": "json",

    },

    "fields": [

        {"name": "id", "type": "tag"},

        {"name": "$.editions[*]", "type": "tag"},

        {"name": "$.genres[*]", "type": "tag"},

        {"name": "author", "type": "text"},

        {"name": "description", "type": "text"},

        {"name": "title", "type": "text"},

        {"name": "pages", "type": "numeric"},

        {"name": "$.year_published", "type": "numeric"},

        {"name": "$.votes", "type": "numeric"},

        {"name": "$.score", "type": "numeric"},

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

```


#### 4. Adding Data

With the schema defined and the index created, you can start adding JSON objects to Redis. These objects will automatically be indexed according to the defined schema, enabling efficient queries.

This schema setup lays the foundation for performing sophisticated searches, including vector similarity searches, text searches, and filtering based on numeric and tag criteria, utilizing the full power of Redis as a vector database.


## Step 5: Create an Index for Vector Search

Create a `SearchIndex` object by passing the schema and the Redis connection URL. This step links your schema with a Redis instance where the data will be stored and indexed.

```python

index = SearchIndex.from_dict(

    schema, 

    redis_url="redis://localhost:6379"  # Adjust the URL to your Redis instance

)

```

With the `SearchIndex` object ready and configured according to your schema, create the index in Redis. This is done by calling the `.create()` method on your index object. You can choose to overwrite an existing index with the same name by setting `overwrite=True` or preserve it with `overwrite=False`.

```python

index.create(overwrite=False)

```

This method establishes the index structure within your Redis instance, making it ready to store and query your data according to the defined schema, including efficiently handling vector-based searches.


## Step 6: Add JSON Objects with Vector Embeddings to Redis

Use the `.load()` method of your `SearchIndex` object to add the JSON object. This method takes a list of objects, so even if you're adding a single JSON object, make sure to wrap it in a list.

```python

# Add 'book_json' to Redis and index it using the 'index' SearchIndex instance

index.load([book_json])

```

This code snippet will add your JSON object to Redis under the defined schema, automatically indexing it based on the fields specified in your schema setup. The object is now searchable with queries that utilize its vector embeddings, text, numeric, and tag fields according to your index definition.


## Step 7: Prepare and Execute a Vector Search Query


### A. Prepare Your Query Text:

Your query text should be a string that represents the search intent. For example, if you're looking for books related to "science fiction adventures with AI," your query text would be exactly that phrase.

```python

query_text = "science fiction adventures with AI"

```


### B. Convert the Query Text to a Vector Embedding:

Use the `encode` method of your loaded model to convert the query text into a vector embedding. This method processes the text and outputs a vector (usually a NumPy array) where each element represents a dimension in the model's embedding space.

```python

query_embedding = model.encode(query_text)

```

The resulting `query_embedding` is a numerical representation of your query's semantic meaning, ready to be used in similarity searches. 


### C. Create the `VectorQuery` object

The `VectorQuery` object in `redisvl` is designed to facilitate vector-based search queries within Redis. Setting up a `VectorQuery` involves specifying the vector for the search query, defining search parameters, and indicating which fields should be returned in the search results. Here’s how to configure it:


#### 1. Specify the Query Vector: 

The query vector is the numerical representation of your search query, typically generated by converting text to a vector embedding using a model like `all-MiniLM-L6-v2`. You'll need this vector to initialize the `VectorQuery`.


#### 2. Define Search Parameters: 

This includes the vector field name in your Redis schema against which the query vector will be compared, the distance metric for similarity comparison (usually `cosine` for text embeddings), and other indexing specifics.


#### 3. Choose Fields to Return:

Decide which fields from your indexed documents you want to be included in the search results. This can be the title, author, description, or any other fields stored in your Redis documents.

Here is an example of how to set up a `VectorQuery` object with `redisvl`:

```python

# Create the VectorQuery object

query = VectorQuery(

    vector=query_embedding,  # The query vector obtained from encoding the search text

    vector_field_name="embedding",  # The field in Redis documents that contains the vector embeddings

    return_fields=["title", "author", "description"],  # Fields to return in the search results

    dialect=3,  # Query dialect (check redisvl documentation for details)

    num_results=3  # Number of search results to return

)

```

In this snippet, `query` is configured to perform a vector search using `query_embedding` against the `embedding` field in your indexed Redis documents. It's set to return the top 3 results, including the `title`, `author`, and `description` fields of each matching document. This approach enables highly relevant and context-aware search functionalities in applications leveraging Redis for vector data.


#### 4. Execute the Query

Executing a vector-based search query involves several steps, focusing on how the `vector_distance` field can be used to gauge similarity between the query and the search results. Here's how to perform and interpret such a query:


##### i. Execute the Vector Query

Assuming you have already set up your `VectorQuery` object as described previously, you execute the search query by passing it to the `.query()` method of your `SearchIndex` instance. This method returns a list of search results that match your query based on vector similarity.

```python

# Use the query object with the .query() method on the index instance to execute the search

results = index.query(query)

```


##### ii: Interpreting the Results

The results returned by the `.query()` method will include the documents that best match your search query based on the vector similarity. Along with the requested fields (`title`, `author`, `description`, etc.), each result will also include a `vector_distance` field if the query dialect supports it. This field indicates the distance between the query vector and the document's vector embedding, which is a measure of similarity:

- **Lower `vector_distance` values** indicate a closer match between the query and the document, suggesting high relevance.

- **Higher `vector_distance` values** suggest less similarity, meaning the document may not be as relevant to the query.


## Step 8: Conduct Filtered Searches

Enhancing search queries with filters in a vector search context allows you to refine the results based on specific criteria, such as genre or page count, beyond just the semantic similarity. Here’s a step-by-step guide on how to incorporate filters into your vector search queries:


### A. Understand the Filtering Mechanism

Filters in vector searches can be applied to any attribute in your indexed documents. For example, you might want to filter books by a certain genre or ensure the books returned have a certain number of pages. The `redisvl` library supports constructing complex filter expressions that can be used alongside vector similarity searches.


### B. Create Filter Expressions

Filter expressions are constructed using the fields defined in your schema. For categorical data like genres, you might use tag filters. For numerical data like page counts, you can use numerical range filters.

```python

from redisvl.query.filter import Tag, Num

# Example of creating a filter for the genre

genre_filter = Tag("genres") == "Science Fiction"

# Example of creating a filter for the page count

page_count_filter = Num("pages") > 200

```


### C: Combine Filters as Needed

You can combine multiple filters using logical operators to refine your search criteria further. This is useful for applying multiple restrictions, like finding science fiction books with more than 200 pages.

```python

# Combining filters with an AND operation

combined_filter = genre_filter & page_count_filter

```


### D. Apply Filters to Your Vector Query

When creating your `VectorQuery` object, include the combined filter expression using the `filter_expression` parameter. This tells the query to return only the results that match both the semantic similarity criteria and the filter conditions.

```python

from redisvl.query import VectorQuery

# Adjust your VectorQuery setup to include the filter expression

query_with_filters = VectorQuery(

    vector = query_embedding,

    vector_field_name = "embedding",

    dialect = 3,  # Query dialect (check redisvl documentation for details)

    return_fields = ["title", "author", "description", "genres", "pages"],

    filter_expression = combined_filter,  # Apply the combined filter here

    num_results = 3

)

```


### E. Execute the Filtered Search Query

Execute your query as before. The results will now be filtered according to your specified criteria, in addition to being ranked by vector similarity.

```python

filtered_results = index.query(query_with_filters)

```

The returned results will adhere to both the semantic similarity based on the vector embeddings and the constraints imposed by your filters. This approach enables more precise control over the search results, ensuring they meet specific requirements or preferences.

By applying filters to your vector search queries, you can significantly enhance the relevancy and specificity of the search results, making your search feature more powerful and user-friendly.


## Conclusion

The process of integrating vector embeddings into an application's search capabilities with Redis starts with selecting an appropriate model to convert textual data into vector embeddings that capture semantic meaning. These embeddings are then stored in Redis alongside other relevant fields of the data objects, utilizing a predefined schema that supports efficient indexing and querying of vector data. Through the creation of a Redis search index, applications can perform sophisticated semantic searches by comparing the similarity between query embeddings and stored embeddings, effectively enhancing search functionalities with the ability to understand and match based on context and meaning, rather than mere keyword overlap. This approach leverages Redis's high performance and scalability to provide advanced search capabilities that are both fast and relevant, meeting the needs of applications requiring nuanced data retrieval mechanisms.

Diving into vector embeddings and Redis offers a rich playground for enhancing your application's search capabilities.We encourage you to experiment with different models beyond `all-MiniLM-L6-v2`, as each model has unique strengths and can offer different perspectives on your data. Don't hesitate to tweak your queries and explore various filters to refine your search results further. Playing with these components can lead to surprising discoveries about what makes your data tick and how best to serve it to your users. 

Remember, the best solutions often come from a willingness to try new approaches and learn from the outcomes. So, go ahead and explore the vast possibilities—your next breakthrough in search functionality is just an experiment away!
