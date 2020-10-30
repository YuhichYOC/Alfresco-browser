#
# item.py
#
# Copyright 2020 Yuichi Yoshii
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

import json

from ..auth import auth
from ..query import query


class Item:

    def __init__(self):
        self.id = ''
        self.name = ''
        self.ancestor = []

    def set_id(self, arg):
        self.id = arg
        self.query()

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_ancestor(self):
        return self.ancestor

    def query(self):
        t = auth.get_ticket()
        this = query.get_node(self.id, t)
        this = json.loads(this.decode())
        self.name = this['entry']['name']
        self.ancestor = self.query_ancestor(t)

    def query_ancestor(self, t):
        ret = []
        p = query.get_parent(self.id, t)
        p = json.loads(p.decode())
        if p['list']['pagination']['count'] == 0:
            return ret
        for item in p['list']['entries']:
            add = {
                'id': item['entry']['id'],
                'name': item['entry']['name'],
            }
            ret.append(add)
            return self.query_ancestor_recurse(item['entry']['id'], ret, t)

    def query_ancestor_recurse(self, node_id, ancestors, t):
        ret = []
        for a in ancestors:
            ret.append(a)
        p = query.get_parent(node_id, t)
        p = json.loads(p.decode())
        if p['list']['pagination']['count'] == 0:
            return ret
        for item in p['list']['entries']:
            add = {
                'id': item['entry']['id'],
                'name': item['entry']['name'],
            }
            ret.insert(0, add)
            return self.query_ancestor_recurse(item['entry']['id'], ret, t)
