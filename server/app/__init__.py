from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from .config import Config
import json
from datetime import datetime


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())
    app.static_folder = app.config['STATIC_FOLDER']

    db.init_app(app)
    mail.init_app(app)
    return app


db = SQLAlchemy()
mail = Mail()
app = create_app()

# TODO fix this import cycles
from server.app.utils import *


@app.route('/')
def home():
    schedules = get_upcoming_schedules()

    return render_template('index.html', schedules=schedules)


@app.route('/new', methods=["GET", "POST"])
def new():
    if request.method == "GET":
        return render_template('new.html')
    elif request.method == "POST":
        data = request.data
        data = json.loads(data.decode('utf8'))

        start_time = datetime.fromisoformat(data['startTime'])
        end_time = datetime.fromisoformat(data['endTime'])

        # validate inputs here as well
        if (start_time > end_time):
            return jsonify({'error': "Bad api request, start > end"})

        emails = data['emails'].split(',')
        emails = [email.strip() for email in emails]

        valid_emails = validate_emails(emails)

        # validity of all emails
        perfect = True
        for valid in valid_emails:
            perfect = perfect and valid

        if perfect:
            unavailable, available = check_participants_avaliability(
                emails, start_time, end_time)          
            if len(unavailable) > 0:
                return jsonify({"error": "These paricipants are unavailable", 'participants': unavailable})
            else:
                add_schedule(available, start_time, end_time)
        else:
            return jsonify({"valid": valid_emails, "error": "Some participants doesn't exist"})

        return jsonify({"error": None, 'success': True})


@app.route('/delete/<int:interview_id>', methods=["DELETE"])
def delete_schedule(interview_id):
    delete_current_schedule(interview_id)
    return jsonify({})


@app.route('/edit/<int:interview_id>',  methods=["GET", "PATCH"])
def edit(interview_id: int):
    schedule_id = (interview_id)
    if request.method == "GET":
        schedule = get_current_schedules(schedule_id)
        return render_template('edit.html', schedule=schedule)
    elif request.method == "PATCH":
        data = request.data
        data = json.loads(data.decode('utf8'))
        start_time = datetime.fromisoformat(data['startTime'])
        end_time = datetime.fromisoformat(data['endTime'])

        if (start_time > end_time):
            return jsonify({'error': "Bad api request, start > end"})

        emails = data['emails'].split(',')
        emails = [email.strip() for email in emails]

        valid_emails = validate_emails(emails)

        # validity of all emails
        perfect = True
        for valid in valid_emails:
            perfect = perfect and valid

        if perfect:
            unavailable, available = check_participants_avaliability(
                emails, start_time, end_time, schedule_id)
            update_schedule_participants(schedule_id, start_time, end_time, available)            
            if len(unavailable) > 0:
                return jsonify({"error": "These paricipants are unavailable", 'participants': unavailable})
            else:

                return jsonify({"valid": valid_emails, "error": "Some participants doesn't exist"})

        return jsonify({"error": None, 'success': True})

@app.route('/search', methods=['POST'])
def results():
    term = json.loads(request.data.decode('utf8'))['term']
    print(term)
    from server.models.user import User
    return jsonify(User.get_similar_users(term))


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404
