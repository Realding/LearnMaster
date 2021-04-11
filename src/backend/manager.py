from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

from .models import User
from .models.db import db
from .app import create_app

app = create_app()

# db
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


# shell
def make_shell_context():
    return dict(app=app, db=db)


manager.add_command('shell', Shell(make_context=make_shell_context))

#
# # custom
# @manager.option('-u', '--user', dest='name', help='Your name')
# @manager.option('-p', '--password', dest='password', help='Your password')
# def create_super_user(name, password):
#     user = User(username=name, password=password)
#     user.phone = ''
#     user.email = ''
#     user.is_admin = True
#     db.session.add(user)
#     db.session.commit()
#     print('New user created:', user)
#

if __name__ == '__main__':
    manager.run()
