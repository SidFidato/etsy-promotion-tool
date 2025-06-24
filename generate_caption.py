from bark import generate_audio, preload_models
import torchaudio, torch, whisper, json
import numpy as np

def generate_caption_and_audio(script_text, voice_path="voice.wav", caption_path="caption_segments.json"):
    preload_models()
    sentences = [s.strip() for s in script_text.split('.') if s.strip()]
    audio_chunks = [generate_audio(line, history_prompt="v2/en_speaker_6") for line in sentences]
    voiceover = np.concatenate(audio_chunks)
    torchaudio.save(voice_path, torch.tensor(voiceover).unsqueeze(0), 24000)

    model = whisper.load_model("base")
    result = model.transcribe(voice_path)
    segments = result["segments"]
    captions = [{"start": s["start"], "end": s["end"], "text": s["text"].strip()} for s in segments]

    with open(caption_path, "w", encoding="utf-8") as f:
        json.dump(captions, f, indent=2)
