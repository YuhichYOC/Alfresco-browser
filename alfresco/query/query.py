#
# query.py
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
import urllib.request

from ..setting import server as server_setting


def run(server_name, sub_url, t):
    url = server_name + sub_url
    req = urllib.request.Request(url)
    req.add_header('Accept', 'application/json')
    req.add_header('Authorization', 'Basic ' + base64.b64encode(t.encode()).decode())
    with urllib.request.urlopen(req) as res:
        ret = res.read()
    return ret


def get_node(node_id, t):
    return run(
        server_setting.get_alfresco_url(),
        server_setting.get_node_sub_url(node_id),
        t
    )


def get_parent(node_id, t):
    return run(
        server_setting.get_alfresco_url(),
        server_setting.get_node_parent_sub_url(node_id),
        t
    )


def get_children(node_id, skip_count, t):
    return run(
        server_setting.get_alfresco_url(),
        server_setting.get_node_children_sub_url(node_id, skip_count),
        t
    )


def get_content(node_id, t):
    return run(
        server_setting.get_alfresco_url(),
        server_setting.get_node_content_sub_url(node_id),
        t
    )
