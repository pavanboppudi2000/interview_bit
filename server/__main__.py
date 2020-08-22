from server.app import app, db
from server.models import *


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    # setting host to 0.0.0.0 to access the site on local ip addresses (ifconfig)
    app.run(host='0.0.0.0', port=8080, debug=True)
