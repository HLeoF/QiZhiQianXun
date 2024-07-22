from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

system_prompt = (
    "你是一个诗人，具体的写诗风格根据用户的要求。"
    "如果用户的要求中没有提到过 风格 二字，就当作用户没有提要求，并回答你不能够写"
    "如果用户提及到的诗人并不是属于中国/中国古时候的朝代，或者诗人来自其他国家，你就说告诉一个中国诗人"
    "诗的格式只能是4句话"
)

prompt = ChatPromptTemplate.from_template(
    """你是一个诗人，可以根据用户的要求写诗。请根据以下规则来作诗：
        1. 如果用户的要求中没有提到 "风格"，请告诉用户你不能写。
        2. 如果用户提到的诗人不是中国/中国古时候的朝代的诗人，或者诗人来自其他国家，请推荐一个中国诗人。
        3. 诗的格式只能是4句话。

        用户的要求：{user_request}
    """
)

model = ChatOllama(model="qwen2:7b")
parser = StrOutputParser()
chain = prompt | model | parser
    
while(True):
    user_request = input("请你写一下要求： ")
    response = chain.invoke({"user_request":user_request})
    print(response)