#
# Handler.py
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

from django.shortcuts import render

from com.yoclabo.alfresco.item import Item
from com.yoclabo.setting import server


class Handler:

    def __init__(self):
        self.f_request = None
        self.f_parameters: list = []
        self.f_id: str = ''
        self.f_skip_count: int = 0

    @property
    def request(self):
        return self.f_request

    @property
    def parameters(self) -> list:
        return self.f_parameters

    @property
    def id(self) -> str:
        return self.f_id

    @property
    def skip_count(self) -> int:
        return self.f_skip_count

    @request.setter
    def request(self, arg):
        self.f_request = arg

    @parameters.setter
    def parameters(self, arg: list):
        self.f_parameters = arg

    @id.setter
    def id(self, arg: str):
        self.f_id = arg

    @skip_count.setter
    def skip_count(self, arg: int):
        self.f_skip_count = arg

    def query_node(self) -> dict:
        l_node = Item.Node()
        l_node.id = self.id
        l_children = l_node.query_children(self.skip_count)
        for c in l_children:
            l_node.add_child(c)
        return {'node': l_node, 'link': server.get_django_server_name()}

    def query_image(self) -> dict:
        l_image = Item.Image()
        l_image.id = self.id
        return {'node': l_image}


class NodeHandler(Handler):

    def __init__(self):
        super().__init__()

    def run(self):
        if not self.id:
            self.id = '-root-'
            self.skip_count = 0
        return render(self.request, 'alfresco/browse.html', self.query_node())


class ImageHandler(Handler):

    def __init__(self):
        super().__init__()

    def run(self):
        return render(self.request, 'alfresco/view.html', self.query_image())
