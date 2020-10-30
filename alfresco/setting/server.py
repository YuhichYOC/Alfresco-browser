def get_alfresco_server_addr():
    return '[alfresco server address]'


def get_alfresco_server_port():
    return '[alfresco port number]'


def get_alfresco_server_tenant():
    return 'alfresco'


def get_alfresco_server_name():
    return get_alfresco_server_addr() + ':' + get_alfresco_server_port() + '/' + get_alfresco_server_tenant() + '/'


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
