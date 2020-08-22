from server.app import db

# import logging
# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

class User(db.Model):
    id = db.Column('uid', db.Integer, primary_key=True)
    name = db.Column('name', db.String(100))
    # TODO unique
    email = db.Column('email', db.String(100), unique=True)
    # TODO add passwords


    def __init__(self, name, email):
        self.name = name
        self.email = email


    @staticmethod
    def is_valid_email(email):
        # TODO can be improved by making it a single sql query
        done = db.session.query(User.email).filter(User.email==email).scalar()
        print(email, done)
        exists =  done is not None
        return exists

    @staticmethod
    def check_valid_emails(emails):
        valid = []        
        for email in emails:
            valid.append(User.is_valid_email(email))
        return valid

    @staticmethod
    def get_similar_users(search):
        results = User.query.filter(User.email.like(search) | User.name.like(search)).all()
        return results
