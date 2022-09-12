from bot import db

class DuplicateReport(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.String(80), unique=True, nullable=False)
    HackerOne_report_id = db.Column(db.String(120), unique=True, nullable=True)

    def __repr__(self):
        return '<chat_id %r>' % self.chat_id