from server.app import app, db
from server.models.schedule import Schedule
from server.models.user import User
from datetime import datetime

class Participants(db.Model):
    __tablename__ = "participants"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey(User.id))
    schedule_id = db.Column(db.ForeignKey(Schedule.schedule_id))

    schedule = db.relationship(
        'Schedule', foreign_keys='Participants.schedule_id')
    participant = db.relationship(
        'User', foreign_keys='Participants.user_id')

    def __init__(self, schedule_id, user_id):
        self.schedule_id = schedule_id
        self.user_id = user_id

    def commit(self):
        db.session.add(self)
        db.session.commit()


    @staticmethod
    def clash(startTime, endTime, givenStartTime, givenEndTime):
        if startTime <= givenStartTime:
            return endTime >= givenStartTime
        else:
            return startTime <= givenEndTime

    @staticmethod
    def is_available(email, start_time, end_time, curr_schedule_id = None):
        """"""
        user_id = db.session.query(User.id).filter(User.email==email).scalar()
        print("User ID:", user_id)
        schedules = db.session.query(Participants.schedule_id).filter(Participants.user_id==user_id).all()
        print("Schedules:", list(schedules))
        clashing = False
        if schedules is not None:
            for schedule_id in schedules:
                if curr_schedule_id is not None and schedule_id[0] != curr_schedule_id:
                    schedule = db.session.query(Schedule).filter(Schedule.schedule_id==schedule_id[0]).scalar()
                    if schedule is not None:
                        print('if schedule not none', schedule.start_time, schedule.end_time)
                        clashing = clashing or Participants.clash(schedule.start_time, schedule.end_time,\
                            start_time, end_time)

        print(clashing)
        return (not clashing), user_id
    
    @staticmethod
    def delete_schedule_participants(schedule_id):
        db.session.query(Participants).filter(Participants.schedule_id == schedule_id).delete()
        db.session.commit()