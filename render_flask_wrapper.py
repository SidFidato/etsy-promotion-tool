import gradio as gr
from portrait_gui_app import portrait_ui
import os

def start_gradio():
    portrait_ui.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 3000)))

if __name__ == "__main__":
    start_gradio()
