from flask_appbuilder.security.sqla.models import User
from sqlalchemy import Column, Integer, ForeignKey, String, Sequence, Table


class UnisetUser(User):
    uuid = Column(String(256), unique=True)
