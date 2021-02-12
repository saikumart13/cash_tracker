from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    
    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    particulars = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime,nullable=False, default=datetime.utcnow)
    amount = db.Column(db.Float, nullable=False)
    t_type = db.Column(db.String(1), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='assets', lazy=True)

    
    def __repr__(self):
        return f"Asset('{self.date}','{self.particulars}','{self.t_type}','{self.amount}')"