import json
import tiktoken
from loadfiles import parse_pdf
from langchain_text_splitters import RecursiveCharacterTextSplitter


# Compute text tokens number
def num_tokens(string:str, encoding_name:str="cl100k_base") -> int:
    """
    Returns the number of tokens in a text string.
    https://cookbook.openai.com/examples/how_to_count_tokens_with_tiktoken
    """
    encoding = tiktoken.get_encoding(encoding_name)
    tokens = encoding.encode(string)
    n_tokens = len(tokens)

    return n_tokens


def split_text_into_texts(text, chunk_size, chunk_overlap):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = chunk_size,
        chunk_overlap = chunk_overlap,
        length_function = num_tokens,
    )
    texts = text_splitter.split_text(text)
    return texts


def split_docs_into_chunks(docs, chunk_size=500, chunk_overlap=50):
    """
        将文章列表里面的每个doc换分成更小的文本块
    Args:
        docs (_type_): 文章文本和Metadata
        chunk_size (int, optional): 每个文本块的最大size
        chunk_overlap (int, optional): 文本块之间的重叠大小.

    """
    chunks = []
    chunk_id = 0
    for doc in docs:
        page_content_texts = split_text_into_texts(doc['page_content'], chunk_size, chunk_overlap)
        for page_content_text in page_content_texts:
            chunk = {
                "page_content":page_content_text,
                "metadata":{
                    "chunk_id": chunk_id,
                    **doc['metadata'],
                }
            }
            chunks.append(chunk)
            chunk_id +=1
    return chunks

def save_chunks_as_json(chunks, filename="ChunksOutput.json"):
    with open(filename,'w', encoding='utf-8') as file:
        json.dump(chunks, file, ensure_ascii=False, indent=4)
    print(f"Successful saved {len(chunks)} chunks to file: {filename}")

