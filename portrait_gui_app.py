import gradio as gr
import os
import shutil

def generate_all(script, video_path, image_path):
    with open("script.txt", "w", encoding="utf-8") as f:
        f.write(script)
    shutil.copy(video_path, "input_video.mp4")
    shutil.copy(image_path, "input_image.png")
    os.system("python generate_caption.py")
    os.system("python portrait_tool.py")
    return "✅ Video Generated Successfully!"

with gr.Blocks() as portrait_ui:
    gr.Markdown("# 🖼️ Portrait Video Generator Tool")

    with gr.Row():
        with gr.Column():
            script_input = gr.Textbox(label="🎬 Enter Your Script", lines=4, placeholder="Type or paste your script here")
            video_input = gr.Video(label="📹 Upload Portrait Video (.mp4)")
            image_input = gr.Image(label="🖼️ Upload Bottom Image (1140x912)", type="filepath")
            generate_btn = gr.Button("🚀 Generate Video")
        with gr.Column():
            status = gr.Textbox(label="📢 Status")

    generate_btn.click(fn=generate_all, inputs=[script_input, video_input, image_input], outputs=status)
