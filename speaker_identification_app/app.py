from flask import Flask, request, render_template, jsonify, send_from_directory
import os
from werkzeug.utils import secure_filename
from transformers import AutoFeatureExtractor, AutoModelForAudioClassification, TrainingArguments, Trainer
from sklearn.preprocessing import LabelEncoder
import pickle
import soundfile as sf
with open('C:/Users/duyma/Documents/GitHub/Speaker-Recognize/WavLM/label_encoder.pkl', 'rb') as f:
    label_encoder = pickle.load(f)

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

fe = AutoFeatureExtractor.from_pretrained("microsoft/wavlm-base")
model = AutoModelForAudioClassification.from_pretrained("C:/Users/duyma/Documents/GitHub/Speaker-Recognize/WavLM/Wav30fr", num_labels=29)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        return jsonify({"message": "File uploaded successfully", "filename": file.filename}), 200

@app.route('/predict', methods=['POST'])
def identify_speaker():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        print(f"File saved to: {filepath}")  # Debug: Verify file path
    audio, sample_rate = sf.read(filepath)
    inputs = fe(audio, sampling_rate=fe.sampling_rate, return_tensors="pt")
    logit = model(**inputs).logits
    preds = logit.argmax(-1)
    decoded_value = label_encoder.inverse_transform(preds)[0]
    print("dap an ne`" ,decoded_value)
    return jsonify(decoded_value), 200
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    print(f"Serving file from: {file_path}")  # Debugging: Print the file path
    if os.path.exists(file_path):
        return send_from_directory('C:/Users/duyma/Documents/GitHub/Speaker-Recognize/uploads', filename)
    else:
        return jsonify({"error": "File not found"}), 404
if __name__ == '__main__':
    app.run(debug=True)
