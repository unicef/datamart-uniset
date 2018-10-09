from flask_appbuilder import Model
from sqlalchemy import Column, Integer, ForeignKey, String, Sequence
from sqlalchemy.orm import relationship


class UserProfile(Model):
    __tablename__ = 'uniset_userprofile'
    id = Column(Integer, Sequence('ab_userprofile_id_seq'), primary_key=True)
    uuid = Column(String(256), unique=True)

    user_id = Column(Integer, ForeignKey('ab_user.id'), nullable=False)
    user = relationship("User", backref='profiles')
