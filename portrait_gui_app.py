import gradio as gr
import os, shutil, subprocess
from uuid import uuid4
from generate_caption import generate_caption_and_audio
import time

def rename_and_save(file_obj, new_name):
    ext = os.path.splitext(file_obj.name)[-1]
    final_name = f"{new_name}{ext}"
    shutil.copy(file_obj.name, final_name)
    return final_name

def run_tool(script_text, video_file, image_file, progress=print):
    uid = str(uuid4())[:8]
    video_path = rename_and_save(video_file, f"input_video_{uid}")
    image_path = rename_and_save(image_file, f"input_image_{uid}")
    script_path = f"script.txt"

    with open(script_path, "w", encoding="utf-8") as f:
        f.write(script_text)

    progress("📢 Generating voice and captions...")
    generate_caption_and_audio(script_text)

    progress("🎬 Rendering video...")
    subprocess.run(["python", "portrait_tool.py"], check=True)
    return "final_video.mp4"

with gr.Blocks(theme=gr.themes.Soft(primary_hue="amber"), title="Portrait Video Generator") as app:
    gr.Markdown("""
    # ✨ AI Portrait Video Generator
    Create professional vertical videos with synced captions and voiceover using AI.
    """)

    with gr.Row():
        with gr.Column():
            video_input = gr.File(label="🎥 Upload Video", file_types=[".mp4"])
            image_input = gr.File(label="🖼️ Upload Bottom Image", file_types=[".jpg", ".png"])
        with gr.Column():
            script_input = gr.Textbox(label="📝 Paste Your Script", lines=7, placeholder="Type your voice script here...")

    generate_btn = gr.Button("🚀 Generate Final Video", variant="primary")
    output = gr.Video(label="✅ Output Video Preview")
    status = gr.Markdown("", visible=False)

    def generate(script, video_file, image_file):
        status.update(value="🔄 Step 1/2: Generating voiceover...", visible=True)
        time.sleep(0.5)
        out = run_tool(script, video_file, image_file, progress=lambda msg: status.update(value=f"🔄 {msg}"))
        time.sleep(0.5)
        status.update(value="✅ Video Generated Successfully!")
        return out, status

    generate_btn.click(generate, [script_input, video_input, image_input], [output, status])

app.launch()
