import gradio as gr
import os
import shutil

script_input = gr.Textbox(label="Enter Your Script")
video_input = gr.Video(label="Upload Portrait Video")
image_input = gr.Image(label="Upload Image (1140x912)", type="filepath")

status = gr.Textbox(label="Status")

def generate_all(script, video_path, image_path):
    with open("script.txt", "w", encoding="utf-8") as f:
        f.write(script)
    shutil.copy(video_path, "input_video.mp4")
    shutil.copy(image_path, "input_image.png")
    os.system("python generate_caption.py")
    os.system("python portrait_tool.py")
    return "Video Generated Successfully!"

generate_btn = gr.Button("Generate Video")
gui = gr.Blocks()

with gui:
    gr.Markdown("# Portrait Video Generator")
    with gr.Row():
        with gr.Column():
            gui_script = script_input
            gui_video = video_input
            gui_image = image_input
            generate_btn.render()
        with gr.Column():
            gui_status = status

    generate_btn.click(generate_all, inputs=[gui_script, gui_video, gui_image], outputs=gui_status)

portrait_ui = gui
