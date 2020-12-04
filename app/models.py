from app import db


class Text(db.Model):
    __tablename__ = 'text'
    __searchable__ = ['text']

    id = db.Column(db.Integer, primary_key=True)
    rubrics = db.Column(db.String(30), nullable=False)
    text = db.Column(db.Text, nullable=False)
    created_date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return self.text

