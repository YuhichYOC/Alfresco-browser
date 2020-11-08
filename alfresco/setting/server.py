#
# server.py
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

def get_alfresco_server_addr():
    return '[alfresco server address]'


def get_alfresco_server_port():
    return '[alfresco port number]'


def get_alfresco_server_tenant():
    return 'alfresco'


def get_alfresco_server_name():
    return get_alfresco_server_addr() + ':' + get_alfresco_server_port() + '/' + get_alfresco_server_tenant() + '/'


def get_alfresco_url():
    return 'http://' + get_alfresco_server_name()


def get_alfresco_auth_params():
    return {
        'userId': '[alfresco user id]',
        'password': '[alfresco user password]',
    }


def get_ticket_sub_url():
    return 'api/-default-/public/authentication/versions/1/tickets'


def get_node_sub_url(node_id):
    return 'api/-default-/public/alfresco/versions/1/nodes/' + node_id + '/'


def get_node_parent_sub_url(node_id):
    return 'api/-default-/public/alfresco/versions/1/nodes/' + node_id + '/parents'


def get_node_children_sub_url(node_id, skip_count):
    return 'api/-default-/public/alfresco/versions/1/nodes/' \
           + node_id + '/children?skipCount=' + str(skip_count) + '&maxItems=20'


def get_node_content_sub_url(node_id):
    return 'api/-default-/public/alfresco/versions/1/nodes/' + node_id + '/content'


def get_django_server_addr():
    return 'localhost'


def get_django_server_port():
    return '8000'


def get_django_server_tenant():
    return 'alfresco'


def get_django_server_name():
    return get_django_server_addr() + ':' + get_django_server_port() + '/' + get_django_server_tenant() + '/'
