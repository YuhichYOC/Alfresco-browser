import base64
import json

from . import item
from ..auth import auth
from ..query import query


def node_is_image(arg):
    if 'content' in arg['entry'] \
            and 'mimeType' in arg['entry']['content']:
        if arg['entry']['content']['mimeType'] == 'image/jpeg':
            return True
        elif arg['entry']['content']['mimeType'] == 'image/png':
            return True
        elif arg['entry']['content']['mimeType'] == 'image/gif':
            return True
    return False


def query_child_thumb(child_id, t):
    c = query.get_children(child_id, 0, t)
    c = json.loads(c.decode())
    for child in c['list']['entries']:
        if node_is_image(child):
            thumb_id = child['entry']['id']
            thumb = query.get_content(thumb_id, t)
            thumb = 'data:image/png;base64,' + base64.b64encode(thumb).decode()
            return thumb


class Node(item.Item):

    def __init__(self):
        super().__init__()
        self.children = []
        self.items_on_this_page = 0
        self.page = 0
        self.pages_total = 0
        self.is_image = False

    def add_child(self, add_id):
        self.children.append(add_id)

    def get_children(self):
        return self.children

    def get_page(self):
        return '{:.0f}'.format(self.page)

    def get_prev_skip_count(self):
        if self.page < 2:
            return '{:.0f}'.format(0)
        return '{:.0f}'.format(20 * (self.page - 1))

    def get_next_skip_count(self):
        if self.pages_total < self.page + 2:
            return '{:.0f}'.format(20 * (self.pages_total - 1))
        return '{:.0f}'.format(20 * (self.page + 1))

    def query_children(self, skip_count):
        ret = []
        t = auth.get_ticket()
        c = query.get_children(self.id, skip_count, t)
        c = json.loads(c.decode())
        self.items_on_this_page = 20
        self.pages_total = -(-c['list']['pagination']['totalItems'] // self.items_on_this_page)
        self.page = c['list']['pagination']['skipCount'] / self.items_on_this_page
        row = self.items_on_this_page * self.page
        for child in c['list']['entries']:
            row += 1
            is_image = node_is_image(child)
            thumb = None
            if is_image:
                thumb = query_child_thumb(child['entry']['id'], t)
            add = {
                'row': '{:.0f}'.format(row),
                'id': child['entry']['id'],
                'name': child['entry']['name'],
                'is_image': is_image,
                'thumb': thumb,
            }
            ret.append(add)
        return ret
