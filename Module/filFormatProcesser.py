import os
import json
import pdfplumber
import tiktoken
from typing import List
from Module.configuration import CHUNK_SIZE, CHUNK_OVERLAP
from langchain_text_splitters import RecursiveCharacterTextSplitter


class fileFormatProcesser:
    def __init__(self, file_path:str, file_name:str=None, file_extension:str = None, file_md5:str = None):
        
        self.file_path = file_path
        self.file_name = file_name
        self.file_extension=file_extension
        self.file_md5 = file_md5

    def file_to_docs(self) -> list:
        extension_mapping = {
            '.pdf':self.processingPDF,
            '.txt':self.processingTxt,
        } 
        func = extension_mapping.get(self.file_extension)
        return func(self.file_path)
    
    @staticmethod
    def processingPDF(file_path:str) -> List[dict]:
        file_name = os.path.basename(file_path)
        # declare a empty list to store the data of each parse pdf page
        chunks = [] 

        # Open PDF file By pdfminer
        with pdfplumber.open(file_path) as pdf:
            #Visit all pages for the pdf file
            for page in pdf.pages:
                #Extract current page content
                page_content = page.extract_text()
            
                #If current page exist content, processing and store data
                if page_content:
                    chunk = {
                        "page_content":page_content, # page content
                        "metadata":{
                            "source":file_path, # pdf source file path
                            "page_number":page.page_number, # current page number
                            "total_pages":len(pdf.pages), # the total number of the pdf file
                            "width":page.width, # page width
                            "height":page.height, # page height
                            "rotation":page.rotation, #page rotation
                            **pdf.metadata # extract other data from the pdf file
                        }
                    }

                    #construct content append into the chuncks list
                    chunks.append(chunk)
        return chunks
    
    
    @staticmethod
    def processingTxt(file_path:str) -> List[dict]:
        file_name = os.path.basename(file_path)

        with open(file_path, 'r') as file:
            text = file.read()
        if not text:
            return []
        chunk = {
            "page_content": text,
            "metadata": {
                "file_name":file_name
            }
        }
        return [chunk]
    
    #########################################

    @staticmethod
    def num_tokens(string:str, encoding_name:str="cl100k_base") -> int:
        """
        Returns the number of tokens in a text string.
        https://cookbook.openai.com/examples/how_to_count_tokens_with_tiktoken
        """
        encoding = tiktoken.get_encoding(encoding_name)
        tokens = encoding.encode(string)
        n_tokens = len(tokens)

        return n_tokens
    
    def split_text_into_texts(self, text, chunk_size, chunk_overlap):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = chunk_size,
            chunk_overlap = chunk_overlap,
            length_function = self.num_tokens,
        )
        texts = text_splitter.split_text(text)
        return texts
    
    def split_docs_into_chunks(self, docs, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP):
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
            page_content_texts = self.split_text_into_texts(doc['page_content'], chunk_size, chunk_overlap)
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
    
    # def save_chunks_as_json(self, chunks, filename="ChunksOutput.json"):
    #     with open(filename,'w', encoding='utf-8') as file:
    #         json.dump(chunks, file, ensure_ascii=False, indent=4)
    #     print(f"Successful saved {len(chunks)} chunks to file: {filename}")

# if __name__ == "__main__":
#     # 测试
#     file_path = "D:/LLMs Projects/FilesGPT/data/translated_article.pdf"
#     file_name = "translated_article.pdf"
#     file_extension = ".pdf"
#     file_md5 = "0"  # 'f59d5ebd9c2cb8161651f5e44ecd6c9f'

#     file_processor_helper = fileFormatProcesser(
#         file_path=file_path,
#         file_name=file_name,
#         file_extension=file_extension,
#         file_md5=file_md5,
#     )
#     docs = file_processor_helper.file_to_docs()
#     print(docs)

#     # 测试 num_tokens_from_string
#     print(fileFormatProcesser.num_tokens("tiktoken is great!"))