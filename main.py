import os
#import magic
import urllib.request
from app import app
from flask import Flask, Response, flash, request, redirect, render_template
from models.user import User
from werkzeug.utils import secure_filename
import json

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
KEYS =["0iadeeBCasdf33221"]
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload')
def upload_form():
	return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    print("upload file")
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        f = request.files['file']
        key = request.form["key"]
        print(key)
        if(key not in KEYS):
            return render_template("api_auth_error.html")
        if f.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)

            f.save(os.path.join(app.config['UPLOAD_FOLDER'],key, filename))
            flash('File(s) successfully uploaded')
            return redirect('/reports')

@app.route('/reports')
def get_report_auth():
	return render_template('reports_auth.html')

@app.route('/reports', methods=['POST'])
def get_reports():
    if request.method == 'POST':
        # check if the post request has the file part
        key = request.form["key"]
        path_to_json = os.path.join(app.config["REPORTS_FOLDER"],key)
        json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
        reports=[]
        
        for f in json_files:
            with open(os.path.join(path_to_json,f)) as json_data:
                reports.append(json.load(json_data))
        print(reports)
        return render_template('reports.html', data=reports)


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8000)
