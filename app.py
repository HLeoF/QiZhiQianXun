import sys
import os
current_dir = os.path.dirname((os.path.abspath(__file__)))
dir_path = os.path.join(current_dir, 'Module')
if dir_path not in sys.path:
    sys.path.append(dir_path)

from Module.configuration import *
from Module.UI_function import *

with gr.Blocks() as demo:

    gr.Markdown("# <center> 祺智千寻 🌌 </center>")

    with gr.Row(equal_height=True):
        with gr.Column(scale=4):
            chatbot = gr.Chatbot(label="Chat Box")
            user_input_textbox = gr.Textbox(label="User Input", value="")
            with gr.Row():
                submit_btn = gr.Button("Submit")
                clear_btn = gr.Button("Clear")
                Speak_btn = gr.Button("Speak")
        with gr.Column(scale=1):
            with gr.Tab(label="Q&A"):
                chat_mode_radio = gr.Radio(
                    choices=["Normal Chat",
                             "Document RAG"],
                    label="Chat Mode",
                    value="Normal Chat",
                    interactive=True)
                file_path_files = gr.Files(
                    label="Upload File",
                    file_count="multiple",
                    file_types=[
                        ".pdf",
                        ".txt",
                    ],
                    type="filepath",
                )
                file_paths_dataframe = gr.DataFrame(value = pd.DataFrame({'Uploaded File':[]}))
                top_n_number = gr.Number(label="Top N", value=5)
            with gr.Tab(label="Parameters"):
                with gr.Column():
                    model_dropdown = gr.Dropdown(
                        label="model",
                        choices=MODELS,
                        value=DEFAULT_MODEL,
                        multiselect=False,
                        interactive=True,
                    )
                    voice_language_dropdown = gr.Dropdown(
                        label="Voice Language",
                        choices=VOICE_LANGUAGE,
                        value=DEFAULT_VOICE_LANGUAGE,
                        multiselect=False,
                        interactive=True
                    )
                    voice_dropdown = gr.Dropdown(
                        label="Voice Model",
                        choices=VOICE_MODEL,
                        value=DEFAULT_VOICE_MODEL,
                        multiselect=False,
                        interactive=True
                    )
                    max_token_slider = gr.Slider(
                        minimum=0,
                        maximum=4096,
                        value=1000,
                        step=1.0,
                        label="Max Tokens",
                        interactive=True,
                    )
                    temperature_slider = gr.Slider(
                        minimum=0,
                        maximum=1,
                        value=0.7,
                        step=0.01,
                        label="Temperature",
                        interactive=True
                    )
                    stream_radio = gr.Radio(
                        choices=[
                            True,
                            False
                        ],
                        label="Stream Output",
                        value = True,
                        interactive=True)
                    

    model_dropdown.change(
        fn = fn_update_max_tokens,
        inputs = [model_dropdown, max_token_slider],
        outputs = max_token_slider
    )

    user_input_textbox.submit(
        fn = fn_handle_user_input,
        inputs = [user_input_textbox,chatbot],
        outputs=[chatbot]
    ).then(
        fn=fn_chat,
        inputs = [chat_mode_radio,
                  file_paths_dataframe,
                  user_input_textbox,
                  chatbot,
                  model_dropdown,
                  max_token_slider,
                  temperature_slider,
                  stream_radio,
                  top_n_number],
        outputs=[chatbot]
    ).then(
        fn = fn_handle_user_input_clean,
        inputs=[user_input_textbox],
        outputs=[user_input_textbox]
    )


    submit_btn.click(
        fn=fn_handle_user_input,
        inputs=[user_input_textbox, chatbot],
        outputs=[chatbot]
    ).then(
        fn=fn_chat,
        inputs = [chat_mode_radio,
                  file_paths_dataframe,
                  user_input_textbox,
                  chatbot,
                  model_dropdown,
                  max_token_slider,
                  temperature_slider,
                  stream_radio,
                  top_n_number],
        outputs=[chatbot]
    ).then(
        fn = fn_handle_user_input_clean,
        inputs=[user_input_textbox],
        outputs=[user_input_textbox]
    )


    Speak_btn.click(
        fn = fn_handle_user_voice_input,
        inputs=[voice_language_dropdown,chatbot],
        outputs=[chatbot]
    ).then(
        fn=fn_voice_chat,
        inputs = [chat_mode_radio,
                  file_paths_dataframe,
                  chatbot,
                  model_dropdown,
                  max_token_slider,
                  temperature_slider,
                  stream_radio,
                  top_n_number,
                  voice_dropdown],
        outputs=[chatbot]
    )

    clear_btn.click(lambda:None, None, chatbot, queue=False)
    
    file_path_files.upload(
        fn=fn_upload_file,
        inputs=[file_path_files],
        outputs=[file_paths_dataframe],
        show_progress=True,
    )

demo.queue().launch()