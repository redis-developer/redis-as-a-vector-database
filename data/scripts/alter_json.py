import json
import random

languages = ['Spanish', 'French', 'German', 'Chinese', 'Japanese', 'Arabic', 'Russian', 'Italian']


# Open the JSON file in read mode
json_file_path = '../data/larger_science_fiction.json'
with open(json_file_path, 'r') as f:
    # Load JSON data
    data = json.load(f)

    # Convert Genres from String to List
    for item in data:
        genres = item["Genres"]
        genres= genres.replace('\'', '\"')
        print(genres)
        genres = json.loads(genres)
        print('happy')
        genres = genres.keys()
        genres = list(genres)
        item["genres"] = genres
        del item["Genres"]
        
        random_languages = random.sample(languages, random.randint(0, 8))
        random_languages.insert(0, 'English')
        item["editions"] = random_languages
        del item["Edition_Language"]
        
        pages = random.randint(150, 2350)
        item["pages"] = pages
        
        item["year_published"] = int(item["year_published"])
        item["votes"] = int(item["votes"])
        item["score"] = float(item["score"])
        
        
        
# Open the JSON file in write mode
with open('science_fiction_books.json', 'w') as f:
    # Write modified JSON content back to the file
    json.dump(data, f, indent=4)