#
# image.py
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
