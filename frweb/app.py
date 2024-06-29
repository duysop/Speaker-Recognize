from flask import Flask, request, render_template, jsonify, send_from_directory
import os
from werkzeug.utils import secure_filename
from transformers import AutoFeatureExtractor, AutoModelForAudioClassification, TrainingArguments, Trainer
from sklearn.preprocessing import LabelEncoder
import pickle
import soundfile as sf
from datetime import datetime
with open('C:/Users/duyma/Documents/GitHub/Speaker-Recognize/WavLM/label_encoder.pkl', 'rb') as f:
    label_encoder = pickle.load(f)

import mysql.connector
from mysql.connector import errorcode

import base64

# Thiết lập kết nối đến MySQL
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="duy100301",
  database="INFor"
)

# Hàm để lấy thông tin người dùng từ cơ sở dữ liệu
def get_user_info(name):
    try:
        # Tạo cursor để thực hiện truy vấn
        cursor = mydb.cursor(dictionary=True)

        # Truy vấn để lấy thông tin của người dùng
        query = "SELECT id, name, email,phone , image FROM users WHERE name = %s"
        cursor.execute(query, (name,))

        # Lấy kết quả từ cursor
        user_info = cursor.fetchone()

        # Đóng cursor sau khi sử dụng
        cursor.close()

        if user_info and user_info['image']:
            user_info['image'] = base64.b64encode(user_info['image']).decode('utf-8')
        return user_info

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def save_attendance_history(name):
    try:
        cursor = mydb.cursor()
        query = "INSERT INTO attendance_history (name) VALUES (%s)"
        cursor.execute(query, (name,))
        mydb.commit()
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def update_month(table_name, year, month):
    cursor = mydb.cursor()
    for day in range(1, 32):  # Assuming a maximum of 31 days
        try:
            cursor.execute(f"""
                UPDATE {table_name} ma
                JOIN attendance_history ah
                ON ma.name = ah.name
                SET ma.day{day} = TRUE
                WHERE DATE(ah.timestamp) = '{year}-{str(month).zfill(2)}-{str(day).zfill(2)}'
            """)
           

        # Commit thay đổi
            mydb.commit()

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_BAD_FIELD_ERROR:
                break  

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

fe = AutoFeatureExtractor.from_pretrained("microsoft/wavlm-base")
model = AutoModelForAudioClassification.from_pretrained("C:/Users/duyma/Documents/GitHub/Speaker-Recognize/WavLM/Wav30fr", num_labels=29)

@app.route('/')
def index():
    return render_template('home.html')
@app.route('/today')
def today():
    update_month('monthly_attendance_june_2024', 2024, 6)

    cur = mydb.cursor()
    query = "SELECT * FROM monthly_attendance_june_2024"
    cur.execute(query)
    attendance_data = cur.fetchall()
    days = 31

    return render_template('today.html', data=attendance_data, days=days)
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
    person_inf = get_user_info(decoded_value)
    save_attendance_history(decoded_value)
    return jsonify(person_inf), 200
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    print(f"Serving file from: {file_path}")  # Debugging: Print the file path
    if os.path.exists(file_path):
        return send_from_directory('C:/Users/duyma/Documents/GitHub/Speaker-Recognize/uploads', filename)
    else:
        return jsonify({"error": "File not found"}), 404

@app.route('/attendance_history/<name>', methods=['GET'])
def attendance_history(name):
    try:
        cursor = mydb.cursor(dictionary=True)
        query = "SELECT timestamp FROM attendance_history WHERE name = %s ORDER BY timestamp DESC"
        cursor.execute(query, (name,))
        history = cursor.fetchall()
        cursor.close()
        return jsonify(history)
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    
@app.route('/search_user', methods=['GET'])
def search_user():
    name = request.args.get('name')
    try:
        cursor = mydb.cursor(dictionary=True)
        query = "SELECT id, name, email, phone, image FROM users WHERE name = %s"
        cursor.execute(query, (name,))
        user_info = cursor.fetchone()
        cursor.close()
        if user_info and user_info['image']:
            user_info['image'] = base64.b64encode(user_info['image']).decode('utf-8')
        return jsonify(user_info) if user_info else jsonify({'error': 'User not found'}), 404
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    
@app.route('/attendance_today', methods=['GET'])
def attendance_today():
    today = datetime.now().date()
    try:
        cursor = mydb.cursor(dictionary=True)
        query = """
        SELECT name, timestamp
        FROM attendance_history 
        WHERE DATE(timestamp) = %s
        """
        cursor.execute(query, (today,))
        attendance_list = cursor.fetchall()
        return jsonify(attendance_list)
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500

if __name__ == '__main__':
    app.run(debug=True)
