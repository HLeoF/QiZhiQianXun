import faiss
import numpy as np
from loadfiles import parse_pdf
from splitting import split_docs_into_chunks, save_chunks_as_json
from embedding import load_jsonfile, get_embeddings


def faiss_index(embeddings, dimension=1536, index_path="test.faiss"):

    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings).astype('float32'))
    faiss.write_index(index,index_path)
    print("Successfully Create and Store FAISS index to ", index_path)
    return index

def load_faiss(index_path):
    try:
        return faiss.read_index(index_path)
    except Exception as e:
        print(f"Loading Faiss Index Error {e}.")
        return None


def searchIndex(query_vector, index, top_k = 5):
    """_summary_

    Args:
        query_vector : Query Vetor
        index (_type_): Faiss Vector Index
        top_k (int, optional): _description_. Defaults to 5.

    Returns:
        _type_: _description_
    """
    
    distance, indices = index.search(np.array(query_vector).astype('float32'), top_k)
    filter_indices = [idx for idx in indices[0] if idx != -1]
    filter_distance = [dist for dist, idx in zip(distance[0], indices[0]) if idx != -1]
    return filter_distance, filter_indices




