import json
import urllib.request

from ..setting import server as server_setting


def run():
    url = server_setting.get_alfresco_server_name() + server_setting.get_ticket_sub_url()
    req = urllib.request.Request(url, json.dumps(server_setting.get_alfresco_auth_params()).encode())
    req.add_header('Content-Type', 'application/json')
    with urllib.request.urlopen(req) as res:
        t = res.read()
    return t


def get_ticket():
    t = run()
    return json.loads(t)['entry']['id']
