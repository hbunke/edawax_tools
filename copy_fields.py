# Hendrik Bunke <h.bunke@zbw.eu>, 10/2015

import requests
import json
from config import api_key, url_base

headers = {'Authorization': api_key, 'content-type':
           'application/json; charset=UTF-8'}


def get_package_list():
    req = requests.get(url('package_list'), headers=headers)
    content = json.loads(req.content)
    return content['result']


def get_package(pkg_id):
    params = {'id': pkg_id}
    req = requests.get(url('package_show'), params=params, headers=headers)
    assert req.status_code == 200
    return json.loads(req.content)['result']


def update(pkg):
    pkg.update({'dara_Publication_PID': pkg.get('edawax_article_url'),
        'dara_Publication_PIDType': 'URL'})
    data = json.dumps(pkg)
    req = requests.post(url('package_update'), data=data, headers=headers)
    # assert req.status_code == 200
    if not req.status_code == 200:
        import ipdb; ipdb.set_trace()

def update_all_packages():
    map(lambda pkg: update(get_package(pkg)), get_package_list())


def url(cmd):
    return "{}/api/action/{}".format(url_base, cmd) 



