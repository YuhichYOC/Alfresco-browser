import base64

from . import item
from ..auth import auth
from ..query import query


def query_content(node_id, t):
    ret = query.get_content(node_id, t)
    ret = 'data:image/jpeg;base64,' + base64.b64encode(ret).decode()
    return ret


class Image(item.Item):

    def __init__(self):
        super().__init__()
        self.image = None

    def set_id(self, arg):
        super().set_id(arg)
        self.query_image()

    def get_image(self):
        return self.image

    def query_image(self):
        t = auth.get_ticket()
        self.image = query_content(self.id, t)
