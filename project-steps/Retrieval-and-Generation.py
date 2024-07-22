import faiss
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv
from loadfiles import parse_pdf
from embedding import load_jsonfile, get_embeddings
from Storing import faiss_index, load_faiss, searchIndex
from splitting import split_docs_into_chunks, save_chunks_as_json

load_dotenv("D:/LLMs Projects/enviroment.env")

client = OpenAI()


def bind_variables(prompt_template, **kwags):
    for key, value in kwags.items():
        prompt_template = prompt_template.replace(f"{{{key}}}", value)
    return prompt_template

def get_response(prompt, model='gpt-3.5-turbo', max_tokens=1000, temperature=0.7):
    completion = client.chat.completions.create(
        messages=[{"role":"user","content":prompt}],
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return completion.choices[0].message.content
    

if __name__ == "__main__":
    json_path = "D:/LLMs Projects/FilesGPT/data/chunks.json"
    file_path = "D:/LLMs Projects/FilesGPT/data/translated_article.pdf"
    index_path = "D:/LLMs Projects/FilesGPT/data/chunksIdx.faiss"
    
    #Parse PDF file
    docs = parse_pdf(file_path)
    
    #Splitting docs after parse PDF file and save as json file
    chunks = split_docs_into_chunks(docs)
    save_chunks_as_json(chunks, json_path)

    #Embedding chunks in json file and store them into Faiss
    json_chunks = load_jsonfile("D:/LLMs Projects/FilesGPT/data/chunks.json")
    json_chunks_texts = [c['page_content'] for c in json_chunks]
    chunks_embeddings = get_embeddings(json_chunks_texts, client=client)
    index = faiss_index(chunks_embeddings, index_path=index_path)

    loaded_index = load_faiss(index_path)

    question = "什么Zore Shot Prompting?"
    question_embedding = get_embeddings(question, client=client)

    distance, indices = searchIndex(question_embedding, loaded_index, top_k=2)

   # find the content 
    top_k_chunks = [chunks[idx]['page_content'] for idx in indices]
    
    separator = "\n" + "=" * 30 + "\n"
    result_chunks = separator.join(top_k_chunks)
    

question_answering_prompt_template = """根据文章回答问题: 
文章：
'''
{article}
'''

问题：
'''
{question}
'''
输出："""

question_prompt = bind_variables(question_answering_prompt_template, article = result_chunks, question=question)

answer = get_response(question_prompt, max_tokens=2000)
print(answer)


