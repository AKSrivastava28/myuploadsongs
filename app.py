import os 
from flask import Flask,request,render_template,redirect,url_for
from werkzeug.utils import secure_filename
app = Flask(__name__)

UPLOAD_FOLDER = 'static/songs'
ALLOWED_EXTENSIONS = {'mp3', 'wav'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

SONG_FOLDER= os.path.join(os.getcwd(), UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    songs = [f for f in os.listdir(SONG_FOLDER) if f.endswith(('.mp3', '.wav'))]
    return render_template('index.html',songs=songs)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method=='POST':
        if 'file' not in request.files:
            return "No file part"
        file = request.files['file']
        if file.filename == '':
            return "No selected file"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('home'))
    return render_template('upload.html')

@app.route('/about_us')
def about_us():
    return render_template('aboutus.html')
if __name__ == '__main__':
    app.run(debug=True)