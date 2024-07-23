from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


class ollama:
    def __init__(self, model, max_tokens=1000, temperature=0.7):
        self.client = ChatOllama(
            model = model,
            max_tokens = max_tokens,
            temperature = temperature,
        )
    
    def get_response(self, messages, stream=False):
        prompt = ChatPromptTemplate.from_template(
            """你是一个诗人，可以根据用户的要求写诗。请根据以下规则来作诗：
                1. 如果用户的要求中没有提到 "风格"，请告诉用户你不能写。
                2. 如果用户提到的诗人不是中国/中国古时候的朝代的诗人，或者诗人来自其他国家，请推荐一个中国诗人。
                3. 诗的格式只能是4句话。

                用户的要求：{user_request}
            """
        )
        strparser = StrOutputParser()
        chain = prompt | self.client | strparser
        
        
        if stream:
            response = chain.stream({'user_request':messages})
        else:
            response = chain.invoke({"user_request":messages})
            
        return response
            
        

if __name__ == ("__main__"):
    model = ollama(model='qwen2:7b')
    user_request = input("写下您的要求：")
    result = model.get_response(user_request)
    print(result)

