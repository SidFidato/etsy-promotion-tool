from flask import Flask
import threading
app = Flask(__name__)

def launch_gui():
    import portrait_gui_app
    portrait_gui_app.app.launch(server_name="0.0.0.0", server_port=7860)

threading.Thread(target=launch_gui).start()

@app.route("/")
def home():
    return "✅ Gradio app running on :7860"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
