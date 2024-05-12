from flask import Flask, render_template, request, redirect, url_for
import tensorflow as tf
from tensorflow import keras
import pickle
from MFCC import MFCC
import numpy as np
import os
import pyaudio
import wave
from sklearn.preprocessing import LabelEncoder
app = Flask(__name__)

# Load the trained model
# with open('C:/Users/Admin/Documents/GitHub/Sound-processing/Test-soundProcessing/trained_model.pkl', 'rb') as file:
#     model = pickle.load(file)
model = tf.keras.models.load_model('C:/Users/duyma/Documents/GitHub/Speaker-Recognize/finetune_model/loss2.4acc92lb31.h5')

# Thư mục lưu trữ tệp âm thanh
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Cấu hình PyAudio
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 10  # Thời gian ghi âm

# Tạo một PyAudio object
audio = pyaudio.PyAudio()

def record_audio(file_path):
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    frames = []

    print("Recording...")

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Finished recording.")

    stream.stop_stream()
    stream.close()

    wf = wave.open(file_path, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


@app.route('/record', methods=['POST'])
def record():
    file_path = os.path.join(UPLOAD_FOLDER, 'test1.wav')
    record_audio(file_path)
    return redirect(url_for('index'))

@app.route('/predict_voice', methods=['POST'])
def predict_voice():
    file_path = os.path.join(UPLOAD_FOLDER, 'test.wav')
    record_audio(file_path)
        # Get the input data from the form
    Mfcc=MFCC('', 'C:/Users/duyma/Documents/GitHub/Speaker-Recognize/uploads/test.wav')
    A = Mfcc[:,0:400]
    print(A)
    A=np.expand_dims(A, axis=0)
    prediction = model.predict(A)
    print("prediction shape:", prediction)
    a=np.argmax(prediction)
    pred=np.array([a])
# Load the label encoder
    with open('C:/Users/duyma/Documents/GitHub/Speaker-Recognize/Test-soundProcessing/label_encoder.pkl', 'rb') as f:
        label_encoder = pickle.load(f)
    
    # Load the encoded data as a NumPy array
    encoded_data = np.load('C:/Users/duyma/Documents/GitHub/Speaker-Recognize/Test-soundProcessing/encoded_data.npy')

    # Decode the encoded data

    decoded_value = label_encoder.inverse_transform(pred)[0]
    print(decoded_value)
    # Preprocess the input data if necessary


    # Process the predictions if necessary

    # Return the output to the user
    return render_template('result.html', predictions=decoded_value,compatibles=np.max(prediction))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get the input data from the form
    input_data = request.form['input_data']
    TEST_PATH=''
    Mfcc=MFCC(TEST_PATH,input_data)
    A = Mfcc[:,0:400]
    print(A)
    A=np.expand_dims(A, axis=0)
    prediction = model.predict(A)
    print("prediction shape:", prediction)
    a=np.argmax(prediction)
    pred=np.array([a])
# Load the label encoder
    with open('Test-soundProcessing/label_encoder.pkl', 'rb') as f:
        label_encoder = pickle.load(f)
    
    # Load the encoded data as a NumPy array
    encoded_data = np.load('Test-soundProcessing/encoded_data.npy')

    # Decode the encoded data

    decoded_value = label_encoder.inverse_transform(pred)[0]
    print(decoded_value)
    # Preprocess the input data if necessary


    # Process the predictions if necessary

    # Return the output to the user
    return render_template('result.html', predictions=decoded_value,compatibles=np.max(prediction))

if __name__ == '__main__':
    app.run(debug=True)
