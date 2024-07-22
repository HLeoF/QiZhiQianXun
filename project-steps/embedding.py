import json

def load_jsonfile(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
        print(f"Successfully Load JSON data file {filename}")
        return data
    except FileNotFoundError:
        print(f"JSON file {filename} Not Found")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON File ERROR {e}")
        return None
    except Exception as e:
        print(f"Error When Load JSON file: {e}")
    return None


def get_embeddings(texts, client, model="text-embedding-3-small"):
    response = client.embeddings.create(
        input=texts,
        model=model,
    )
    embeddings = [data.embedding for data in response.data]
    return embeddings
