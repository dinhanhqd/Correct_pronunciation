from flask import Flask, render_template, request
from pydub import AudioSegment
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Đường dẫn lưu file âm thanh
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'audio_data' not in request.files:
        return 'No file part'
    
    file = request.files['audio_data']
    if file.filename == '':
        return 'No selected file'
    
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Chuyển đổi sang định dạng MP3
        audio = AudioSegment.from_file(file_path)
        mp3_path = file_path.replace('.wav', '.mp3')
        audio.export(mp3_path, format='mp3')
        
        return 'File uploaded and converted to MP3'

if __name__ == '__main__':
    app.run(debug=True)
