# app/models.py

import json
from app import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
from flask_user import UserMixin, SQLAlchemyAdapter, UserManager
from sqlalchemy import func, DateTime
from sqlalchemy import select, Table, Column, String, MetaData, Integer
from sqlalchemy import desc, asc, func
from flask_sqlalchemy import SQLAlchemy

def convert_block_to_dictionary(block):
    return {'block_number':  block.block_number,
            'timestamp':     block.timestamp,
            'transactions':  None if None == block.transactions else json.loads(block.transactions),
            'nonce':         block.nonce,
            'previous_hash': block.previous_hash
            }

class Block(db.Model):
    """This class represents the medical record table."""

    __tablename__ = 'block'

    block_number = Column(Integer, primary_key=True)
    timestamp = Column(String)
    nonce = Column(Integer)
    previous_hash = Column(String(64))
    transactions = Column(JSON)

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
        return Block.query.count()

    @staticmethod
    def get_all_blocks():
        blocks = []

        db_blocks = Block.query.order_by(asc(Block.block_number)).all()
        for cur_db_block in db_blocks:
            blocks.append(convert_block_to_dictionary(cur_db_block))

        return blocks

    @staticmethod
    def get_newest_block():
        return Block.query.order_by(desc(Block.block_number)).first()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Block: {}>".format(self.name)
