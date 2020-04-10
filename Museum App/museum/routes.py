import os
from museum import app, db
from flask import Flask, render_template, url_for, request, flash, redirect, session
from museum.models import *
from museum.forms import *
from museum.config import *
from flask_login import login_user, current_user, logout_user, login_required
#from sqlalchemy import create_engine
from sqlalchemy import *


@app.route("/", methods=['GET', 'POST'])
def mainpage():
    return render_template("index.html", museum_data = museum_info, page_name = "Cardiff Museum", active_page="index");

@app.route("/settings", methods=['GET', 'POST'])
def settings():
    return render_template('settings.html', museum_data = museum_info, page_name = "Settings", active_page = "settings");
    
@app.route("/search", methods=['GET', 'POST'])
def search():
    form = ArtPieceSearchForm()
    search = ArtPieceSearchForm(request.form)
    if request.method == 'POST':
        artPieces = []
        search_string = search.data['search']
        if search.data['search'] != '':
            search_string = '%{0}%'.format(search_string)
            artPieces = ArtPiece.query.filter(or_(  ArtPiece.title.like(search_string), ArtPiece.description.like(search_string))) 

           #### result = ArtPiece.query.join(Artist).filter(Artist.artist_name.like(search_string) ).all()

          #  re=ArtPiece.query.outerjoin(Artist, ArtPiece.c.artist_id == Artist.c.artist_id)

                ### REmBER TO DO ARTIST!!!!!!!!!!!
            return render_template('search.html', artPieces=artPieces,museum_data = museum_info, page_name = "Search", form=form);        
    artPieces = ArtPiece.query.all()
    return render_template('search.html', artPieces=artPieces, museum_data = museum_info, page_name = "Search", form=form, active_page="search");

##################################


@app.route("/artifact/<int:artwork_id>/<string:sortType>", methods=['GET', 'POST'])
def artifact(artwork_id, sortType = "byArtist"):
    artPiece = ArtPiece.query.get_or_404(artwork_id)

    artist_ida = artPiece.artist_id
    artist = Artist.query.get_or_404(artist_ida)

    if(sortType == "byArtist" ):
        recomendedArt = ArtPiece.query.filter_by(   artist_id= artist_ida    ).limit(4)

        ##need to change to closed date
    elif(sortType == "byDate"):
        recomendedArt = ArtPiece.query.filter_by(date = artPiece.date ).limit(4) 
    elif(sortType == "byRoom"):
        recomendedArt = ArtPiece.query.filter_by(room_id =artPiece.room_id).limit(4)
    else:
        print("not found sort type in route/artifct.py  type")
#recomendedArt = recomendedArt.query.filter_by(artwork_id !=artist_ida)


  #  artPeices = ArtPiece.query.get_or_404(artwork_id)   
    return render_template('artifact.html', artPiece = artPiece, artist = artist, recomendedArt=recomendedArt, museum_data = museum_info, page_name = "Artifact");

@app.route("/room/<int:room_id>", methods=['GET', 'POST'])
def room(room_id):
    room = Room.query.get_or_404(room_id)
    artpieces = ArtPiece.query.filter_by(room_id=room_id)
    page_name = "Room " + str(room.room_id)
    return render_template('room.html', museum_data = museum_info, page_name = page_name, room = room, artpieces = artpieces);

@app.route("/scan", methods=['GET', 'POST'])
def scan():
    if request.method == 'POST':
        artwork_id = request.form['scan']
        if artwork_id != '':
            artPiece = ArtPiece.query.get_or_404(artwork_id)

            artist_ida = artPiece.artist_id
            artist = Artist.query.get_or_404(artist_ida)
            recomendedArt = ArtPiece.query.filter_by(   artist_id= artist_ida    ).limit(4)

            #return render_template('artifact.html', artPiece = result, museum_data = museum_info, page_name = "Artifact");
            return render_template('artifact.html', artPiece = artPiece, artist = artist, recomendedArt=recomendedArt, museum_data = museum_info, page_name = "Artifact");
        
    return render_template('scan.html', museum_data = museum_info, page_name = "Scan", active_page="sacn");

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == "Museum" and password == "Password":
            flash("You have been signed in!")
            return redirect(url_for('admin'))
        else:
            return redirect(url_for('login'))
    return render_template('login.html', page_name='Admin Login', museum_data = museum_info, form=form)

#@app.route("/register", methods=['GET', 'POST'])
#def register():
#    form = RegistrationForm()
#    if form.validate_on_submit():
#        user_login = user(username=form.username.data,
#        email=form.email.data, password=form.password.data)
#        db.session.add(user_login)
#        db.session.commit()
#        flash("You have been successfully registered") 
#        return redirect(url_for('login'))
#    return render_template('register.html', page_name='Create an Account', museum_data = museum_info, form=form)

@app.route("/logout")
def logout():
    flash("You have been logged out successfully")
    return render_template("index.html", museum_data = museum_info, page_name = "Cardiff Museum");

@app.route("/admin")
def admin():
    return render_template('admin.html', page_name='Admin Dashboard', museum_data = museum_info)
