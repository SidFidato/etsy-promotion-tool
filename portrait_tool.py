import cv2
import numpy as np
import json
import os
from PIL import ImageFont, ImageDraw, Image
import moviepy.editor as mp

with open("caption_segments.json", "r", encoding="utf-8") as f:
    caption_data = json.load(f)

video = cv2.VideoCapture("input_video.mp4")
image = cv2.imread("input_image.png") if os.path.exists("input_image.png") else cv2.imread("input_image.jpg")
voice = mp.AudioFileClip("voice.wav")

W, H = 1080, 1920
canvas = np.ones((H, W, 3), dtype=np.uint8) * 255

font_path = "BebasNeue-Bold.ttf"
font_size = 80
font = ImageFont.truetype(font_path, font_size)

video_frames = []
fps = int(video.get(cv2.CAP_PROP_FPS))
total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

for i in range(total_frames):
    success, frame = video.read()
    if not success:
        break

    canvas[:, :, :] = 255

    frame = cv2.resize(frame, (1140, 912))
    x_offset = (W - 1140) // 2
    canvas[0:912, x_offset:x_offset+1140] = frame

    image_resized = cv2.resize(image, (1140, 912))
    canvas[1008:1920, x_offset:x_offset+1140] = image_resized

    current_time = i / fps
    caption_text = ""
    for segment in caption_data:
        if segment['start'] <= current_time <= segment['end']:
            caption_text = segment['text'].upper()
            break

    if caption_text:
        pil_img = Image.fromarray(canvas)
        draw = ImageDraw.Draw(pil_img)

        text_width, text_height = draw.textbbox((0, 0), caption_text, font=font)[2:]
        padding = 30
        bg_height = text_height + padding * 2
        caption_y = 930 - bg_height // 2

        draw.rectangle([(0, caption_y), (W, caption_y + bg_height)], fill=(0, 0, 0))
        draw.text(((W - text_width) // 2, caption_y + padding), caption_text, font=font, fill=(255, 255, 0))
        canvas = np.array(pil_img)

    video_frames.append(canvas.copy())

video.release()

out = cv2.VideoWriter("final_video.mp4", cv2.VideoWriter_fourcc(*"mp4v"), fps, (W, H))
for frame in video_frames:
    out.write(frame)
out.release()

final = mp.VideoFileClip("final_video.mp4").set_audio(voice)
final.write_videofile("final_video.mp4", codec="libx264", audio_codec="aac")
