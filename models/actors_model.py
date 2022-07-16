from sqlalchemy.dialects.postgresql import UUID
import uuid
import marshmallow as ma
from db import db

class Actors(db.Model):
    __tablename__= 'actors'
    actor_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    actor_first_name = db.Column(db.String(), nullable=False)
    actor_last_name = db.Column(db.String(), nullable=False)
    active = db.Column(db.Boolean(), nullable = False, default = True)

    def __init__(self, actor_first_name, actor_last_name):
        self.actor_first_name = actor_first_name
        self.actor_last_name = actor_last_name

class ActorsSchema(ma.Schema):
    class Meta:
        fields = ['actor_id', 'actor_first_name', 'actor_last_name', 'active']

actor_schema = ActorsSchema()
actors_schema = ActorsSchema(many=True)