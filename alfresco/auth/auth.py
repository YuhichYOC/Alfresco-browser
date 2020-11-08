#
# auth.py
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
import urllib.request

from ..setting import server as server_setting


def run():
    url = server_setting.get_alfresco_url() + server_setting.get_ticket_sub_url()
    req = urllib.request.Request(url, json.dumps(server_setting.get_alfresco_auth_params()).encode())
    req.add_header('Content-Type', 'application/json')
    with urllib.request.urlopen(req) as res:
        t = res.read()
    return t


def get_ticket():
    t = run()
    return json.loads(t)['entry']['id']
