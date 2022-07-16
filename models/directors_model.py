from sqlalchemy.dialects.postgresql import UUID
import uuid
import marshmallow as ma
from db import db

class Directors(db.Model):
    __tablename__= 'directors'
    director_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    director_first_name = db.Column(db.String(), nullable=False)
    director_last_name = db.Column(db.String(), nullable=False)
    active = db.Column(db.Boolean(), nullable = False, default = True)

    def __init__(self, director_first_name, director_last_name):
        self.director_first_name = director_first_name
        self.director_last_name = director_last_name

class DirectorsSchema(ma.Schema):
    class Meta:
        fields = ['director_id', 'director_first_name', 'director_last_name', 'active']

director_schema = DirectorsSchema()
directors_schema = DirectorsSchema(many=True)