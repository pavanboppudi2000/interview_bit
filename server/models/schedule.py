from server.app import app, db
from datetime import datetime
from server.models.user import User


class Schedule(db.Model):
    __tablename__ = "schedules"
    schedule_id = db.Column('sch_id', db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time

    def commit(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_upcoming_schedules():
        from server.models.participants import Participants
        current_time = datetime.now()
        final_schedules = []
        schedules = db.session.query(Schedule).filter(Schedule.start_time > current_time).all()
        for schedule in schedules:
            curr_schedule = Schedule.get_current_schedule(schedule.schedule_id)
            final_schedules.append(curr_schedule)
        return final_schedules

    @staticmethod
    def get_current_schedule(schedule_id):
        from server.models.participants import Participants
        participants = db.session.query(Participants).filter(Participants.schedule_id == schedule_id).all()
        emails = []
        curr_schedule = {}
        schedule = db.session.query(Schedule).filter(Schedule.schedule_id == schedule_id).scalar()
        curr_schedule["id"] = schedule_id
        curr_schedule["start_time"] = schedule.start_time
        curr_schedule["end_time"] = schedule.end_time
        for participant in participants:
            email = db.session.query(User.email).filter(User.id == participant.user_id).scalar()
            emails.append(email)
        curr_schedule["emails"] = emails
        return curr_schedule
    
    @staticmethod
    def delete_schedule(schedule_id):
        db.session.query(Schedule).filter(Schedule.schedule_id == schedule_id).delete()
        db.session.commit()

    @staticmethod
    def update_schedule(schedule_id, start_time, end_time):
        db.session.query(Schedule).filter(Schedule.schedule_id == schedule_id)\
            .update({"start_time" : start_time, "end_time": end_time})
        db.session.commit()
