# app/models.py

from app import db
from flask_sqlalchemy import SQLAlchemy
from flask_user import UserMixin, SQLAlchemyAdapter, UserManager


class MedicalRecord(db.Model):
    """This class represents the medical record table."""

    __tablename__ = 'medical_records'

    id = db.Column(db.Integer, primary_key=True)
    patient_address = db.Column(db.String(64))
    provider_address = db.column(db.String(64))
    provider_employee_address = db.column(db.String(64))
    medical_record_address = db.column(db.String(64))

    date_created = db.Column(
        db.DateTime
        , default=db.func.current_timestamp()
        )
    date_modified = db.Column(
        db.DateTime
        , default=db.func.current_timestamp()
        , onupdate=db.func.current_timestamp()
        )

    def __init__(self, name):
        """initialize with name."""
        self.name = name

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Bucketlist.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Bucketlist: {}>".format(self.name)

# class UserAuth(db.Model, UserMixin):
#     """
#     User Authentication
#     """
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer(), db.ForeignKey(
#         'user.User_id', ondelete='CASCADE'))

#     # User authentication information
#     username = db.Column(db.String(50), nullable=False, unique=True)
#     password = db.Column(db.String(255), nullable=False)


# Flask-User Initialization
# DB_ADAPTER = SQLAlchemyAdapter(db, MedicalRecord, UserAuthClass=UserAuth)
# initialize sql-alchemy
