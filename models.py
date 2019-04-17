from app import db
#
# generate database Schemas
class Flaskr(db.Model):
    __tablename__ = "flaskr"
#
    post_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=True)
    text = db.Column(db.String, nullable=True)
#
    def __init__(self, title, text):
        self.title = title
        self.text = text
#
    def __repr__(self):
        return '< title {}>'.format(self.body)