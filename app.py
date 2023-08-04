from flask import Flask, render_template, flash, redirect, url_for, request, session, logging
from flask_sqlalchemy import SQLAlchemy
import os




app = Flask(__name__)

picfolder = os.path.join('static','images')

app.config['UPLOAD_FOLDER'] = picfolder

logofolder = os.path.join(app.config['UPLOAD_FOLDER'], 'logo.png')

saved_workouts = dict()


@app.route('/')
def index():
    pic = os.path.join(app.config['UPLOAD_FOLDER'], 'dumbbell.jpeg')
    return render_template('home.html', user_image = pic)

@app.route('/register')
def register():
    return render_template('register.html')

import json
@app.route('/database', methods=['GET'])
def show_database():
    return '<pre>' + json.dumps(saved_workouts, indent=4) + '</pre>'

@app.route('/create/routine',methods=["GET","POST"])
def create_routine():
    return render_template('create_routine.html')

@app.route('/create/workout',methods=["GET","POST"])
def create_workout():
    routine = request.form.get('routine_title')
    saved_workouts[routine] = {}
    return render_template('create_workout.html',routine=routine)


@app.route('/routines/<routine>',methods=["GET","POST"])
def routine(routine):
    if request.method == "POST":
        id = request.form.get('workout_title')
        saved_workouts[routine][id] = {}
        saved_workouts[routine][id]['exercise'] = request.form.get('exercise')
        saved_workouts[routine][id]['sets'] = request.form.get('sets')
        saved_workouts[routine][id]['reps'] = request.form.get('reps')
    return render_template('routines.html',saved_workouts=saved_workouts,id=id)

@app.route('/routines', methods=["GET","POST"])
def routines():
    return render_template('routines.html',saved_workouts = saved_workouts)

@app.route('/workouts/<workout>', methods=["GET","POST"])
def workouts(workout):
    data_i_want = saved_workouts[workout]
    if request.method == "POST":
        id = request.form.get('workout_title')
        saved_workouts[workout][id] = {}
        saved_workouts[workout][id]['exercise'] = request.form.get('exercise')
        saved_workouts[workout][id]['sets'] = request.form.get('sets')
        saved_workouts[workout][id]['reps'] = request.form.get('reps')
    return render_template('workouts.html', data=data_i_want, workout=workout)

@app.route('/workout/<routine>/<day>',methods=["GET","POST"])
def workout(routine,day):
    data = saved_workouts[routine][day]
    return render_template('workout.html', data=data, day=day)

@app.route('/<name>/add/workout', methods=["GET","POST"])
def add_workout(name):
    name = name
    return render_template('add_workout.html',name=name)

if __name__ == '__main__':
    app.run(debug=True)
