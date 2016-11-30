from config import api_key, url_base
import requests
import json
from toolz.dicttoolz import get_in


headers = {'Authorization': api_key, 'content-type': 'application/json; charset=UTF-8'}


def update_all():
    
    def update_res(res):
        currentVersion = get_in(['dara_currentVersion'], res, '1')
        
        # for old datasets that will be part of production!
        data = json.dumps({'id': res['id'],
            'dara_currentVersion': currentVersion, 
            'dara_DOI_Test': "", 'dara_registered_test': "",
            'dara_updated_test': "", 'dara_DOI': "", 'dara_DOI_Test': ""} )
        
        update('resource_patch', data)
        print u'updated resource "{}"'.format(res['name'])

    def update_pkg(pkg):
        currentVersion = pkg['dara_currentVersion'] or '1'
        pubdate = pkg['dara_PublicationDate'] or '2000'

        data = json.dumps({'id': pkg['id'],
            'dara_currentVersion': currentVersion,
            'dara_registered': "", 'dara_updated': "", 'dara_PublicationDate':
            pubdate, 'dara_DOI_Test': "", 'dara_updated_test': "",
            'dara_registered_test': "", 'dara_DOI': "", 'dara_DOI_Test': ""})
        
        update('package_patch', data)
        map(update_res, pkg['resources'])
        print u'updated pkg and resources of "{}"'.format(pkg['title'])
        
    pkgs = get_all_packages()
    a = map(update_pkg, pkgs)
    print u'updated {} packages'.format(len(a))
    

def update(action, data):
    req = requests.post(
        url(action),
        data=data,
        headers=headers)
    if not req.status_code == 200:
        import ipdb; ipdb.set_trace()


def url(action):
        return "{}/api/action/{}".format(url_base, action)
        


def get_all_packages():
    params = {'limit': 1000}
    req = requests.get(url('current_package_list_with_resources'),
            headers=headers, params=params)
    assert req.status_code == 200
    req_dict = json.loads(req.content)
    pkgs = req_dict['result']
    return pkgs
    
