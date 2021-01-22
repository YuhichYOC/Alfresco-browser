#
# Item.py
#
# Copyright 2021 Yuichi Yoshii
#     吉井雄一 @ 吉井産業  you.65535.kir@gmail.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import base64
import json

from com.yoclabo.alfresco.query import Query


class Item:

    def __init__(self):
        self.f_id: str = ''
        self.f_name: str = ''
        self.f_ancestor: list = []
        self.f_query: Query.Query = Query.Query()

    @property
    def id(self) -> str:
        return self.f_id

    @property
    def name(self) -> str:
        return self.f_name

    @property
    def ancestor(self) -> list:
        return self.f_ancestor

    @id.setter
    def id(self, arg: str):
        self.f_id = arg
        self.query()

    def query(self) -> None:
        self.f_query.ticket = self.f_query.alfresco_access_ticket
        self.f_query.node_id = self.id
        this_node = self.f_query.node
        this_node = json.loads(this_node.decode())
        self.f_name = this_node['entry']['name']
        self.f_ancestor = self.query_ancestor()
        return None

    def query_ancestor(self) -> list:
        this_ancestors = self.f_query.parent
        this_ancestors = json.loads(this_ancestors.decode())
        ret = []
        if this_ancestors['list']['pagination']['count'] == 0:
            return ret
        for a in this_ancestors['list']['entries']:
            add = {
                'id': a['entry']['id'],
                'name': a['entry']['name'],
            }
            ret.append(add)
            return self.query_ancestor_recurse(a['entry']['id'], ret)

    def query_ancestor_recurse(self, node_id: str, ancestors: list) -> list:
        ret = []
        for a in ancestors:
            ret.append(a)
        self.f_query.node_id = node_id
        this_ancestors = self.f_query.parent
        this_ancestors = json.loads(this_ancestors.decode())
        if this_ancestors['list']['pagination']['count'] == 0:
            return ret
        for a in this_ancestors['list']['entries']:
            add = {
                'id': a['entry']['id'],
                'name': a['entry']['name'],
            }
            ret.insert(0, add)
            return self.query_ancestor_recurse(a['entry']['id'], ret)


class Node(Item):

    def __init__(self):
        super().__init__()
        self.f_children: list = []
        self.f_items_on_this_page: int = 0
        self.f_page: int = 0
        self.f_pages_total: int = 0
        self.f_is_image: bool = False

    @property
    def children(self) -> list:
        return self.f_children

    @property
    def page(self) -> str:
        return '{:.0f}'.format(self.f_page)

    @property
    def prev_skip_count(self) -> str:
        if self.f_page < 2:
            return '{:.0f}'.format(0)
        return '{:.0f}'.format(20 * (self.f_page - 1))

    @property
    def next_skip_count(self) -> str:
        if self.f_pages_total < self.f_page + 2:
            return '{:.0f}'.format(20 * (self.f_pages_total - 1))
        return '{:.0f}'.format(20 * (self.f_page + 1))

    def add_child(self, add_id: str) -> None:
        self.children.append(add_id)
        return None

    def query_children(self, skip_count: int) -> list:
        self.f_query.ticket = self.f_query.alfresco_access_ticket
        self.f_query.node_id = self.id
        self.f_query.skip_count = skip_count
        this_children = self.f_query.children
        this_children = json.loads(this_children.decode())
        self.f_items_on_this_page = 20
        self.f_pages_total = -(-this_children['list']['pagination']['totalItems'] // self.f_items_on_this_page)
        self.f_page = this_children['list']['pagination']['skipCount'] / self.f_items_on_this_page
        row = self.f_items_on_this_page * self.f_page
        ret = []
        for c in this_children['list']['entries']:
            row += 1
            l_is_image = self.node_is_image(c)
            l_thumb = None
            if l_is_image:
                l_thumb = self.query_child_thumb(c['entry']['id'])
            add = {
                'row': '{:.0f}'.format(row),
                'id': c['entry']['id'],
                'name': c['entry']['name'],
                'is_image': l_is_image,
                'thumb': l_thumb,
            }
            ret.append(add)
        return ret

    @staticmethod
    def node_is_image(arg) -> bool:
        if 'content' in arg['entry'] \
                and 'mimeType' in arg['entry']['content']:
            if arg['entry']['content']['mimeType'] == 'image/jpeg':
                return True
            elif arg['entry']['content']['mimeType'] == 'image/png':
                return True
            elif arg['entry']['content']['mimeType'] == 'image/gif':
                return True
        return False

    def query_child_thumb(self, child_id: str) -> str:
        self.f_query.node_id = child_id
        self.f_query.skip_count = 0
        child_thumb = self.f_query.children
        child_thumb = json.loads(child_thumb.decode())
        for t in child_thumb['list']['entries']:
            if self.node_is_image(t):
                thumb_id = t['entry']['id']
                self.f_query.node_id = thumb_id
                thumb = self.f_query.content
                thumb = 'data:image/png;base64,' + base64.b64encode(thumb).decode()
                return thumb


class Image(Item):

    def __init__(self):
        super().__init__()
        self.f_image = None

    @property
    def id(self) -> str:
        return self.f_id

    @property
    def image(self):
        return self.f_image

    @id.setter
    def id(self, arg: str):
        self.f_id = arg
        self.query()
        self.query_image()

    def query_image(self) -> None:
        self.f_query.ticket = self.f_query.alfresco_access_ticket
        self.f_query.node_id = self.id
        l_image = self.f_query.content
        self.f_image = 'data:image/jpeg;base64,' + base64.b64encode(l_image).decode()
        return None
