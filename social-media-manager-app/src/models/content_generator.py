from . import db
from typing import List, Dict
import json

class ContentGeneratorModel(db.Model):
    __tablename__ = 'content_generator'
    id = db.Column(db.Integer, primary_key=True)
    provider_name = db.Column(db.String(100), nullable=False)
    is_configured = db.Column(db.Boolean, default=False)

    @staticmethod
    def get_configured_providers():
        return ContentGeneratorModel.query.filter_by(is_configured=True).all()
