import os
import math
import operator
import heapq
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
           # num = ArtPiece.query.filter(or_(  ArtPiece.title.like(search_string), ArtPiece.description.like(search_string))).count()
            #artists=Artist.query.filter(Artist.name.like(search_string))
            return render_template('search.html', artPieces=artPieces,museum_data = museum_info, page_name = "Search", form=form);        
    artPieces = ArtPiece.query.all()

    last_artwork_visited = session["last_artwork_visited"]
    return render_template('search.html',last_artwork_visited =last_artwork_visited , artPieces=artPieces, museum_data = museum_info, page_name = "Search", form=form, active_page="search");


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
        
    return render_template('scan.html', museum_data = museum_info, page_name = "Scan", active_page="scan");


@app.route("/artifact/<int:artwork_id>/<string:sortType>", methods=['GET', 'POST'])
def artifact(artwork_id, sortType ):
    artPiece = ArtPiece.query.get_or_404(artwork_id)
    artist_ida = artPiece.artist_id
    artist = Artist.query.get_or_404(artist_ida)

    if "last_artwork_visited" in session:
        print("In dict")
    else: 
        print("not in")
    last_artwork_visited = session["last_artwork_visited"]
    session["last_artwork_visited"] = artwork_id
    
    if(sortType == "byArtist" ):
        recomendedArt = ArtPiece.query.filter_by(   artist_id= artist_ida    ).limit(4)
    elif(sortType == "byClosest"):
        recomendedArt = nClosest(3, artPiece, ArtPiece.query.all())# ArtPiece.query.filter_by(  artwork_id = one    ).limit(4) 
    elif(sortType == "byRoom"):
        recomendedArt = ArtPiece.query.filter_by(room_id = artPiece.room_id).limit(4)
    else:
        print(sortType +"_not found sort type in route/artifct.py  type")
    return render_template('artifact.html',sortType = sortType ,last_artwork_visited = last_artwork_visited, artPiece = artPiece, artist = artist, recomendedArt=recomendedArt, museum_data = museum_info, page_name = "Artifact");

def nClosest(n,artPiece, artPieces ):
    """
    This Algorithem computes the distance of all artpeices to artpiece, 
    and retuens nof the lowest pythagrion distance 
    """
    #Get coordinates of the artPiece
    x = artPiece.location_x
    y = artPiece.location_y
    #Initalize a dictionay proximityValues
    proximityValues = {}
    #get a contender for closest to artPiece
    for contender in artPieces:
        #as long as it isnt artPiece but is in the same room
        if  contender.room_id == artPiece.room_id and  contender != artPiece :
            #Get coordinates of the contender
            con_x =contender.location_x
            con_y =contender.location_y
            #Calculate distance between artPiece and contender with pythagrion therom
            # D = sqrt((X1 - X2)^2 + (Y1 - Y2)^2)
            distance =  math.sqrt(( x - con_x )**2 + (y - con_y)**2)  
            #append contender as key ans distance as corrisponding value
            proximityValues[contender] = distance
    #sort proximityValues by distance
    sortedDic = sorted(proximityValues.items(), key=lambda x: x[1])
    #add Contenders to a list, li
    li =[]
    for a in sortedDic:
        li.append(a[0]) 
    #return list of contenders of lenth n 
    return li[0:n-1]





@app.route("/room/<int:room_id>", methods=['GET', 'POST'])
def room(room_id):
    room = Room.query.get_or_404(room_id)
    artpieces = ArtPiece.query.filter_by(room_id=room_id)
    page_name = "Room " + str(room.room_id)
    if "last_artwork_visited" in session:
        last_artwork_visited = session["last_artwork_visited"]
    else:
        last_artwork_visited = -1
    return render_template('room.html', museum_data = museum_info, page_name = page_name, room = room, artpieces = artpieces, last_artwork_visited=last_artwork_visited);


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



@app.route("/logout")
def logout():
    flash("You have been logged out successfully")
    return render_template("index.html", museum_data = museum_info, page_name = "Cardiff Museum");

@app.route("/admin")
def admin():
    return render_template('admin.html', page_name='Admin Dashboard', museum_data = museum_info)
