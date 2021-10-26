from exts import db
from datetime import datetime


class SampleModel(db.Model):
    __tablename__ = 'sample'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    sample_name = db.Column(db.String(100), nullable=False)
    sample_place = db.Column(db.String(100), nullable=False)
    collector = db.Column(db.String(100), nullable=False)
    sample_time = db.Column(db.String(100), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

    state = db.Column(db.Integer, default=0, nullable=False)
    author_id = db.Column(db.Integer,db.ForeignKey('system_user.id'), nullable=False)
    author = db.relationship("User_Model", backref="sample_list")
