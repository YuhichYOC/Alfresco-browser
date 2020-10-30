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
        server_setting.get_alfresco_server_name(),
        server_setting.get_node_sub_url(node_id),
        t
    )


def get_parent(node_id, t):
    return run(
        server_setting.get_alfresco_server_name(),
        server_setting.get_node_parent_sub_url(node_id),
        t
    )


def get_children(node_id, skip_count, t):
    return run(
        server_setting.get_alfresco_server_name(),
        server_setting.get_node_children_sub_url(node_id, skip_count),
        t
    )


def get_content(node_id, t):
    return run(
        server_setting.get_alfresco_server_name(),
        server_setting.get_node_content_sub_url(node_id),
        t
    )
