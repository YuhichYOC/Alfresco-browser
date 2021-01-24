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

    def has_get_param(self, name: str) -> bool:
        if self.request.GET is None:
            return False
        if self.request.GET.get(name) is None:
            return False
        if not self.request.GET.get(name):
            return False
        return True

    def get_get_param(self, name: str) -> str:
        return self.request.GET.get(name)

    def run_handler(self, handler: Handler, node_id: str, skip_count: int):
        handler.request = self.request
        handler.parameters = self.parameters
        handler.id = node_id
        handler.skip_count = skip_count
        return handler.run()


class BrowserRouter(Router):

    def __init__(self):
        super().__init__()

    def run(self):
        h = Handler.BrowserHandler()
        return self.run_handler(h, '', 0)


class AlfrescoRouter(Router):

    def __init__(self):
        super().__init__()

    def request_towards_any_image(self) -> bool:
        if not self.has_get_param('id'):
            return False
        if not self.has_get_param('is_image'):
            return False
        return True

    def request_towards_any_node(self) -> bool:
        if not self.has_get_param('id'):
            return False
        if self.has_get_param('is_image'):
            return False
        return True

    def run_root(self):
        h = Handler.NodeHandler()
        return self.run_handler(h, '-root-', 0)

    def run_others(self):
        h = Handler.NodeHandler()
        return self.run_handler(h, self.get_get_param('id'), int(self.get_get_param('skip_count')))

    def run_image(self):
        h = Handler.ImageHandler()
        return self.run_handler(h, self.get_get_param('id'), int(self.get_get_param('skip_count')))

    def run(self):
        if self.request_towards_any_image():
            return self.run_image()
        elif self.request_towards_any_node():
            return self.run_others()
        else:
            return self.run_root()
