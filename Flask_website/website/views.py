from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import *
from . import db
from .webscrape import *
from pretty_html_table import build_table

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


@views.route('/delete/<int:id>') #unused route for testing
def delete(id):
    note = Note.query.get(id)
    if note:
        db.session.delete(note)
        db.session.commit()
        flash("Deleted", category = "success")
    return redirect('/')

