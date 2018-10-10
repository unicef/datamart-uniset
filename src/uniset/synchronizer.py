from flask_appbuilder.models.sqla.interface import SQLAInterface

from uniset.azure.synchronizer import Synchronizer


class UnisetSynchronizer(Synchronizer):
    def _store(self, pk, values):
        from uniset.models import UserProfile
        from superset import db
        from flask_appbuilder.security.sqla.models import User

        created = False
        datamodel = SQLAInterface(User, db.session)

        P = SQLAInterface(UserProfile, db.session)
        u = db.session.query(User).filter_by(email=values['email']).first()
        if not u:
            created = True
            u = User(first_name=values['first_name'],
                     last_name=values['last_name'],
                     email=values['email'],
                     username=values['email'],
                     roles=[self.extra['role']],
                     active=False)
            datamodel.add(u)
        else:
            datamodel.add(u)
        if u.profiles:
            profile = u.profiles[0]
            profile.uuid = values['azure_id']
        else:
            profile = UserProfile(user_id=u.id)
            profile.uuid = values['azure_id']
        P.add(profile)
        return values, created

