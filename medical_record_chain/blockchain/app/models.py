# app/models.py

from app import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
from flask_user import UserMixin, SQLAlchemyAdapter, UserManager


class Block(db.Model):
    """This class represents the medical record table."""

    __tablename__ = 'block'

    block_number = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(
        db.DateTime,
        default=db.func.current_timestamp()
        )
    nonce = db.Column(db.Integer)
    previous_hash = db.Column(db.String(64))
    transactions = db.Column(JSON)

    def __init__(self, block_number, nonce, previous_hash, transactions):
        """initialize with name."""
        self.block_number = block_number
        self.nonce = nonce
        self.previous_hash = previous_hash
 #       self.transactions = convert_transactions_to_JSON(transactions)


    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Block.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Block: {}>".format(self.name)
