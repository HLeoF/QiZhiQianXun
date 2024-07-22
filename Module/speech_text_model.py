
import os
import edge_tts
import gradio as gr
from loguru import logger
from openai import OpenAI
from dotenv import load_dotenv
import speech_recognition as sr
from playsound import playsound

recognizer = sr.Recognizer()

def recognize_speech_from_mic(language='es-ES'):
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        gr.Info("请说话....",duration=5)
        audio = recognizer.listen(source)

        try:
            gr.Info("正在识别.....",duration=5)
            speech_text = recognizer.recognize_google(audio, language=language)
            logger.success(f"你说：{speech_text}")
            return speech_text
        except sr.UnknownValueError:
            logger.error("无法识别语音, 请重试")
            return None
        except sr.RequestError as e:
            logger.error(f"请求错误; {e}")
            return None

async def speak_text(text, voice="zh-CN-YunxiNeural"):
    player = edge_tts.Communicate(text, voice)
    await player.save("output.mp3")
    playsound("output.mp3")
    os.remove("output.mp3")
