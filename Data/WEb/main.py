from flask import Flask, render_template, request
import tensorflow as tf
from tensorflow import keras
import pickle
from MFCC import MFCC
import numpy as np
from sklearn.preprocessing import LabelEncoder
app = Flask(__name__)

# Load the trained model
# with open('C:/Users/Admin/Documents/GitHub/Sound-processing/Test-soundProcessing/trained_model.pkl', 'rb') as file:
#     model = pickle.load(file)
model = tf.keras.models.load_model('C:/Users/duyma/Documents/GitHub/Speech-Recognize/Data/WEb/model.h5')
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get the input data from the form
    input_data = request.form['input_data']
    TEST_PATH='C:/Users/duyma/Documents/GitHub/Speech-Recognize/Data/Data/LibriSpeech/testWebData'
    Mfcc=MFCC(TEST_PATH,input_data)
    A = Mfcc[:,0:400]
    print(A)
    A=np.expand_dims(A, axis=0)
    prediction = model.predict(A)
    print("prediction shape:", prediction)
    a=np.argmax(prediction)
    pred=np.array([a])
# Load the label encoder
    with open('C:/Users/duyma/Documents/GitHub/Speech-Recognize/Data/WEb/label_encoder.pkl', 'rb') as f:
        label_encoder = pickle.load(f)
    
    # Load the encoded data as a NumPy array
    encoded_data = np.load('C:/Users/duyma/Documents/GitHub/Speech-Recognize/Data/WEb/encoded_data.npy')

    # Decode the encoded data

    decoded_value = label_encoder.inverse_transform(pred)[0]
    print(decoded_value)
    # Preprocess the input data if necessary


    # Process the predictions if necessary

    # Return the output to the user
    return render_template('result.html', predictions=decoded_value,compatibles=np.max(prediction))

if __name__ == '__main__':
    app.run(debug=True)
