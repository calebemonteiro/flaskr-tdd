import os
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, jsonify
#
# Database Setup
# Defines the full path for the database
DATABASE = 'flaskr.db'
DEBUG = True
SECRET_KEY = 'test_calebe'
USERNAME = 'admin'
PASSWORD = 'admin'
BASEDIR=os.path.abspath(os.path.dirname(__file__))
DATABASE_PATH = os.path.join(BASEDIR, DATABASE)
#
# Database configurations
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH
SQLALCHEMY_TRACK_MODIFICATIONS = False
#
# Creates the APP and Imports the Database Models
app = Flask(__name__)
app.config.from_object(__name__)
db = SQLAlchemy(app)
import models
#
# define views for the application
@app.route('/')
def index():
    """Search the database for entries and display (if applicable)"""
    entries = db.session.query(models.Flaskr)
    return render_template('index.html', entries=entries)
#
@app.route('/add', methods=['POST'])
def add_entry():
    """Add new post to database"""
    if not session.get('logged_in'):
        abort(401)
    new_entry = models.Flaskr(request.form['title'], request.form['text'])
    db.session.add(new_entry)
    db.session.commit()
    flash('New entry was sucessfully posted')
    return redirect(url_for('index'))
#
@app.route('/delete/<int:post_id>', methods=['GET'])
def delete_entry(post_id):
    """Delete post from Database"""
    result = {'status': 0, 'message': 'Error'}
    try:
        new_id = post_id
        db.session.query(models.Flaskr).filter_by(post_id=new_id).delete()
        db.session.commit()
        result = {'status': 1, 'message': 'Post Deleted'}
        flash('The entry was deleted')
    except Exception as e:
        result = {'status': 1, 'message': repr(e)}
    return jsonify(result)
#
@app.route('/search/', methods=['GET'])
def search():
    query = '%' + str(request.args.get('query')) + '%' 
    entries = db.session.query(models.Flaskr).filter(models.Flaskr.text.like(query))
    if query:
        return render_template('search.html', entries=entries, query=query)
    return render_template('search.html')
#
@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login/autentication/session management"""
    error = None
    if request.method == "POST":
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid Username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid Password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('index'))
    return render_template('login.html',error=error)
#
@app.route('/logout')
def logout():
    """User logout/authentication/session management"""
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))
#
if __name__=='__main__':
    app.run()