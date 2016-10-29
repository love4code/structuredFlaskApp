from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    # Using werkzeug to hash our passwords
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username

    # The password hasshing function is implemented through a write only
    # property
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    # When this property is set, the setter method will call Werkzeug's
    # generate_password_function and write the result to the
    # password_hash field.
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    # The verify password method takes a password and passess it to
    # Werkzeug's check_password_hash() function for varification against
    # the hashed version stored in the User model.
    # Returns True if password is a match
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


    # >>> u = User()
    # >>> u.password = 'cat'
    # >>> u.password_hash
    # 'pbkdf2:sha1:1000$Jolpp8cU$e28948bf1bbd6fc46f6849a64a52c5797ded527c'
    # >>> u.verify_password('cat')
    # True
    # >>> u.verify_password('catfish')
    # False
    # >>> u2 = User()
    # >>> u2.password = ('cat')
    # >>> us.password_hash
    # Traceback (most recent call last):
    #   File "<console>", line 1, in <module>
    # NameError: name 'us' is not defined
    # >>> u2.password_hash
    # 'pbkdf2:sha1:1000$vg0qadZT$5f72af07c2aa578778fb5cb7c1659d630e46a1d1'
    # >>>

    # Flask requires the application to set up a callback function that
    # loads a user, given the identifier

    @login_manager.user_loader
    def load_user(user_id):
        """Load User with given identifier"""
        return User.query.get(int(user_id))