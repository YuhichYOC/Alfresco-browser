#
# Router.py
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

from com.yoclabo.routing import Handler


class Router:

    def __init__(self):
        self.f_request = None
        self.f_parameters = []

    @property
    def request(self):
        return self.f_request

    @property
    def parameters(self) -> list:
        return self.f_parameters

    @request.setter
    def request(self, arg):
        self.f_request = arg

    @parameters.setter
    def parameters(self, arg: list):
        self.f_parameters = arg

    def run(self):
        if self.request.GET.get('id') is not None:
            l_id = self.request.GET.get('id')
            l_skip_count = self.request.GET.get('skip_count')
            if 'is_image' not in self.request.GET:
                l_node_handler = Handler.NodeHandler()
                l_node_handler.request = self.request
                l_node_handler.parameters = self.parameters
                l_node_handler.id = l_id
                l_node_handler.skip_count = l_skip_count
                return l_node_handler.run()
            else:
                l_image_handler = Handler.ImageHandler()
                l_image_handler.request = self.request
                l_image_handler.parameters = self.parameters
                l_image_handler.id = l_id
                l_image_handler.skip_count = l_skip_count
                return l_image_handler.run()
        else:
            l_node_handler = Handler.NodeHandler()
            l_node_handler.request = self.request
            l_node_handler.parameters = self.parameters
            return l_node_handler.run()
