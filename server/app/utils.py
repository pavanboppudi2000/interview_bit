from server.models.user import User
from server.models.participants import Participants
from server.models.schedule import Schedule


def validate_emails(emails):
    valid_emails = User.check_valid_emails(emails)
    return valid_emails


def check_participants_avaliability(emails, startTime, endTime, curr_schedule_id = None):
    """Returns any unavailable participants info from the start and end times"""

    unavailable, available_userIDs = [], []
    for email in emails:
        available, userID = Participants.is_available(email, startTime, endTime, curr_schedule_id)
        if available:
            available_userIDs.append(userID)
        else:
            unavailable.append(email)
    print("Unavailable: ", unavailable)
    return unavailable, available_userIDs


def update_schedule_participants(schedule_id, start_time, end_time, userIDs):
    Participants.delete_schedule_participants(schedule_id)
    Schedule.update_schedule(schedule_id, start_time, end_time)
    for userID in userIDs:
        pariticipant = Participants(schedule_id, userID)
        pariticipant.commit()


def add_schedule(userIDs, startTime, endTime):
    schedule = Schedule(startTime, endTime)
    schedule.commit()
    print(schedule.schedule_id)
    # TODO can be added in the schedule class it self
    for userID in userIDs:
        pariticipant = Participants(schedule.schedule_id, userID)
        pariticipant.commit()

def get_upcoming_schedules():
    return Schedule.get_upcoming_schedules()

def get_current_schedules(schedule_id):
    return Schedule.get_current_schedule(schedule_id)

def delete_current_schedule(schedule_id):
    Schedule.delete_schedule(schedule_id)
    Participants.delete_schedule_participants(schedule_id)
