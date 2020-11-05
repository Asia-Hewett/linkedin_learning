from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os.path
from werkzeug.utils import secure_filename # This tool allows us to make sure user uploaded files are safe

app = Flask(__name__) # This is the name of the module running in flask
app.secret_key = 'h323r842sdf23r843' # This allows us to hide information from users

@app.route('/') # This is for someone visiting the home page
def home():
    return render_template('home.html')

@app.route('/your-url', methods=['GET', 'POST'])
def your_url():
    if request.method == 'POST':
        urls = {}

        if os.path.exists('urls.json'):
            with open('urls.json') as urls_file:
                urls = json.load(urls_file)

        if request.form['code'] in urls.keys(): # This grabs all the keys from the dictionary and checks them
            flash('That short name has already been taken. Please select another name.') # This code generates a error
            return redirect(url_for('home'))

        if 'url' in request.form.keys(): # Checks all of the keys for something called url
            urls[request.form['code']] = {'url':request.form['url']}
        else:
            f = request.files['file']
            full_name = request.form['code'] + secure_filename(f.filename)
            f.save('/Users/asiah/Documents/git_repos/linkedin_learning/flask_essential_training/static/user_files/' + full_name)
            urls[request.form['code']] = {'file':full_name}# This is where you'll find the URL links and the shortened version

        with open('urls.json', 'w') as url_file: # The URL address will appear in the urls.json file
            json.dump(urls, url_file) # Saved shortened names for urls will override if used twice
        return render_template('your_url.html', code=request.form['code']) # When working with POST requ use .form[]
    else:
        return redirect(url_for('home'))

@app.route('/<string:code>')
def redirect_to_url(code):
    if os.path.exists('urls.json'):
        with open('urls.json') as urls_file:
            urls = json.load(urls_file)
            if code in urls.keys():
                if 'url' in urls[code].keys():
                    return redirect(urls[code]['url'])
                else:
                    return redirect(url_for('static', filename='user_files/' + urls[code]['file']))