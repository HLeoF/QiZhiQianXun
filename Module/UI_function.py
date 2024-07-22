import asyncio
import sys
import gradio as gr
import pandas as pd
from loguru import logger
from GPTStart import GPTStart
from utils import upload_file, build_prompt
from configuration import MODEL_TO_MAX_TOKENS
from filFormatProcesser import fileFormatProcesser
from speech_text_model import recognize_speech_from_mic,speak_text


logger.remove()
logger.add(sys.stderr, level="TRACE")

# Function for update LLM max tokens
def fn_update_max_tokens(model, origin_tokens):
    new_max_tokens = MODEL_TO_MAX_TOKENS.get(model)
    new_max_tokens = new_max_tokens if new_max_tokens else origin_tokens

    new_set_tokens = origin_tokens if origin_tokens <= new_max_tokens else 1000

    new_max_tokens_component = gr.Slider(
        minimum=0,
        maximum=new_max_tokens,
        value=new_set_tokens,
        step=1.0,
        label="Max Tokens",
        interactive=True,
    )

    return new_max_tokens_component


# Function for handle user input box content
def fn_handle_user_input(user_input, chat_history):
    logger.info(f"Component Input | user input: {user_input} | Chat History: {chat_history}")

    chat_history = [] if not chat_history else chat_history

    if not user_input:
        gr.Warning("Please Enter Your Question")
        logger.warning("Please Enter Your Question")
        return chat_history
    
    chat_history.append([user_input, None])

    return chat_history


def fn_handle_user_voice_input(language, chat_history):
    speech_text = recognize_speech_from_mic(language)
    logger.info(f"User's Voice Input: {speech_text}")

    chat_history = [] if not chat_history else chat_history

    if not speech_text:
        gr.Warning("Please Input your voice")
        return chat_history
    
    chat_history.append([speech_text, None])

    return chat_history


# Function for clean user input box content
def fn_handle_user_input_clean(user_input):
    user_input=""
    return user_input


# Function for due with user input and chat with LLM
def fn_chat(chat_mode, uploaded_file_df, user_input, chat_history, model, max_tokens, temperature, stream, top_n):
    if not user_input:
        return chat_history
    
    messages = []

    if chat_mode == "Normal Chat":
        messages = user_input
        if len(chat_history) > 1:
            messages = []
            for chat in chat_history:
                if chat[0] is not None:
                    messages.append({"role":"user", "content":chat[0]})
                if chat[1] is not None:
                    messages.append({"role":"assistant","content":chat[1]})
    else:

        uploaded_file_paths = uploaded_file_df['Uploaded File'].values.tolist()
        logger.info(f"\n"
                    f"Chat Model: {chat_mode} \n"
                    f"File Path: {uploaded_file_paths} {type(uploaded_file_paths)} \n"
                    f"User Input: {user_input} \n"
                    f"Chat History: {chat_history} \n"
                    f"Using LLM Model: {model} {type(model)}\n"
                    f"Max Tokens: {max_tokens} {type(max_tokens)}\n"
                    f"Temperature: {temperature} {type(temperature)}\n"
                    f"Stream? : {stream} {type(stream)}\n"
                    f"top_n: {top_n} {type(top_n)}")
    
        if not isinstance(uploaded_file_paths, list) or not uploaded_file_paths or '' in uploaded_file_paths:
            gr.Warning("Unuploaded File")
        
        chat_doc_prompt = build_prompt(uploaded_file_paths, user_input, chat_history, top_n)

        if chat_doc_prompt:
            messages.append({"role":"user", "content":chat_doc_prompt})
        else:
            logger.error("Build Chat Doc Prompt Fail")
            messages = []
        

    if not messages:
        logger.error(f"message is empty list")
        gr.Warning("Server Error")
        return chat_history
    else:
        logger.trace(f"Message: {messages}")

        gpt = GPTStart()
        response = gpt.get_response(messages,model,max_tokens,temperature,stream)

        #Stream Output
        if stream:
            chat_history[-1][1] = ""
            for char in response:
                char_content = char.choices[0].delta.content
                if char_content is not None:
                    chat_history[-1][1] += char_content
                    yield chat_history
            else:
                logger.success(f"Stream Output | Bot Response: {chat_history[-1][1]}")
                prompt = messages
                if isinstance(messages, list):
                    prompt = ""
                    for message in messages:
                        prompt += message['content'] + "\n"
                logger.trace(f"prompt:{prompt}")
                #get the number tokens of prompt
                prompt_tokens = fileFormatProcesser.num_tokens(prompt)
                #get the number tokens of prompt
                completion_tokens = fileFormatProcesser.num_tokens(chat_history[-1][1])
                #Total Tokens
                total_tokens = prompt_tokens + completion_tokens
                logger.success(f"Stream Output | Total Tokens {total_tokens} "
                               f"=Prompt Tokens: {prompt_tokens} + Completion Tokens:{completion_tokens}")
        #Non Stream Output
        else:
            chat_history[-1][1] = response
            logger.success(f"Non Stream Output | Bot Response: {chat_history[-1][1]}")
            yield chat_history


def fn_upload_file(unuploaded_file_paths):
    logger.trace(f"Component Input | Unupload File Path:{unuploaded_file_paths}")

    upload_file_paths = []

    for file_path in unuploaded_file_paths:
        result = upload_file(str(file_path))

        if result.get('code') == 200:
            gr.Info("File Has Been Upload Successfuly")
            upload_file_paths.append(result.get('data').get('uploaded_file_path'))

        else:
            raise gr.Error("File failres to Upload") 
    return pd.DataFrame({'Uploaded File': upload_file_paths})

def fn_voice_chat(chat_mode,upload_file_df,chat_history, model, max_tokens, temperature, stream, top_n,voice):
    
    messages = []
    if chat_mode == "Normal Chat":
        messages = chat_history[0][0]
        if len(chat_history) > 1:
            messages = []
            for chat in chat_history:
                if chat[0] is not None:
                    messages.append({"role":"user", "content":chat[0]})
                if chat[1] is not None:
                    messages.append({"role":"assistant", "content":chat[1]})
    else:


        logger.success(f"user input: {chat_history[0][0]}")

        uploaded_file_paths = upload_file_df['Uploaded File'].values.tolist()
        logger.info(f"\n"
                    f"Chat Model: {chat_mode} \n"
                    f"File Path: {uploaded_file_paths} {type(uploaded_file_paths)} \n"
                    f"User Input: {messages} \n"
                    f"Chat History: {chat_history} \n"
                    f"Using LLM Model: {model} {type(model)}\n"
                    f"Max Tokens: {max_tokens} {type(max_tokens)}\n"
                    f"Temperature: {temperature} {type(temperature)}\n"
                    f"Stream? : {stream} {type(stream)}\n"
                    f"top_n: {top_n} {type(top_n)}")
        
        if not isinstance(uploaded_file_paths, list) or not uploaded_file_paths or '' in uploaded_file_paths:
            gr.Warning("Unuploaded File")
        chat_doc_prompt = build_prompt(uploaded_file_paths, chat_history[0][0], chat_history, top_n)

        if chat_doc_prompt:
            messages.append({"role":"user","content":chat_doc_prompt})
        else:
            logger.error("Build Chat Doc Prompt Fail")
            messages = []

    if not messages:
        logger.error(f"message is empty list")
        gr.Warning("Server Error")
        return chat_history
    else:
        logger.trace(f"Message: {messages}")    
        gpt = GPTStart()
        response= gpt.get_response(messages, model, max_tokens, temperature, stream)
        
        if stream:
            chat_history[-1][1] = ""
            for char in response:
                char_content = char.choices[0].delta.content
                if char_content is not None:
                    chat_history[-1][1] += char_content
                    yield chat_history
            else:
                logger.success(f"Stream Output | Bot Response: {chat_history[-1][1]}")
                prompt = messages
                if isinstance(messages, list):
                    prompt = ""
                    for message in messages:
                        prompt += message['content'] + "\n"
                logger.trace(f"prompt:{prompt}")
                #get the number tokens of prompt
                prompt_tokens = fileFormatProcesser.num_tokens(prompt)
                #get the number tokens of prompt
                completion_tokens = fileFormatProcesser.num_tokens(chat_history[-1][1])
                #Total Tokens
                total_tokens = prompt_tokens + completion_tokens
                logger.success(f"Stream Output | Total Tokens {total_tokens} "
                                f"=Prompt Tokens: {prompt_tokens} + Completion Tokens:{completion_tokens}")
        #Non Stream Output
        else:
            chat_history[-1][1] = response
            logger.success(f"Non Stream Output | Bot Response: {chat_history[-1][1]}")
            yield chat_history

        asyncio.run(speak_text(chat_history[-1][1], voice))

