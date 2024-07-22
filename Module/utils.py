import time
import traceback
from VCDB import *
from Module.GPTStart import GPTStart
from Module.handleFiles import handlefiles
from Module.filFormatProcesser import fileFormatProcesser

def create_result_dict(code, msg=None, data=None):
    result = {
        'code': code,
        'msg': msg,
        'data':data,
    }
    return result

def file_store_vecDB(file_path, file_name, file_extension, file_md5):
    # Using file MD5 as collection 5
    collection_name = file_md5

    #Create Qdrant object
    qdrant = VCDB()

    # get the collection point number

    points_count = qdrant.check_collection(collection_name)
    

    if points_count == 0:
        #if collection points number is 0
        # Create a FileFormatProceser Object
        processFile = fileFormatProcesser(
            file_path=file_path,
            file_name=file_name,
            file_extension=file_extension,
            file_md5=file_md5,
        )

        #Obtain Docs
        docs = processFile.file_to_docs()
        logger.trace(f"docs: {docs}")

        #Cut docs to chunks
        chunks = processFile.split_docs_into_chunks(docs)

        #chunks into vetcor
        texts = [chunk['page_content'] for chunk in chunks]
        gpt = GPTStart()
        chunks_embeddings = gpt.get_embeddings(texts)

        if qdrant.add_vector_points(collection_name=collection_name, vectors=chunks_embeddings, payloads=chunks):
            return file_path
    
    elif points_count > 0:
        return file_path
    else:
        return ''
    

def upload_file(file_path):
    try:
        logger.info(f"File_path: {file_path} Type({type(file_path)})")

        #Check file_path
        if not file_path:
            #if file_path is invalid retrun 400 state
            return create_result_dict(400, "Did not Upload File")
        
        #Create the handfiles object
        handlefile = handlefiles(file_path=file_path)

        #Check whether file allows to process
        if not handlefile.check_file_extension():
            #if file extention does not allow to process, return 400 state
            extention = handlefile.handle_file_extension()
            return create_result_dict(400, f"Not Support this type file so far:{extention}")
        
        logger.trace(f"File allow be process | file_path:{file_path}")

        #Handle file basic information
        file_name = handlefile.get_file_name()
        file_extention = handlefile.handle_file_extension()
        file_md5 = handlefile.get_file_md5()
        logger.info(
            f"File Info | Name: {file_name} | Extention: {file_extention} | md5: {file_md5}"
        )

        # Store file into Vetcor database
        upload_file_path = file_store_vecDB(file_path, file_name, file_extention, file_md5)

        # Processing file successfully 
        if upload_file_path:
            # return 200 state
            return create_result_dict(200, "File Successfuly Uploaded", {'uploaded_file_path':upload_file_path})
        else:
            # if not return 500 state
            return create_result_dict(500, "File Unsuccessfuly Uploaded")

    except Exception:
        error = traceback.format_exc()
        logger.error(error)
        return create_result_dict(500, f"{error}")
    

def search_create_context(qdrant, collection_names, query_vector, limit):
    scored_points = []
    #Processing similarity search and get ScoredPoints object lists
    for collection_name in collection_names:
        scored_points_by_current_collection = qdrant.search(
            collection_name, query_vector, limit=limit
        )
        scored_points.extend(scored_points_by_current_collection)
    
    #Put the ScoredPoint object convert to dics list
    points = []
    for point in scored_points:
        point = {
            "id": point.id,
            "score": point.score,
            "payload": point.payload,
        }
        points.append(point)
    
    #Dict list descresing sort by points score
    points.sort(key=lambda x:x['score'], reverse=True)
    points = points[:limit]
    logger.trace(f"Points: {points}")

    #Constract contexts
    contexts = []
    for point in points:
        context = point['payload']['page_content']
        contexts.append(context)
    separator = "\n"+"="*30+"\n"
    context = separator.join(contexts)
    return context

def build_prompt(file_paths, user_input, chat_history, top_n):
    try:
        logger.debug(
            f"File Path: {file_paths}, user_input:{user_input}, chat_history:{chat_history}, top_n:{top_n}"
        )

        qdrant = VCDB()

        # Collection Name
        collection_names = []
        for path in file_paths:
            file_bytes = handlefiles.BytefilsRead(path)
            file_md5 = handlefiles.calculate_md5_files(file_bytes)
            collection_names.append(file_md5)
        logger.debug(f"Collection Names: {collection_names}")

        gpt = GPTStart()
        query_embeddings = retry(gpt.get_embeddings, args=([user_input]))
        if not query_embeddings:
            logger.error("Obtain Query Embedding Parameter Error")
            return ''
        query_embedding = query_embeddings[0]

        topN = int(top_n)
        context = search_create_context(qdrant, collection_names, query_embedding, topN)
        logger.trace(f"Context:\n{context}")

        chat_history_str = ""
        for chat in chat_history[:-1]:
            if chat[0]:
                chat_history_str += f"user:{chat[0]}\n"
            if chat[1]:
                chat_history_str += f"assistant:{chat[1]}\n"
        chat_history_str = chat_history_str[:-1]
        logger.trace(f"chat_history_str: \n{chat_history_str}")

        #Create Prompt
        prompt = f"""你是一位文档问答助手，你会基于`文档内容`和`对话历史`回答user的问题。如果用户的问题与`文档内容`无关，就不用强行根据`文档内容`回答。

文档内容：```
{context}```

对话历史：```
{chat_history_str}```

user: ```{user_input}```
assistant: """
        
        logger.info(f"prompt: \n{prompt}")
        return prompt
    except Exception:
        error = traceback.format_exc()
        logger.error(error)
        return ''
    

def retry(func, args=None, kwargs=None, retries=3, delay=1):
    """
    重试机制函数
    :param func: 需要重试的函数
    :param args: 函数参数，以元组形式传入
    :param kwargs: 函数关键字参数，以字典形式传入
    :param retries: 重试次数 默认为3
    :param delay: 重试间隔时间 默认为1秒
    :return: 函数执行结果
    """
    for i in range(retries):
        try:
            if args is None and kwargs is None:
                result = func()
            elif args is not None and kwargs is None:
                result = func(*args)
            elif args is None and kwargs is not None:
                result = func(**kwargs)
            else:
                result = func(*args, **kwargs)
            return result
        except Exception as e:
            logger.warning(f"{func.__name__} function{i+1} Retry: {e}")
            time.sleep(delay)
    logger.error(f"Times of {func.__name__}function retry has been Done!")