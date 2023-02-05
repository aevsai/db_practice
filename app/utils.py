import logging

logger = logging.getLogger('uvicorn')


class Updatable():

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if value:
                if hasattr(self, key):
                    setattr(self, key, value)
