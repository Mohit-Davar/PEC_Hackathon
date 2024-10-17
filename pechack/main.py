from flask import Flask, render_template,jsonify
import sys
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
import json
from flask import Response,request

from wtforms.validators import InputRequired

import populate_database
import query_data
app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = './data'

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")
UPLOAD_FOLDER = './data'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/upload', methods=['POST'])
def upload_pdf():
    # Check if a file is present in the request
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    
    file = request.files['file']
    if file.filename == '' or not file.filename.endswith('.pdf'):
        return jsonify({"error": "No selected file or not a PDF"}), 400

    # Save the file to the specified folder
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    return     query(), 200


@app.route('/home', methods=['GET',"POST"])
def home():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data # First grab the file
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename))) # Then save the file
        return "File has been uploaded."
    return render_template('index.html', form=form)
@app.route('/dataup',methods=['GET','POST'])
def query():
    populate_database.main()

    return jsonify({ 'Questions' :query_data.main("Generate 5 random question related to the pdf")})


@app.route('/query/',methods=['POST'])
def submit_string():
     # Check if the request is JSON
    if request.is_json:
        # Get the JSON data from the request
        data = request.get_json()
        
        # Process the JSON data (you can access keys like a dictionary)
        response_message = {
            "message": "JSON received successfully!",
            "received_data": data
        }
        return jsonify({'ans':query_data.main(data.get('query'))}), 200
    else:
        return jsonify({"error": "Request must be JSON"}), 400
    
if __name__ == '__main__':
    app.run(debug=True,port=8080)