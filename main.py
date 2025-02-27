from flask import Flask, request, render_template
import os 
from PIL import Image
from werkzeug.utils import secure_filename
import numpy as np


app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



# check if the upload folder exists 
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def extract_colors(image_path):
    image = Image.open(image_path).convert("RGB")
    image_array = np.array(image)
    unique_colors = np.unique(image_array.reshape(-1, 3), axis=0)
    return unique_colors


@app.route('/', methods=["GET","POST"])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith(("png", "jpg", "jpeg")):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            colors = extract_colors(filepath)


            return render_template("results.html", filename=filename, colors=colors)


    return render_template("index.html")




if __name__ == "__main__":
    app.run(debug=True)