from flask_appbuilder import Model
from sqlalchemy import Column, ForeignKey, Integer, Sequence, String
from sqlalchemy.orm import relationship, backref


class UserProfile(Model):
    __tablename__ = 'uniset_userprofile'
    id = Column(Integer, Sequence('ab_userprofile_id_seq'), primary_key=True)
    uuid = Column(String(256), unique=True)

    user_id = Column(Integer, ForeignKey('ab_user.id'), nullable=False)
    # should be OneToOne but cannot be done in SQLAlchemy without touch User
    # and but in SuperSet prevent changing SecurityManager
    user = relationship("User",
                        backref=backref("profiles", cascade="all, delete-orphan")
                        )
