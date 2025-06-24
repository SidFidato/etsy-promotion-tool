from gtts import gTTS
import whisper

tts = gTTS("Your input script here", lang='en')
tts.save("voice.wav")

model = whisper.load_model("base")
result = model.transcribe("voice.wav")

with open("caption_segments.json", "w", encoding="utf-8") as f:
    import json
    segments = [{"start": s['start'], "end": s['end'], "text": s['text']} for s in result['segments']]
    json.dump(segments, f, indent=2)
