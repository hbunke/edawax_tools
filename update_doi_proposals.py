from config import api_key, url_base, doi_prefix
import requests
import json
from datetime import datetime
from toolz.dicttoolz import get_in


headers = {'Authorization': api_key, 'content-type': 'application/json; charset=UTF-8'}


def update_all():
    
    def update_res(res, org_name):
        currentVersion = get_in(['dara_currentVersion'], res, '1')
        created = res['created']
        doi = dara_doi(org_name, created)
        
        # XXX careful! don't use when there are REAL DOIs already. This is just
        # for old datasets that will be part of production!
        data = json.dumps({'id': res['id'], 'dara_DOI_Proposal': doi,
            'dara_currentVersion': currentVersion, 'dara_DOI': ""})
        
        update('resource_patch', data)
        print u'updated resource "{}"'.format(res['name'])

    def update_pkg(pkg):
        org_name = get_in(['organization', 'name'], pkg, 'edawax')
        currentVersion = get_in(['dara_currentVersion'], pkg, '1')
        # currentVersion = '1'
        created = pkg['metadata_created']
        doi = dara_doi(org_name, created)

        # XXX careful! don't use when there are REAL DOIs already. This is just
        # for old datasets that will be part of production!
        data = json.dumps({'id': pkg['id'], 'dara_DOI_Proposal': doi,
            'dara_currentVersion': currentVersion, 'dara_DOI': "",
            'dara_registered': "", 'dara_updated': ""})
        
        update('package_patch', data)
        map(lambda res: update_res(res, org_name), pkg['resources'])
        print u'updated pkg and resources of "{}"'.format(pkg['title'])
        
    pkgs = get_all_packages()
    a = map(lambda p: update_pkg(p), pkgs)
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
    

def dara_doi(org_name, created):
    dt = datetime.strptime(created, "%Y-%m-%dT%H:%M:%S.%f")
    timestamp = "{:%Y%j.%H%M%S}".format(dt)
    doi = u'{}/{}.{}'.format(doi_prefix, org_name, timestamp)
    return doi


