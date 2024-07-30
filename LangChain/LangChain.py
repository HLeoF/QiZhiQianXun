from ast import Store
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
store = {}

class ollama:
    def __init__(self, model, max_tokens=1000, temperature=0.7):
        self.client = ChatOllama(
            model = model,
            max_tokens = max_tokens,
            temperature = temperature,
        )
    
    def get_session_history(session_id:str) -> BaseChatMessageHistory:
        if session_id not in store:
            store[session_id] = ChatMessageHistory()
        return store[session_id]
            
    
    def get_response(self, messages, config, history, stream=False):
        prompt = ChatPromptTemplate.from_template(
            """
            {user_request}
            """
        )
        strparser = StrOutputParser()
        chain = prompt | self.client | strparser
        self.client
        
        
        if stream:
            response = chain.stream({'user_request':messages})
        else:
            response = chain.invoke({"user_request":messages})
            
        return response
            
        

if __name__ == ("__main__"):
    
    model = ollama(model='qwen2:latest')
    with_message_history = RunnableWithMessageHistory(model, model.get_session_history)
    config = {"configurable":{"seesion_id":'uuid1'}}
    
    
    while True:
        user_request = input("~:")
        result = model.get_response(user_request,config, with_message_history, stream=False)
        for chunk in result:
            # 如果 chunk 具有 `content` 属性，输出内容
            if hasattr(chunk, 'content'):
                print(chunk.content, end="", flush=True)
            else:
                print(chunk, end="", flush=True)
