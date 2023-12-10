from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import *
from . import db
from .webscrape import *
from pretty_html_table import build_table
from .similarity_checker import *
import tensorflow as tf

views = Blueprint("views", __name__)

@views.route('/', methods = ['GET', 'POST']) #homepage
def home():
    links = []
    title = []
    if request.method == "POST":
        ticker = request.form.get('note').upper()
        links_and_title = list(get_links_and_title(ticker).items())
        for entries in links_and_title:
            links.append(entries[1])
            title.append(entries[0])
        print(links_and_title)
    return render_template("home.html", user = current_user,links = links, title = title, type = type, total = zip(links,title))

@views.route('/sim-score', methods = ['GET', 'POST']) #sim_score checker
def sim_score():
    links = []
    title = []
    prompt_response = ""
    loading = False
    if request.method == "POST":
        searchQuery = request.form.get('searchQuery').upper()
        articleContent = request.form.get('articleContent').upper()
        if ((searchQuery) and (articleContent)):
            html_content = google_search(searchQuery)
            data = extract_headings_and_links(html_content)

            for i, entry in enumerate(data[:5], 1):
                title.append(entry['heading'])
                links.append(entry['url'])
                print(f"{i}. {entry['heading']} - {entry['url']}")
                print(links)
                print(title)

            loading = True
            prompt_response = similarity_checker(searchQuery, articleContent)
            loading = False
        else:
            prompt_response = "Please fill both fields."
            
    return render_template("sim_score.html", user = current_user, prompt_response = prompt_response, loading = loading, links = links, title = title, total = zip(links, title))

@views.route('/lstm_model', methods = ['GET', 'POST']) #LSTM
def lstm():
    model = tf.keras.models.load_model('saved_model/my_model')
    loading = True
    results = False
    if request.method == "POST":
        searchQuery = request.form.get('searchQuery').upper()
        articleContent = request.form.get('articleContent').upper()
        loading = False
        prediction = model.predict([" ".join([searchQuery, articleContent])])
        results = "Fake!" if prediction > 0.5 else "Real!"
    return render_template("lstm.html", user = current_user, results = results, loading = loading)

@views.route('/delete/<int:id>') #unused route for testing
def delete(id):
    note = Note.query.get(id)
    if note:
        db.session.delete(note)
        db.session.commit()
        flash("Deleted", category = "success")
    return redirect('/')

