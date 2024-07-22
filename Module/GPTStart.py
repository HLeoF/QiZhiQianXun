from openai import OpenAI
from loguru import logger
from dotenv import load_dotenv

load_dotenv("D:/LLMs Projects/enviroment.env")

class GPTStart:
    def __init__(self):
        self.client = OpenAI()

    # Text Module
    def get_response(self,messages,model = "gpt-3.5-turbo", max_tokens = 1000,temperature = 0.7,stream = False):
        logger.info(messages)
        if isinstance(messages,str):
            messages = [{"role": "user", "content": messages}]
        elif not isinstance(messages, list):
            return "Invalid 'Messages' Type, It must be a String or list"
        
        completion = self.client.chat.completions.create(
            messages=messages,
            model=model,
            max_tokens=max_tokens,
            stream=stream,
            temperature=temperature,
        )

        if stream:
            return completion
        
        logger.debug(completion.choices[0].message.content)
        logger.info(f"Total Token:{completion.usage.total_tokens}")
        return completion.choices[0].message.content
    

    # Image Module
    def generate_image(self, prompt, model="dall-e-3", quality="standard", size="1024x1024", style="vivid", n=1, response_format="url"):
        response = self.client.images.generate(
            prompt=prompt,
            model=model,
            quality=quality,
            size=size,
            style=style,
            n=n,
            response_format=response_format,
        )

        logger.info(f"Improved Prompt: {response.data[0].revised_prompt}")
        return response
    
    def get_embeddings(self, context, model="text-embedding-3-small"):
        response = self.client.embeddings.create(
            input=context,
            model=model,
        )
        embeddings = [data.embedding for data in response.data]
        return embeddings
    