#
# Query.py
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
import urllib.request

from com.yoclabo.setting import server


class Query:

    def __init__(self):
        self.f_server_name = server.get_alfresco_url()
        self.f_ticket = ''
        self.f_url = ''
        self.f_node_id = ''
        self.f_skip_count = 0

    @property
    def server_name(self) -> str:
        return self.f_server_name

    @property
    def ticket(self) -> str:
        return self.f_ticket

    @property
    def url(self) -> str:
        return self.f_url

    @property
    def node_id(self) -> str:
        return self.f_node_id

    @property
    def skip_count(self) -> int:
        return self.f_skip_count

    @ticket.setter
    def ticket(self, arg: str):
        self.f_ticket = arg

    @url.setter
    def url(self, arg: str):
        self.f_url = arg

    @node_id.setter
    def node_id(self, arg: str):
        self.f_node_id = arg

    @skip_count.setter
    def skip_count(self, arg: int):
        self.f_skip_count = arg

    def run(self):
        l_request = urllib.request.Request(self.server_name + self.url)
        l_request.add_header('Accept', 'application/json')
        l_request.add_header('Authorization', 'Basic ' + base64.b64encode(self.ticket.encode()).decode())
        with urllib.request.urlopen(l_request) as l_response:
            ret = l_response.read()
        return ret

    @property
    def alfresco_access_ticket(self):
        self.url = server.get_ticket_sub_url()
        l_request = urllib.request.Request(
            self.server_name + self.url,
            json.dumps(server.get_alfresco_auth_params()).encode()
        )
        l_request.add_header('Content-Type', 'application/json')
        with urllib.request.urlopen(l_request) as l_response:
            ret = l_response.read()
        return json.loads(ret)['entry']['id']

    @property
    def node(self):
        self.url = server.get_node_sub_url(self.node_id)
        return self.run()

    @property
    def parent(self):
        self.url = server.get_node_parent_sub_url(self.node_id)
        return self.run()

    @property
    def children(self):
        self.url = server.get_node_children_sub_url(self.node_id, self.skip_count)
        return self.run()

    @property
    def content(self):
        self.url = server.get_node_content_sub_url(self.node_id)
        return self.run()
