# app/models.py

import json
from app import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
from flask_user import UserMixin, SQLAlchemyAdapter, UserManager
from sqlalchemy import func
from sqlalchemy import desc, asc, func

def convert_block_to_dictionary(block):
    return {'block_number':  block.block_number,
            'timestamp':     block.timestamp,
            'transactions':  json.loads(block.transactions),
            'nonce':         block.nonce,
            'previous_hash': block.previous_hash
            }

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
        self.transactions = json.dumps(transactions)


    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_block_count():
        return db.session.query(func.count(Block.block_number))

    @staticmethod
    def get_all_blocks():
        blocks = []

        db_blocks = db.session.query(Block).order_by(Block.block_number)
        for cur_db_block in db_blocks:
            blocks.append(convert_block_to_dictionary(cur_db_block))

        return blocks

    @staticmethod
    def get_newest_block():
        return convert_block_to_dictionary(db.session.query(Block).order_by(Block.block_number.desc).limit(1))

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Block: {}>".format(self.name)
