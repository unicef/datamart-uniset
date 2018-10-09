import logging

from flask_appbuilder.basemanager import BaseManager

log = logging.getLogger(__name__)


class UnisetManager(BaseManager):

    def __init__(self, appbuilder):
        super(UnisetManager, self).__init__(appbuilder)
        # self.appbuilder.get_app.config.setdefault('MYADDON_KEY', 'SOME VALUE')

    def register_views(self):
        pass

    def pre_process(self):
        pass

    def post_process(self):
        pass
