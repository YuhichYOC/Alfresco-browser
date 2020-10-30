from django.shortcuts import render

from ..node import image, node
from ..setting import server as server_setting


def root(request):
    return render(request, 'alfresco/browse.html', query_page_params('-root-', 0))


def another(request, node_id, skip_count):
    if 'is_image' not in request.GET:
        return render(request, 'alfresco/browse.html', query_page_params(node_id, skip_count))
    return render(request, 'alfresco/view.html', {'node': query_image(node_id)})


def query_page_params(node_id, skip_count):
    ret = {'node': query_node(node_id, skip_count), 'link': server_setting.get_django_server_name()}
    return ret


def query_node(node_id, skip_count):
    ret = node.Node()
    ret.set_id(node_id)
    c = ret.query_children(skip_count)
    for c_item in c:
        ret.add_child(c_item)
    return ret


def query_image(node_id):
    ret = image.Image()
    ret.set_id(node_id)
    return ret
